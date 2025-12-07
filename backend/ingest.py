import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
import google.generativeai as genai
import glob
from markdown_it import MarkdownIt
import hashlib
import time
import uuid
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from google.api_core import exceptions as google_exceptions

COLLECTION_NAME = "physical_ai_textbook"

# Gemini embedding-001 uses 768 dimensions by default
VECTOR_SIZE = 768

def load_environment_variables():
    """Loads API keys and other configurations from a .env file."""
    load_dotenv()
    
    # Validate required environment variables
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    if not all([qdrant_url, qdrant_api_key, gemini_api_key]):
        raise ValueError("Missing one or more required environment variables: QDRANT_URL, QDRANT_API_KEY, GEMINI_API_KEY")
    
    return qdrant_url, qdrant_api_key, gemini_api_key

def initialize_qdrant_client(url: str, api_key: str):
    """Initializes and returns a Qdrant client."""
    try:
        client = QdrantClient(
            url=url,
            api_key=api_key,
        )
        # Verify connection
        client.get_collections()
        print("Successfully connected to Qdrant Cloud.")
        return client
    except Exception as e:
        raise ConnectionError(f"Failed to connect to Qdrant Cloud: {e}") from e

def initialize_gemini_api(api_key: str):
    """Configures the Gemini API (no model object needed for embeddings)."""
    try:
        genai.configure(api_key=api_key)
        print("Successfully configured Gemini API for embeddings.")
        return None  # No model object needed for embeddings
    except Exception as e:
        raise ConnectionError(f"Failed to configure Gemini API: {e}") from e

def create_qdrant_collection(client: QdrantClient):
    """Creates the Qdrant collection if it doesn't already exist."""
    try:
        # Check if collection exists first
        collections = client.get_collections().collections
        collection_names = [collection.name for collection in collections]
        
        if COLLECTION_NAME in collection_names:
            print(f"Collection '{COLLECTION_NAME}' already exists. Deleting...")
            client.delete_collection(collection_name=COLLECTION_NAME)
        
        # Create new collection
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )
        print(f"Collection '{COLLECTION_NAME}' created successfully.")
    except Exception as e:
        raise RuntimeError(f"Failed to create Qdrant collection '{COLLECTION_NAME}': {e}") from e

def get_markdown_files(docs_path: str = "../frontend/docs/"):
    """Finds all .md and .mdx files within the specified docs_path."""
    markdown_files = []
    # Use recursive glob to find all .md and .mdx files
    for ext in ["md", "mdx"]:
        markdown_files.extend(glob.glob(f"{docs_path}**/*.{ext}", recursive=True))
    
    if not markdown_files:
        print(f"Warning: No Markdown files found in '{docs_path}'")
    
    return markdown_files

def parse_markdown_file(filepath: str):
    """Reads a markdown file and strips its frontmatter."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple frontmatter stripping: look for --- at the beginning
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) > 2:
            content = parts[2].strip()  # Content after the second ---
        else:
            content = parts[1].strip()  # If only one --- (unlikely for Docusaurus frontmatter)
    
    return content

def chunk_content(text: str):
    """Splits markdown content into chunks based on H2/H3 headers."""
    md = MarkdownIt()
    tokens = md.parse(text)
    
    chunks = []
    current_chunk_content = []
    current_heading = None

    for token in tokens:
        if token.type == 'heading_open' and token.tag in ['h2', 'h3']:
            # If there's content before this new heading, save it as a chunk
            if current_chunk_content:
                chunks.append({
                    "content": "\n".join(current_chunk_content).strip(), 
                    "heading": current_heading
                })
                current_chunk_content = []
            
            # Extract heading text
            next_token_index = tokens.index(token) + 1
            if next_token_index < len(tokens) and tokens[next_token_index].type == 'inline':
                current_heading = tokens[next_token_index].content
            else:
                current_heading = "Unknown Section"
        elif token.type == 'inline' and token.content:
            # Add inline content to current chunk
            current_chunk_content.append(token.content)
        elif token.content:
            # Catch-all for other content types
            current_chunk_content.append(token.content)

    # Add the last chunk if any content remains
    if current_chunk_content:
        chunks.append({
            "content": "\n".join(current_chunk_content).strip(), 
            "heading": current_heading
        })
    
    # Filter out empty chunks and ensure heading is present
    return [chunk for chunk in chunks if chunk["content"] and chunk["heading"]]

@retry(
    retry=retry_if_exception_type((google_exceptions.ResourceExhausted, google_exceptions.TooManyRequests)),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(5)
)
def generate_embedding(text_chunk: str):
    """Generates an embedding for a text chunk using the Gemini embedding API with rate limiting."""
    try:
        # Add a small delay to respect rate limits (12 seconds for 5 RPM)
        time.sleep(12)
        
        # Call embed_content directly on genai module
        response = genai.embed_content(
            model="models/embedding-001",
            content=text_chunk,
            task_type="retrieval_document"  # Use for document chunks
        )
        # Access the embedding from the response dictionary
        return response['embedding']
    except Exception as e:
        raise RuntimeError(f"Gemini API error while generating embedding: {e}") from e

def generate_chunk_id(filepath: str, content: str) -> str:
    """Generates a unique UUID for a chunk based on its filepath and content hash."""
    # Create a deterministic hash from filepath and content
    content_hash = hashlib.sha256(f"{filepath}:{content}".encode('utf-8')).hexdigest()
    # Convert hash to UUID (deterministic, so same content = same ID)
    chunk_uuid = str(uuid.UUID(content_hash[:32]))
    return chunk_uuid

def upload_chunks_to_qdrant(client: QdrantClient, points_data: list[dict]):
    """Upserts document chunks (as pre-prepared PointStruct data) to Qdrant."""
    points = []
    for point_data in points_data:
        points.append(
            PointStruct(
                id=point_data["id"],
                vector=point_data["vector"],
                payload=point_data["payload"],
            )
        )
    
    if points:
        try:
            client.upsert(
                collection_name=COLLECTION_NAME,
                wait=True,
                points=points
            )
            print(f"Successfully upserted {len(points)} points to Qdrant.")
            return len(points)
        except Exception as e:
            raise RuntimeError(f"Failed to upsert points to Qdrant: {e}") from e
    return 0

def ingest_workflow():
    """Orchestrates the entire content ingestion process."""
    print("Starting RAG Ingestion Engine...")

    # Load environment variables
    qdrant_url, qdrant_api_key, gemini_api_key = load_environment_variables()

    # Initialize clients and configure API
    qdrant_client = initialize_qdrant_client(qdrant_url, qdrant_api_key)
    initialize_gemini_api(gemini_api_key)

    # Create Qdrant collection
    create_qdrant_collection(qdrant_client)

    # Get markdown files
    markdown_files = get_markdown_files()
    if not markdown_files:
        print("No markdown files found to ingest. Exiting.")
        return

    total_chunks_indexed = 0

    for filepath in markdown_files:
        print(f"Processing file: {filepath}")
        content = parse_markdown_file(filepath)
        chunks = chunk_content(content)
        
        print(f"  → Found {len(chunks)} chunks to process")
        
        processed_chunks_for_file = []
        for idx, chunk in enumerate(chunks, 1):
            print(f"  → Processing chunk {idx}/{len(chunks)}...", end=" ")
            
            # Prepare payload with metadata
            chunk_payload = {
                "content": chunk["content"],
                "filepath": filepath,
                "heading": chunk["heading"],
            }
            
            # Generate ID and embedding
            chunk_id = generate_chunk_id(filepath, chunk["content"])
            
            try:
                embedding = generate_embedding(chunk["content"])
                print("✓")
            except RuntimeError as e:
                print(f"✗ Failed: {e}")
                continue
            
            processed_chunks_for_file.append({
                "id": chunk_id,
                "vector": embedding,
                "payload": chunk_payload
            })
        
        # Upload chunks for this file
        if processed_chunks_for_file:
            uploaded_count = upload_chunks_to_qdrant(qdrant_client, processed_chunks_for_file)
            total_chunks_indexed += uploaded_count
            print(f"  → Indexed {uploaded_count} chunks from {filepath}")
        else:
            print(f"  → No chunks successfully processed for {filepath}")
    
    print(f"\n✅ RAG Ingestion Engine completed. Successfully indexed {total_chunks_indexed} chunks.")

if __name__ == "__main__":
    try:
        ingest_workflow()
    except ValueError as ve:
        print(f"❌ Configuration Error: {ve}")
    except ConnectionError as ce:
        print(f"❌ Connection Error: {ce}")
    except RuntimeError as re:
        print(f"❌ Ingestion Error: {re}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
"""
RAG Ingestion Engine for Physical AI Textbook.
Uses OpenAI text-embedding-3-small for embeddings and Qdrant for vector storage.
Enhanced with semantic chunking and richer metadata for hybrid search.
"""

import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from openai import OpenAI
import glob
import hashlib
import uuid
import tiktoken

COLLECTION_NAME = "physical_ai_textbook_v2"
EMBEDDING_MODEL = "text-embedding-3-small"
VECTOR_SIZE = 768  # Match previous Gemini embedding size for cost parity
BATCH_SIZE = 100  # OpenAI can handle batches efficiently

# Semantic chunking parameters
MAX_CHUNK_TOKENS = 500
MIN_CHUNK_TOKENS = 50


def load_environment_variables():
    """Loads API keys and other configurations from a .env file."""
    load_dotenv()

    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not all([qdrant_url, qdrant_api_key, openai_api_key]):
        raise ValueError(
            "Missing one or more required environment variables: "
            "QDRANT_URL, QDRANT_API_KEY, OPENAI_API_KEY"
        )

    return qdrant_url, qdrant_api_key, openai_api_key


def initialize_qdrant_client(url: str, api_key: str):
    """Initializes and returns a Qdrant client."""
    try:
        client = QdrantClient(url=url, api_key=api_key)
        client.get_collections()
        print("Successfully connected to Qdrant Cloud.")
        return client
    except Exception as e:
        raise ConnectionError(f"Failed to connect to Qdrant Cloud: {e}") from e


def initialize_openai_client(api_key: str):
    """Initializes and returns an OpenAI client."""
    try:
        client = OpenAI(api_key=api_key)
        print("Successfully initialized OpenAI client.")
        return client
    except Exception as e:
        raise ConnectionError(f"Failed to initialize OpenAI client: {e}") from e


def create_qdrant_collection(client: QdrantClient):
    """Creates the Qdrant collection if it doesn't already exist."""
    try:
        collections = client.get_collections().collections
        collection_names = [collection.name for collection in collections]

        if COLLECTION_NAME in collection_names:
            print(f"Collection '{COLLECTION_NAME}' already exists. Deleting...")
            client.delete_collection(collection_name=COLLECTION_NAME)

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )
        print(f"Collection '{COLLECTION_NAME}' created successfully.")
    except Exception as e:
        raise RuntimeError(
            f"Failed to create Qdrant collection '{COLLECTION_NAME}': {e}"
        ) from e


def get_markdown_files(docs_path: str = "../frontend/docs/"):
    """Finds all .md and .mdx files within the specified docs_path."""
    markdown_files = []
    for ext in ["md", "mdx"]:
        markdown_files.extend(glob.glob(f"{docs_path}**/*.{ext}", recursive=True))

    if not markdown_files:
        print(f"Warning: No Markdown files found in '{docs_path}'")

    return markdown_files


def parse_markdown_file(filepath: str):
    """Reads a markdown file and strips its frontmatter."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) > 2:
            content = parts[2].strip()
        else:
            content = parts[1].strip()

    return content


# Token counter (initialized lazily)
_encoder = None


def count_tokens(text: str) -> int:
    """Count tokens in text using tiktoken."""
    global _encoder
    if _encoder is None:
        try:
            _encoder = tiktoken.encoding_for_model("gpt-4o-mini")
        except KeyError:
            _encoder = tiktoken.get_encoding("cl100k_base")
    return len(_encoder.encode(text))


def semantic_chunk_content(text: str, filepath: str) -> list[dict]:
    """
    Splits markdown content into semantic chunks based on H2/H3 headers.
    Uses token-based fallback for long sections.

    Returns chunks with enhanced metadata:
    - content: The chunk text
    - heading: Section heading
    - position: Order within document
    - parent_heading: Parent H2 for H3 chunks
    - token_count: Pre-computed token count
    """
    import re

    chunks = []
    current_h2 = None
    current_heading = None
    current_content_lines = []
    position = 0

    lines = text.split("\n")

    for line in lines:
        # Check for H2 or H3 headers
        h2_match = re.match(r"^##\s+(.+)$", line)
        h3_match = re.match(r"^###\s+(.+)$", line)

        if h2_match or h3_match:
            # Save previous section if exists
            if current_content_lines and current_heading:
                content = "\n".join(current_content_lines).strip()
                if content:
                    chunks.extend(
                        _create_chunks_from_section(
                            content=content,
                            heading=current_heading,
                            parent_heading=current_h2 if h3_match else None,
                            position=position,
                            filepath=filepath,
                        )
                    )
                    position += 1

            current_content_lines = []

            if h2_match:
                current_h2 = h2_match.group(1).strip()
                current_heading = current_h2
            else:
                current_heading = h3_match.group(1).strip()
        else:
            current_content_lines.append(line)

    # Don't forget the last section
    if current_content_lines and current_heading:
        content = "\n".join(current_content_lines).strip()
        if content:
            chunks.extend(
                _create_chunks_from_section(
                    content=content,
                    heading=current_heading,
                    parent_heading=None,
                    position=position,
                    filepath=filepath,
                )
            )

    # Filter out tiny chunks
    filtered_chunks = [c for c in chunks if c["token_count"] >= MIN_CHUNK_TOKENS]

    return filtered_chunks


def _create_chunks_from_section(
    content: str,
    heading: str,
    parent_heading: str | None,
    position: int,
    filepath: str,
) -> list[dict]:
    """Create one or more chunks from a section, splitting if too long."""
    token_count = count_tokens(content)

    if token_count <= MAX_CHUNK_TOKENS:
        # Section fits in one chunk
        return [
            {
                "content": content,
                "heading": heading,
                "parent_heading": parent_heading,
                "position": position,
                "token_count": token_count,
                "filepath": filepath,
            }
        ]

    # Section too long, split at paragraphs
    paragraphs = content.split("\n\n")
    chunks = []
    current_parts = []
    current_tokens = 0
    sub_position = 0

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        para_tokens = count_tokens(para)

        # If single paragraph exceeds max, just include it (best effort)
        if para_tokens > MAX_CHUNK_TOKENS:
            # Save accumulated content first
            if current_parts:
                chunk_content = "\n\n".join(current_parts)
                chunks.append(
                    {
                        "content": chunk_content,
                        "heading": heading,
                        "parent_heading": parent_heading,
                        "position": position + sub_position * 0.1,
                        "token_count": current_tokens,
                        "filepath": filepath,
                    }
                )
                sub_position += 1
                current_parts = []
                current_tokens = 0

            # Add the large paragraph as its own chunk
            chunks.append(
                {
                    "content": para,
                    "heading": heading,
                    "parent_heading": parent_heading,
                    "position": position + sub_position * 0.1,
                    "token_count": para_tokens,
                    "filepath": filepath,
                }
            )
            sub_position += 1
            continue

        # Check if adding this paragraph exceeds budget
        if current_tokens + para_tokens > MAX_CHUNK_TOKENS and current_parts:
            # Save current chunk
            chunk_content = "\n\n".join(current_parts)
            chunks.append(
                {
                    "content": chunk_content,
                    "heading": heading,
                    "parent_heading": parent_heading,
                    "position": position + sub_position * 0.1,
                    "token_count": current_tokens,
                    "filepath": filepath,
                }
            )
            sub_position += 1
            current_parts = []
            current_tokens = 0

        current_parts.append(para)
        current_tokens += para_tokens

    # Save remaining content
    if current_parts:
        chunk_content = "\n\n".join(current_parts)
        chunks.append(
            {
                "content": chunk_content,
                "heading": heading,
                "parent_heading": parent_heading,
                "position": position + sub_position * 0.1,
                "token_count": current_tokens,
                "filepath": filepath,
            }
        )

    return chunks


def generate_embeddings_batch(
    openai_client: OpenAI, texts: list[str]
) -> list[list[float]]:
    """
    Generate embeddings for a batch of texts using OpenAI.

    Args:
        openai_client: OpenAI client instance
        texts: List of text strings to embed

    Returns:
        List of embedding vectors
    """
    try:
        response = openai_client.embeddings.create(
            model=EMBEDDING_MODEL, input=texts, dimensions=VECTOR_SIZE
        )
        # Sort by index to maintain order
        embeddings = sorted(response.data, key=lambda x: x.index)
        return [e.embedding for e in embeddings]
    except Exception as e:
        raise RuntimeError(
            f"OpenAI API error while generating embeddings: {e}"
        ) from e


def generate_chunk_id(filepath: str, content: str) -> str:
    """Generates a unique UUID for a chunk based on its filepath and content hash."""
    content_hash = hashlib.sha256(f"{filepath}:{content}".encode("utf-8")).hexdigest()
    chunk_uuid = str(uuid.UUID(content_hash[:32]))
    return chunk_uuid


def upload_chunks_to_qdrant(client: QdrantClient, points_data: list[dict]):
    """Upserts document chunks to Qdrant."""
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
                points=points,
            )
            print(f"Successfully upserted {len(points)} points to Qdrant.")
            return len(points)
        except Exception as e:
            raise RuntimeError(f"Failed to upsert points to Qdrant: {e}") from e
    return 0


def ingest_workflow():
    """Orchestrates the entire content ingestion process."""
    print("Starting RAG Ingestion Engine (OpenAI Edition with Semantic Chunking)...")
    print(f"  - Embedding model: {EMBEDDING_MODEL}")
    print(f"  - Vector dimensions: {VECTOR_SIZE}")
    print(f"  - Collection: {COLLECTION_NAME}")
    print(f"  - Max chunk tokens: {MAX_CHUNK_TOKENS}")
    print(f"  - Min chunk tokens: {MIN_CHUNK_TOKENS}")

    # Load environment variables
    qdrant_url, qdrant_api_key, openai_api_key = load_environment_variables()

    # Initialize clients
    qdrant_client = initialize_qdrant_client(qdrant_url, qdrant_api_key)
    openai_client = initialize_openai_client(openai_api_key)

    # Create Qdrant collection
    create_qdrant_collection(qdrant_client)

    # Get markdown files
    markdown_files = get_markdown_files()
    if not markdown_files:
        print("No markdown files found to ingest. Exiting.")
        return

    print(f"\nFound {len(markdown_files)} markdown files to process.")

    # Collect all chunks using semantic chunking
    all_chunks = []
    for filepath in markdown_files:
        content = parse_markdown_file(filepath)
        chunks = semantic_chunk_content(content, filepath)
        for chunk in chunks:
            chunk["id"] = generate_chunk_id(filepath, chunk["content"])
        all_chunks.extend(chunks)

    print(f"Total chunks to process: {len(all_chunks)}")

    # Print chunk statistics
    token_counts = [c["token_count"] for c in all_chunks]
    if token_counts:
        avg_tokens = sum(token_counts) / len(token_counts)
        print(f"  - Average tokens per chunk: {avg_tokens:.1f}")
        print(f"  - Min tokens: {min(token_counts)}, Max tokens: {max(token_counts)}")

    # Process in batches
    total_indexed = 0
    for batch_start in range(0, len(all_chunks), BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE, len(all_chunks))
        batch = all_chunks[batch_start:batch_end]

        print(
            f"\nProcessing batch {batch_start // BATCH_SIZE + 1} ({len(batch)} chunks)..."
        )

        # Extract texts for embedding
        texts = [chunk["content"] for chunk in batch]

        # Generate embeddings in batch
        try:
            embeddings = generate_embeddings_batch(openai_client, texts)
            print(f"  ✓ Generated {len(embeddings)} embeddings")
        except RuntimeError as e:
            print(f"  ✗ Failed to generate embeddings: {e}")
            continue

        # Prepare points for Qdrant with enhanced metadata
        points_data = []
        for chunk, embedding in zip(batch, embeddings):
            payload = {
                "content": chunk["content"],
                "filepath": chunk["filepath"],
                "heading": chunk["heading"],
                "position": chunk["position"],
                "token_count": chunk["token_count"],
            }
            # Add parent_heading if exists
            if chunk.get("parent_heading"):
                payload["parent_heading"] = chunk["parent_heading"]

            points_data.append(
                {
                    "id": chunk["id"],
                    "vector": embedding,
                    "payload": payload,
                }
            )

        # Upload to Qdrant
        try:
            uploaded = upload_chunks_to_qdrant(qdrant_client, points_data)
            total_indexed += uploaded
        except RuntimeError as e:
            print(f"  ✗ Failed to upload: {e}")
            continue

    print(f"\n✅ RAG Ingestion completed. Successfully indexed {total_indexed} chunks.")


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

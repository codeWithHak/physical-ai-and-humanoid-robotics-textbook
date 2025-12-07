import os
from dotenv import load_dotenv
import google.generativeai as genai
from qdrant_client import QdrantClient
from openai import AsyncOpenAI
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

from src.models.rag import RagRequest, RagResponse, SearchResult

class RagService:
    def __init__(self):
        load_dotenv()
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        if not all([self.gemini_api_key, self.qdrant_url, self.qdrant_api_key, self.openai_api_key]):
            raise ValueError("Missing one or more required environment variables for RagService.")

        genai.configure(api_key=self.gemini_api_key)
        self.qdrant_client = QdrantClient(url=self.qdrant_url, api_key=self.qdrant_api_key)
        self.openai_client = AsyncOpenAI(api_key=self.openai_api_key)

        self.system_prompt = "You are an expert AI Robotics Professor. Answer based ONLY on the provided context. If the answer is not in the context, say 'I cannot find that in the textbook'. Always cite the section title."

    @retry(
        wait=wait_exponential(multiplier=1, min=4, max=10), 
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type(Exception)
    )
    async def embed_query(self, text: str) -> list[float]:
        """Generates an embedding for the given text using Google Generative AI."""
        try:
            model = "models/embedding-001"
            print(f"DEBUG: Calling genai.embed_content with model={model}, text length={len(text)}")
            
            # genai.embed_content is synchronous, so we call it directly
            result = genai.embed_content(
                model=model,
                content=text,
                task_type="retrieval_query"
            )
            
            print(f"DEBUG: genai response received, type: {type(result)}")
            
            # Google's embed_content returns a dict-like object
            # Access the embedding using dictionary notation
            embedding = result['embedding']
            
            print(f"DEBUG: Successfully extracted embedding, length={len(embedding)}")
            return embedding
            
        except KeyError as e:
            print(f"ERROR: KeyError in embed_query - response structure: {result}")
            print(f"ERROR: Available keys: {dir(result) if hasattr(result, '__dir__') else 'N/A'}")
            raise AttributeError(f"Could not find 'embedding' in response. Error: {e}")
        except Exception as e:
            print(f"ERROR in embed_query: {type(e).__name__}: {str(e)}")
            raise

    @retry(
        wait=wait_exponential(multiplier=1, min=4, max=10), 
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type(Exception)
    )
    async def retrieve_context(self, query_embedding: list[float], collection_name: str = "physical_ai_textbook") -> list[SearchResult]:
        """Retrieves relevant context from Qdrant using the query embedding."""
        try:
            print(f"DEBUG: Calling qdrant search on collection '{collection_name}'")
            print(f"DEBUG: Query embedding length: {len(query_embedding)}")
            
            # Try new API first (qdrant-client >= 1.7.0)
            try:
                print("DEBUG: Attempting query_points (new API)...")
                search_result = self.qdrant_client.query_points(
                    collection_name=collection_name,
                    query=query_embedding,
                    limit=5
                ).points
                print(f"DEBUG: query_points succeeded")
                
            except AttributeError:
                # Fall back to old API (qdrant-client < 1.7.0)
                print("DEBUG: Falling back to search (old API)...")
                search_result = self.qdrant_client.search(
                    collection_name=collection_name,
                    query_vector=query_embedding,
                    limit=5
                )
                print(f"DEBUG: search succeeded")
            
            print(f"DEBUG: Qdrant found {len(search_result)} results")
            
            results = []
            for point in search_result:
                # Handle both old and new response formats
                payload = getattr(point, 'payload', None)
                if payload:
                    result = SearchResult(
                        text=payload.get("text", ""),
                        source_id=payload.get("source", ""),
                        title=payload.get("header", "")
                    )
                    results.append(result)
                    print(f"DEBUG: Added result from '{result.title}'")
            
            return results
            
        except Exception as e:
            print(f"ERROR in retrieve_context: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            raise

    async def generate_answer(self, context: str, user_query: str) -> str:
        """Generates an answer using the OpenAI Chat Completions API based on the provided context."""
        try:
            print("DEBUG: Calling OpenAI Chat Completions")
            print(f"DEBUG: Context length: {len(context)} characters")
            
            prompt = f"Context from textbook:\n{context}\n\nUser Question: {user_query}"
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            answer = response.choices[0].message.content
            print(f"DEBUG: Generated answer length: {len(answer)} characters")
            return answer
            
        except Exception as e:
            print(f"ERROR in generate_answer: {type(e).__name__}: {str(e)}")
            raise

    async def process_query(self, request: RagRequest) -> RagResponse:
        """Orchestrates the RAG pipeline."""
        try:
            print(f"\n{'='*60}")
            print(f"DEBUG: Starting process_query for: '{request.message}'")
            print(f"{'='*60}\n")
            
            # Step 1: Generate embedding
            print("STEP 1: Generating embedding...")
            query_embedding = await self.embed_query(request.message)
            print(f"✓ Embedding generated successfully\n")
            
            # Step 2: Retrieve context
            print("STEP 2: Retrieving context from Qdrant...")
            context_chunks = await self.retrieve_context(query_embedding)
            print(f"✓ Retrieved {len(context_chunks)} context chunks\n")

            if not context_chunks:
                print("WARNING: No context chunks found")
                return RagResponse(
                    answer="I cannot find that in the textbook.",
                    sources=[]
                )

            # Step 3: Prepare context for LLM
            print("STEP 3: Preparing context...")
            context_text = "\n\n".join([
                f"Source: {c.title} ({c.source_id})\n{c.text}" 
                for c in context_chunks
            ])
            
            sources = sorted(list(set([
                f"{c.title} ({c.source_id})" 
                for c in context_chunks
            ])))
            print(f"✓ Prepared context from {len(sources)} unique sources\n")

            # Step 4: Generate answer
            print("STEP 4: Generating answer with OpenAI...")
            answer = await self.generate_answer(context_text, request.message)
            print(f"✓ Answer generated successfully\n")

            print(f"{'='*60}")
            print("DEBUG: Process completed successfully")
            print(f"{'='*60}\n")

            return RagResponse(answer=answer, sources=sources)
            
        except Exception as e:
            print(f"\n{'='*60}")
            print(f"ERROR in process_query: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            print(f"{'='*60}\n")
            raise
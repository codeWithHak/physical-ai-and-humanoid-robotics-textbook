import os
from dotenv import load_dotenv
import google.generativeai as genai
from qdrant_client import QdrantClient
from openai_agents import Agent, Runner
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

# Assuming SearchResult is defined in models.rag
from backend.src.models.rag import RagRequest, RagResponse, SearchResult

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

        # Initialize OpenAI Agent
        self.agent = Agent(
            name="AI Robotics Professor",
            instructions="You are an expert AI Robotics Professor. Answer based ONLY on the provided context. If the answer is not in the context, say 'I cannot find that in the textbook'. Always cite the section title."
        )

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3),
           retry=retry_if_exception_type((Exception))) # Catch all for now, refine later
    async def embed_query(self, text: str) -> list[float]:
        """Generates an embedding for the given text using Google Generative AI."""
        # This is a placeholder; actual implementation depends on genai.embed_content specifics
        model = "models/embedding-001" # As specified in the requirements
        response = genai.embed_content(model=model, content=text)
        return response['embedding']

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3),
           retry=retry_if_exception_type((Exception)))
    async def retrieve_context(self, query_embedding: list[float], collection_name: str = "physical_ai_textbook") -> list[SearchResult]:
        """Retrieves relevant context from Qdrant using the query embedding."""
        search_result = self.qdrant_client.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=5
        )
        return [
            SearchResult(
                text=hit.payload["text"],
                source_id=hit.payload["source"],
                title=hit.payload["header"]
            ) for hit in search_result
        ]

    async def generate_answer(self, context: str, user_query: str) -> str:
        """Generates an answer using the OpenAI Agent based on the provided context."""
        prompt = f"Context from textbook:\n{context}\n\nUser Question: {user_query}"
        result = await Runner.run(self.agent, prompt)
        return result.final_output

    async def process_query(self, request: RagRequest) -> RagResponse:
        """Orchestrates the RAG pipeline."""
        try:
            query_embedding = await self.embed_query(request.message)
            context_chunks = await self.retrieve_context(query_embedding)

            if not context_chunks:
                return RagResponse(answer="I cannot find that in the textbook.", sources=[])

            # Prepare context for the LLM
            context_text = "\n\n".join([f"Source: {c.title} ({c.source_id})\n{c.text}" for c in context_chunks])
            sources = sorted(list(set([f"{c.title} ({c.source_id})" for c in context_chunks])))

            answer = await self.generate_answer(context_text, request.message)

            return RagResponse(answer=answer, sources=sources)
        except Exception as e:
            print(f"Error in process_query: {e}")
            # This should be handled by the API endpoint to return 503, not here directly
            raise

"""
RAG Service for processing queries against the Physical AI textbook.
Uses Gemini for embeddings, Qdrant for vector search, and OpenAI for answer generation.
"""

import os
from typing import List
import google.generativeai as genai
from qdrant_client import QdrantClient
from openai import OpenAI
from src.models.rag import RagRequest, RagResponse, SearchResult
from dotenv import load_dotenv

load_dotenv()


class RagService:
    """Service for handling RAG (Retrieval-Augmented Generation) queries."""
    
    def __init__(self):
        """Initialize the RAG service with required clients and configuration."""
        # Load environment variables
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Validate environment variables
        if not all([self.gemini_api_key, self.qdrant_url, self.qdrant_api_key, self.openai_api_key]):
            raise ValueError(
                "Missing required environment variables. Please ensure GEMINI_API_KEY, "
                "QDRANT_URL, QDRANT_API_KEY, and OPENAI_API_KEY are set."
            )
        
        # Initialize clients
        genai.configure(api_key=self.gemini_api_key)
        
        self.qdrant_client = QdrantClient(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key
        )
        
        self.openai_client = OpenAI(api_key=self.openai_api_key)
        
        # Configuration
        self.collection_name = "physical_ai_textbook"
        self.embedding_model = "models/embedding-001"
        self.vector_size = 768
        self.top_k = 10  # Increased for better coverage
        self.similarity_threshold = 0.65  # Minimum similarity score
        
        print(f"[RAG SERVICE] Initialized successfully")
        print(f"  - Collection: {self.collection_name}")
        print(f"  - Embedding model: {self.embedding_model}")
        print(f"  - Top-K retrieval: {self.top_k}")
        print(f"  - Similarity threshold: {self.similarity_threshold}")
    
    async def process_query(self, request: RagRequest) -> RagResponse:
        """
        Process a user query using RAG pipeline.
        
        Args:
            request: RagRequest containing the user's message
            
        Returns:
            RagResponse with answer and sources
        """
        print(f"[RAG SERVICE] Processing query: {request.message[:100]}...")
        
        # Step 1: Generate embedding for the query
        query_embedding = self._generate_query_embedding(request.message)
        print(f"[RAG SERVICE] Generated query embedding (dim: {len(query_embedding)})")
        
        # Step 2: Search for relevant chunks in Qdrant
        search_results = self._search_relevant_chunks(query_embedding)
        print(f"[RAG SERVICE] Found {len(search_results)} relevant chunks")
        
        # Step 3: Generate answer using OpenAI with retrieved context
        if not search_results:
            print("[RAG SERVICE] No relevant chunks found, returning default response")
            return RagResponse(
                answer="I cannot find that in the textbook.",
                sources=[]
            )
        
        answer = self._generate_answer(request.message, search_results)
        sources = self._extract_sources(search_results)
        
        print(f"[RAG SERVICE] Generated answer (length: {len(answer)} chars)")
        print(f"[RAG SERVICE] Extracted {len(sources)} sources")
        
        return RagResponse(answer=answer, sources=sources)
    
    def _generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for a user query using Gemini.
        
        Args:
            query: User's question
            
        Returns:
            List of floats representing the embedding vector
        """
        try:
            response = genai.embed_content(
                model=self.embedding_model,
                content=query,
                task_type="retrieval_query"  # Use for queries
            )
            # Access the embedding from the response dictionary
            return response['embedding']
        except Exception as e:
            print(f"[RAG SERVICE] Error generating embedding: {e}")
            raise
    
    def _search_relevant_chunks(self, query_embedding: List[float]) -> List[SearchResult]:
        """
        Search for relevant chunks in Qdrant using the query embedding.
        
        Args:
            query_embedding: Embedding vector for the query
            
        Returns:
            List of SearchResult objects
        """
        try:
            response = self.qdrant_client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                limit=self.top_k,
                with_payload=True,
                score_threshold=self.similarity_threshold  # Filter by similarity
            )
            
            results = []
            for point in response.points:
                if point.payload:
                    # Log similarity score for debugging
                    score = point.score if hasattr(point, 'score') else 'N/A'
                    print(f"[RAG SERVICE] Retrieved chunk with score: {score}")
                    
                    results.append(SearchResult(
                        text=point.payload.get("content", ""),
                        source_id=point.payload.get("filepath", "Unknown"),
                        title=point.payload.get("heading", "Unknown Section")
                    ))
            
            print(f"[RAG SERVICE] Filtered to {len(results)} chunks above threshold")
            return results
        except Exception as e:
            print(f"[RAG SERVICE] Error searching Qdrant: {e}")
            raise
    
    def _generate_answer(self, query: str, search_results: List[SearchResult]) -> str:
        """
        Generate an answer using OpenAI based on the query and retrieved context.
        
        Args:
            query: User's question
            search_results: List of relevant chunks from the textbook
            
        Returns:
            Generated answer as a string
        """
        # Build context from search results
        context_parts = []
        for i, result in enumerate(search_results, 1):
            context_parts.append(f"[Source {i} - {result.title}]\n{result.text}\n")
        
        context = "\n".join(context_parts)
        
        # Create the prompt with better context
        system_prompt = """You are an expert AI tutor for a Physical AI and Humanoid Robotics textbook. Your goal is to help students understand complex robotics concepts clearly and accurately.

Guidelines:
1. Use the textbook context below as your primary source of truth
2. Provide clear, beginner-friendly explanations with examples when helpful
3. If the context is limited but the question is reasonable, supplement with general robotics/AI knowledge
4. Be conversational and encouraging - you're teaching, not just answering
5. Keep responses concise: 2-3 sentences for definitions, 4-6 sentences for explanations
6. Output ONLY plain text - NO markdown, NO asterisks, NO special formatting
7. If you cannot answer confidently, say "I don't have enough information about that specific topic in the textbook."

Textbook Context (from most to least relevant):
"""
        
        user_prompt = f"""{system_prompt}

{context}

Student Question: {query}

Your Response (plain text, educational tone):"""
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant for a Physical AI and Humanoid Robotics textbook. Always respond in plain text without any markdown formatting."},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[RAG SERVICE] Error generating answer with OpenAI: {e}")
            raise
    
    def _extract_sources(self, search_results: List[SearchResult]) -> List[str]:
        """
        Extract unique source references from search results in a user-friendly format.
        
        Args:
            search_results: List of SearchResult objects
            
        Returns:
            List of unique, user-friendly source strings
        """
        sources = []
        seen = set()
        
        for result in search_results:
            # Use only the section title, not the file path
            # The title already contains the meaningful section name
            source_ref = result.title
            
            if source_ref not in seen and source_ref != "Unknown Section":
                sources.append(source_ref)
                seen.add(source_ref)
        
        return sources
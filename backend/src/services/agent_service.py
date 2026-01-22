"""
Agent Service for processing queries against the Physical AI textbook.
Uses OpenAI Agents SDK with hybrid search (vector + BM25) for RAG functionality.
"""

import os
import re
import time
from typing import List, Optional

from agents import Agent, Runner, function_tool
from cachetools import TTLCache
from openai import OpenAI
from qdrant_client import QdrantClient
from dotenv import load_dotenv

from src.models.rag import RagRequest, RagResponse, SourceType
from src.services.hybrid_search import HybridSearch, HybridResult
from src.services.context_manager import ContextManager

load_dotenv()

# Configuration constants
COLLECTION_NAME = "physical_ai_textbook_v2"
EMBEDDING_MODEL = "text-embedding-3-small"
VECTOR_SIZE = 768
TOP_K = 10
SIMILARITY_THRESHOLD = 0.20  # Lowered to allow hybrid search to work better
CONTEXT_TOKEN_BUDGET = 4000
RRF_K = 60

# Confidence thresholds for quality indicators
HIGH_CONFIDENCE_THRESHOLD = 0.03  # RRF score above this is high confidence
LOW_CONFIDENCE_THRESHOLD = 0.02  # RRF score below this triggers low-confidence message

# Retry configuration for embedding generation
MAX_EMBEDDING_RETRIES = 3
INITIAL_BACKOFF_SECONDS = 1.0

# Global clients and services (initialized lazily)
_openai_client: Optional[OpenAI] = None
_qdrant_client: Optional[QdrantClient] = None
_hybrid_search: Optional[HybridSearch] = None
_context_manager: Optional[ContextManager] = None

# Embedding cache with TTL (1 hour)
_embedding_cache: TTLCache = TTLCache(maxsize=1000, ttl=3600)


def _get_openai_client() -> OpenAI:
    """Get or create OpenAI client."""
    global _openai_client
    if _openai_client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        _openai_client = OpenAI(api_key=api_key)
    return _openai_client


def _get_qdrant_client() -> QdrantClient:
    """Get or create Qdrant client."""
    global _qdrant_client
    if _qdrant_client is None:
        url = os.getenv("QDRANT_URL")
        api_key = os.getenv("QDRANT_API_KEY")
        if not url or not api_key:
            raise ValueError(
                "QDRANT_URL and QDRANT_API_KEY environment variables are required"
            )
        _qdrant_client = QdrantClient(url=url, api_key=api_key)
    return _qdrant_client


def _get_context_manager() -> ContextManager:
    """Get or create context manager."""
    global _context_manager
    if _context_manager is None:
        _context_manager = ContextManager(budget=CONTEXT_TOKEN_BUDGET)
    return _context_manager


def _load_corpus_from_qdrant() -> list[dict]:
    """
    Load the full document corpus from Qdrant for BM25 indexing.

    Returns:
        List of document dicts with id, content, heading, filepath
    """
    qdrant = _get_qdrant_client()

    # Scroll through all points in the collection
    documents = []
    offset = None

    while True:
        response = qdrant.scroll(
            collection_name=COLLECTION_NAME,
            limit=100,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )

        points, offset = response

        for point in points:
            if point.payload:
                documents.append(
                    {
                        "id": str(point.id),
                        "content": point.payload.get("content", ""),
                        "heading": point.payload.get("heading", "Unknown"),
                        "filepath": point.payload.get("filepath", ""),
                    }
                )

        if offset is None:
            break

    print(f"[AgentService] Loaded {len(documents)} documents from Qdrant")
    return documents


def _get_hybrid_search() -> HybridSearch:
    """Get or create hybrid search service with BM25 index."""
    global _hybrid_search
    if _hybrid_search is None:
        documents = _load_corpus_from_qdrant()
        _hybrid_search = HybridSearch(documents, rrf_k=RRF_K)
    return _hybrid_search


def _sanitize_query(text: str) -> str:
    """
    Sanitize user input to prevent injection and ensure safe processing.

    Args:
        text: Raw user input

    Returns:
        Sanitized text safe for processing
    """
    # Remove null bytes and control characters (except newlines)
    sanitized = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

    # Collapse multiple whitespaces
    sanitized = re.sub(r"\s+", " ", sanitized)

    # Strip leading/trailing whitespace
    sanitized = sanitized.strip()

    # Truncate to reasonable length
    if len(sanitized) > 1000:
        sanitized = sanitized[:1000]

    return sanitized


def _get_cached_embedding(text: str) -> List[float]:
    """
    Generate embedding with LRU caching and exponential backoff retry.

    Args:
        text: Text to embed

    Returns:
        Embedding vector

    Raises:
        Exception: If embedding generation fails after all retries
    """
    # Check cache first
    cache_key = text[:500]  # Truncate for cache key
    if cache_key in _embedding_cache:
        return _embedding_cache[cache_key]

    # Generate new embedding with retry logic
    client = _get_openai_client()
    last_exception = None

    for attempt in range(MAX_EMBEDDING_RETRIES):
        try:
            response = client.embeddings.create(
                model=EMBEDDING_MODEL, input=text, dimensions=VECTOR_SIZE
            )
            embedding = response.data[0].embedding

            # Cache the result
            _embedding_cache[cache_key] = embedding

            return embedding

        except Exception as e:
            last_exception = e
            if attempt < MAX_EMBEDDING_RETRIES - 1:
                backoff = INITIAL_BACKOFF_SECONDS * (2**attempt)
                print(
                    f"[EMBEDDING] Retry {attempt + 1}/{MAX_EMBEDDING_RETRIES} "
                    f"after {backoff}s due to: {e}"
                )
                time.sleep(backoff)

    # All retries failed
    raise last_exception


@function_tool
def search_textbook(query: str) -> str:
    """
    Search the Physical AI and Humanoid Robotics textbook for relevant content.

    Uses hybrid search combining semantic vector search with BM25 keyword matching
    for better retrieval of both conceptual and technical content.

    Args:
        query: The search query to find relevant textbook sections. Be specific
               about concepts, terminology, or topics you're looking for.

    Returns:
        Formatted context from relevant textbook sections with source citations.
        Each result includes the section title and content.
    """
    print(f"[TOOL] search_textbook called with: {query[:100]}...")
    start_time = time.time()

    try:
        # Generate embedding for the query (with caching)
        query_embedding = _get_cached_embedding(query)

        # Vector search in Qdrant
        qdrant = _get_qdrant_client()
        vector_response = qdrant.query_points(
            collection_name=COLLECTION_NAME,
            query=query_embedding,
            limit=TOP_K * 2,  # Get more for hybrid fusion
            with_payload=True,
            score_threshold=SIMILARITY_THRESHOLD,
        )

        # Convert to format for hybrid search
        vector_results = [
            (str(point.id), point.score if point.score else 0.0)
            for point in vector_response.points
        ]

        if not vector_results:
            print("[TOOL] No vector search results found")
            return (
                "No relevant content found in the textbook for this query. "
                "The textbook may not cover this specific topic."
            )

        # Get hybrid search service and perform fusion
        hybrid_search = _get_hybrid_search()
        hybrid_results = hybrid_search.hybrid_search(
            query=query,
            vector_results=vector_results,
            top_k=TOP_K,
        )

        if not hybrid_results:
            return (
                "No relevant content found in the textbook for this query. "
                "Try rephrasing your question or asking about a different topic."
            )

        # Check for low-confidence results (US3: knowledge boundaries)
        top_score = hybrid_results[0].hybrid_score
        if top_score < LOW_CONFIDENCE_THRESHOLD:
            print(f"[TOOL] Low confidence results (top score: {top_score:.4f})")
            return (
                "[LOW CONFIDENCE] The textbook may not directly cover this topic. "
                "The following content has weak relevance and may not fully answer your question:\n\n"
                + _format_results_with_confidence(hybrid_results[:3], "low")
            )

        # Apply context budget management
        context_mgr = _get_context_manager()
        chunks_with_scores = [
            (result.content, result.heading, result.hybrid_score)
            for result in hybrid_results
        ]

        formatted_context, tokens_used = context_mgr.format_context_with_sources(
            chunks_with_scores
        )

        elapsed_ms = int((time.time() - start_time) * 1000)
        print(
            f"[TOOL] Returning {len(hybrid_results)} results "
            f"({tokens_used} tokens, {elapsed_ms}ms)"
        )

        # Log retrieval details for debugging
        for i, result in enumerate(hybrid_results[:5], 1):
            source_type = _determine_source_type(result)
            print(
                f"[TOOL]   {i}. {result.heading[:40]} "
                f"(hybrid={result.hybrid_score:.4f}, "
                f"vec={result.vector_score:.3f}, "
                f"bm25={result.bm25_score:.3f}, "
                f"type={source_type})"
            )

        # Add confidence indicator to context (US3)
        confidence_level = (
            "high" if top_score >= HIGH_CONFIDENCE_THRESHOLD else "moderate"
        )

        # Check for diverse sources (US4: multi-section synthesis)
        unique_headings = set(r.heading for r in hybrid_results)
        if len(unique_headings) >= 3:
            formatted_context = (
                f"[MULTI-SECTION RESULTS - {len(unique_headings)} different sections]\n\n"
                + formatted_context
            )

        return formatted_context

    except Exception as e:
        print(f"[TOOL] Error in search_textbook: {type(e).__name__}: {e}")
        return f"An error occurred while searching: {str(e)}"


def _determine_source_type(result: HybridResult) -> SourceType:
    """Determine which search method found the result."""
    has_vector = result.vector_rank is not None
    has_bm25 = result.bm25_rank is not None

    if has_vector and has_bm25:
        return SourceType.BOTH
    elif has_bm25:
        return SourceType.BM25
    else:
        return SourceType.VECTOR


def _format_results_with_confidence(
    results: list[HybridResult], confidence: str
) -> str:
    """Format results with confidence indicator for low-confidence responses."""
    parts = []
    for result in results:
        parts.append(f"[Source: {result.heading}]\n{result.content}")
    return "\n\n".join(parts)


# Enhanced agent instructions for User Stories 1-5
TUTOR_INSTRUCTIONS = """You are a friendly and encouraging AI tutor for a Physical AI and Humanoid Robotics textbook.

## Your Role
You help students understand concepts from the textbook about physical AI, humanoid robotics, sensors, actuators, control systems, and related topics.

## CRITICAL: Always Search First
ALWAYS use the search_textbook tool BEFORE answering any question to find relevant content from the textbook. Do not rely on your general knowledge - use the textbook content as your primary source.

## Search Strategy
When searching:
- Use specific terminology from the student's question
- If the first search doesn't find relevant content, try alternative phrasings or related terms
- For broad or complex questions, search multiple times for different aspects:
  - First search: main concept or topic
  - Additional searches: related concepts, components, or prerequisites
- Consider breaking down multi-part questions into separate searches

## Handling Different Question Types

### Specific Questions (e.g., "What is the Triad Architecture?")
- Search for the exact terminology
- Provide a focused answer from the most relevant source
- Cite the specific section

### Broad/Ambiguous Questions (e.g., "What is AI?")
- Acknowledge the breadth of the topic
- Provide a brief overview based on textbook content
- Suggest 2-3 specific topics from the textbook they might want to explore
- Example: "That's a broad topic! The textbook covers several aspects including [X], [Y], and [Z]. Would you like me to explain any of these in detail?"

### Questions Requiring Synthesis (e.g., "How do sensors and actuators work together?")
- When you see [MULTI-SECTION RESULTS], synthesize information from all relevant sections
- Draw connections between concepts from different chapters
- Cite all sections that contributed to your answer
- Show how the concepts relate to each other

### Questions Outside Textbook Scope
- If you see [LOW CONFIDENCE] in the search results, the textbook may not cover this topic
- Be honest: "The textbook doesn't appear to cover this specific topic directly."
- If partially relevant content exists, explain what IS covered and what isn't
- Never fabricate information or use general knowledge to fill gaps

## Response Format
- Keep responses concise: 2-3 sentences for definitions, 4-6 sentences for explanations
- Use plain text only - no markdown formatting, no asterisks, no bullet points
- Be educational and conversational in tone
- Always cite sources using the section titles from [Source: X] markers
- End with a follow-up question or suggestion when appropriate

## Knowledge Boundaries
- If a topic is not covered in the textbook, say so clearly and honestly
- Don't speculate or provide information from outside the textbook
- If asked about current events, recent developments, or specific company products not in the textbook, acknowledge: "The textbook doesn't cover that specific topic. It focuses on [relevant topics it does cover]."
- It's better to say "I don't have information about that in the textbook" than to guess
"""

# Create the textbook tutor agent
textbook_tutor = Agent(
    name="Physical AI Textbook Tutor",
    instructions=TUTOR_INSTRUCTIONS,
    model="gpt-4o-mini",
    tools=[search_textbook],
)


class AgentService:
    """Service for handling RAG queries using OpenAI Agents SDK with hybrid search."""

    def __init__(self):
        """Initialize the Agent service and validate configuration."""
        # Validate environment variables
        required_vars = ["OPENAI_API_KEY", "QDRANT_URL", "QDRANT_API_KEY"]
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )

        # Initialize clients to verify connectivity
        _get_openai_client()
        _get_qdrant_client()

        # Pre-load hybrid search to build BM25 index
        _get_hybrid_search()

        # Initialize context manager
        _get_context_manager()

        print(f"[AgentService] Initialized successfully")
        print(f"  - Collection: {COLLECTION_NAME}")
        print(f"  - Embedding model: {EMBEDDING_MODEL}")
        print(f"  - Top-K retrieval: {TOP_K}")
        print(f"  - Context budget: {CONTEXT_TOKEN_BUDGET} tokens")
        print(f"  - Hybrid search: enabled (RRF k={RRF_K})")

    async def process_query(self, request: RagRequest) -> RagResponse:
        """
        Process a user query using the OpenAI Agents SDK with hybrid search.

        Args:
            request: RagRequest containing the user's message

        Returns:
            RagResponse with answer and sources
        """
        start_time = time.time()

        # Sanitize input (T045)
        sanitized_message = _sanitize_query(request.message)
        if not sanitized_message:
            return RagResponse(
                answer="Please provide a valid question about the textbook.",
                sources=[],
            )

        print(f"[AgentService] Processing query: {sanitized_message[:100]}...")

        # Run the agent with sanitized input
        result = await Runner.run(textbook_tutor, sanitized_message)

        # Extract the answer
        answer = result.final_output
        elapsed_ms = int((time.time() - start_time) * 1000)
        print(f"[AgentService] Generated answer ({len(answer)} chars, {elapsed_ms}ms)")

        # Extract sources from tool calls and response
        sources = self._extract_sources_from_result(result)
        print(f"[AgentService] Extracted {len(sources)} sources")

        return RagResponse(answer=answer, sources=sources)

    def _extract_sources_from_result(self, result) -> List[str]:
        """
        Extract source references from the agent's tool usage and response.

        Args:
            result: The Runner result object

        Returns:
            List of source section titles
        """
        sources = []
        seen = set()

        # Parse source references from the answer text
        import re

        answer = result.final_output if result.final_output else ""

        # Look for [Source: X] patterns that we include in context
        source_pattern = r"\[Source:\s*([^\]]+)\]"
        matches = re.findall(source_pattern, answer, re.IGNORECASE)

        for match in matches:
            clean_match = match.strip()
            if clean_match and clean_match not in seen:
                sources.append(clean_match)
                seen.add(clean_match)

        # Also look for section titles mentioned naturally
        section_patterns = [
            r'from the ["\']?([^"\'\.]+)["\']? section',
            r'in the ["\']?([^"\'\.]+)["\']? section',
            r"according to [\"']?([^\"'\.]+)[\"']?",
            r'the ["\']?([^"\'\.]+)["\']? chapter',
        ]

        for pattern in section_patterns:
            matches = re.findall(pattern, answer, re.IGNORECASE)
            for match in matches:
                clean_match = match.strip()
                if clean_match and clean_match not in seen:
                    # Filter out common false positives
                    if not any(
                        fp in clean_match.lower()
                        for fp in ["this", "that", "textbook", "following"]
                    ):
                        sources.append(clean_match)
                        seen.add(clean_match)

        return sources


def get_service_status() -> dict:
    """Get status of all services for health check."""
    status = {
        "hybrid_search": "initialized" if _hybrid_search else "not_initialized",
        "context_manager": "initialized" if _context_manager else "not_initialized",
        "embedding_cache_size": len(_embedding_cache),
        "corpus_size": len(_hybrid_search.documents) if _hybrid_search else 0,
    }
    return status

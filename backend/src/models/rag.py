from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime


class SourceType(str, Enum):
    """Indicates which search method found the result."""

    VECTOR = "vector"
    BM25 = "bm25"
    BOTH = "both"


class RagRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)


class RagResponse(BaseModel):
    answer: str
    sources: List[str]


class SearchResult(BaseModel):
    """A ranked retrieval result from hybrid search."""

    chunk_id: str
    content: str
    heading: str
    vector_score: float = 0.0
    bm25_score: float = 0.0
    hybrid_score: float = 0.0
    source_type: SourceType = SourceType.VECTOR


class TextbookChunk(BaseModel):
    """A semantic unit of textbook content stored in Qdrant."""

    id: str
    content: str
    filepath: str
    heading: str
    position: int = 0
    parent_heading: Optional[str] = None
    token_count: int = 0


class StudentQuery(BaseModel):
    """A question submitted by a student through the chat interface."""

    raw_text: str = Field(..., max_length=1000)
    sanitized_text: str
    embedding: Optional[List[float]] = None
    expanded_queries: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AgentResponse(BaseModel):
    """The tutor agent's response to a student query."""

    answer: str
    sources: List[str] = Field(default_factory=list)
    tool_calls: List[dict] = Field(default_factory=list)
    latency_ms: int = 0
    tokens_used: int = 0

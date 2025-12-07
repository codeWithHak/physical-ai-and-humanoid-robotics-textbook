from pydantic import BaseModel, Field
from typing import List

class RagRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)

class RagResponse(BaseModel):
    answer: str
    sources: List[str]

class SearchResult(BaseModel):
    text: str
    source_id: str
    title: str

from fastapi import APIRouter, HTTPException, status
from src.models.rag import RagRequest, RagResponse
from src.services.rag_service import RagService
from google.api_core.exceptions import GoogleAPIError
from qdrant_client.http.exceptions import UnexpectedResponse

chat_router = APIRouter()
rag_service = RagService()

@chat_router.post("/chat", response_model=RagResponse, status_code=status.HTTP_200_OK)
async def chat(request: RagRequest):
    """
    Processes a natural language query against the textbook using RAG.
    """
    try:
        response = await rag_service.process_query(request)
        return response
    except (GoogleAPIError, UnexpectedResponse, ValueError) as e:
        # Catch specific upstream errors and return a 503
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"An upstream service is unavailable or returned an error: {e}"
        )
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}"
        )

from fastapi import APIRouter, HTTPException, status
from src.models.rag import RagRequest, RagResponse
from src.services.rag_service import RagService
from google.api_core.exceptions import GoogleAPIError
from qdrant_client.http.exceptions import UnexpectedResponse
from openai import OpenAIError
import traceback

chat_router = APIRouter()

# Initialize service with error handling
try:
    rag_service = RagService()
    print("✓ RagService initialized successfully")
except Exception as e:
    print(f"✗ Failed to initialize RagService: {e}")
    raise


@chat_router.post("/chat", response_model=RagResponse, status_code=status.HTTP_200_OK)
async def chat(request: RagRequest):
    """
    Processes a natural language query against the textbook using RAG.
    
    Args:
        request: RagRequest containing the user's message
        
    Returns:
        RagResponse with answer and sources
        
    Raises:
        HTTPException: 503 for upstream service errors, 500 for unexpected errors
    """
    try:
        print(f"\n[CHAT ENDPOINT] Received request: {request.message[:100]}...")
        response = await rag_service.process_query(request)
        print(f"[CHAT ENDPOINT] Successfully processed request")
        return response
        
    except GoogleAPIError as e:
        # Google Gemini API errors (embedding)
        print(f"[CHAT ENDPOINT] Google API Error: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Google Gemini API error: {str(e)}"
        )
        
    except UnexpectedResponse as e:
        # Qdrant API errors (vector search)
        print(f"[CHAT ENDPOINT] Qdrant Error: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Qdrant vector database error: {str(e)}"
        )
        
    except OpenAIError as e:
        # OpenAI API errors (answer generation)
        print(f"[CHAT ENDPOINT] OpenAI Error: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"OpenAI API error: {str(e)}"
        )
        
    except ValueError as e:
        # Configuration or validation errors
        print(f"[CHAT ENDPOINT] ValueError: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request: {str(e)}"
        )
        
    except AttributeError as e:
        # Likely the embedding access issue
        print(f"[CHAT ENDPOINT] AttributeError: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal service error (AttributeError): {str(e)}. Please check server logs."
        )
        
    except Exception as e:
        # Catch any other unexpected errors
        print(f"[CHAT ENDPOINT] Unexpected Error: {type(e).__name__}: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {type(e).__name__}: {str(e)}"
        )


@chat_router.get("/health")
async def health_check():
    """
    Health check endpoint to verify the service is running.
    
    Returns:
        dict: Service status and configuration info
    """
    try:
        # Test basic connectivity
        import google.generativeai as genai
        from qdrant_client import QdrantClient
        
        health_status = {
            "status": "healthy",
            "service": "RAG Service",
            "checks": {}
        }
        
        # Check if clients are initialized
        if rag_service.qdrant_client:
            health_status["checks"]["qdrant"] = "connected"
        else:
            health_status["checks"]["qdrant"] = "not initialized"
            
        if rag_service.openai_client:
            health_status["checks"]["openai"] = "connected"
        else:
            health_status["checks"]["openai"] = "not initialized"
            
        # Check environment variables
        health_status["checks"]["env_vars"] = "configured" if all([
            rag_service.gemini_api_key,
            rag_service.qdrant_url,
            rag_service.qdrant_api_key,
            rag_service.openai_api_key
        ]) else "missing"
        
        return health_status
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
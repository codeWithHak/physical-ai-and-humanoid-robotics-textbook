from fastapi import APIRouter, HTTPException, status
from src.models.rag import RagRequest, RagResponse
from src.services.agent_service import AgentService, get_service_status
from qdrant_client.http.exceptions import UnexpectedResponse
from openai import OpenAIError
import traceback
import time

chat_router = APIRouter()

# Simple in-memory rate limiting (for production, use Redis or similar)
_rate_limit_window = 60  # seconds
_max_requests_per_window = 50  # requests per IP per window
_request_counts: dict[str, list[float]] = {}


def _check_rate_limit(client_ip: str) -> bool:
    """
    Simple rate limiting check. Returns True if request is allowed.
    For production, replace with Redis-based rate limiting.
    """
    now = time.time()
    window_start = now - _rate_limit_window

    # Get or create request history for this IP
    if client_ip not in _request_counts:
        _request_counts[client_ip] = []

    # Filter to requests within window
    _request_counts[client_ip] = [
        ts for ts in _request_counts[client_ip] if ts > window_start
    ]

    # Check limit
    if len(_request_counts[client_ip]) >= _max_requests_per_window:
        return False

    # Record this request
    _request_counts[client_ip].append(now)
    return True


# Initialize service with error handling
try:
    agent_service = AgentService()
    print("✓ AgentService initialized successfully")
except Exception as e:
    print(f"✗ Failed to initialize AgentService: {e}")
    raise


@chat_router.post("/chat", response_model=RagResponse, status_code=status.HTTP_200_OK)
async def chat(request: RagRequest, client_ip: str = "unknown"):
    """
    Processes a natural language query against the textbook using RAG.

    Args:
        request: RagRequest containing the user's message
        client_ip: Client IP for rate limiting (extracted by middleware in production)

    Returns:
        RagResponse with answer and sources

    Raises:
        HTTPException: 429 for rate limit exceeded, 503 for upstream service errors, 500 for unexpected errors
    """
    try:
        # Rate limiting check (T046)
        if not _check_rate_limit(client_ip):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please wait before making more requests.",
            )

        print(f"\n[CHAT ENDPOINT] Received request: {request.message[:100]}...")
        response = await agent_service.process_query(request)
        print(f"[CHAT ENDPOINT] Successfully processed request")
        return response

    except UnexpectedResponse as e:
        # Qdrant API errors (vector search)
        print(f"[CHAT ENDPOINT] Qdrant Error: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Qdrant vector database error: {str(e)}",
        )

    except OpenAIError as e:
        # OpenAI API errors (embeddings and agent)
        print(f"[CHAT ENDPOINT] OpenAI Error: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"OpenAI API error: {str(e)}",
        )

    except ValueError as e:
        # Configuration or validation errors
        print(f"[CHAT ENDPOINT] ValueError: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request: {str(e)}",
        )

    except Exception as e:
        # Catch any other unexpected errors
        print(f"[CHAT ENDPOINT] Unexpected Error: {type(e).__name__}: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {type(e).__name__}: {str(e)}",
        )


@chat_router.get("/health")
async def health_check():
    """
    Health check endpoint to verify the service is running.

    Returns:
        dict: Service status and configuration info including hybrid search status
    """
    try:
        import os

        health_status = {
            "status": "healthy",
            "service": "Agent Service (OpenAI with Hybrid Search)",
            "checks": {},
            "services": {},
        }

        # Check environment variables
        health_status["checks"]["openai"] = (
            "configured" if os.getenv("OPENAI_API_KEY") else "missing"
        )
        health_status["checks"]["qdrant_url"] = (
            "configured" if os.getenv("QDRANT_URL") else "missing"
        )
        health_status["checks"]["qdrant_api_key"] = (
            "configured" if os.getenv("QDRANT_API_KEY") else "missing"
        )

        # Get service status (T049)
        try:
            service_status = get_service_status()
            health_status["services"] = service_status

            # Check if all services are initialized
            if service_status.get("hybrid_search") != "initialized":
                health_status["status"] = "degraded"
                health_status["warning"] = "Hybrid search not initialized"
            if service_status.get("context_manager") != "initialized":
                health_status["status"] = "degraded"
                health_status["warning"] = "Context manager not initialized"

        except Exception as e:
            health_status["services"]["error"] = str(e)
            health_status["status"] = "degraded"

        return health_status

    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

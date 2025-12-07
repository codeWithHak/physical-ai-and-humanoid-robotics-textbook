import logging
from fastapi import APIRouter

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/")
async def read_root():
    logger.info("GET / endpoint accessed")
    return {"status": "Physical AI API Ready"}

@router.get("/health")
async def health_check():
    logger.info("GET /health endpoint accessed")
    return {"status": "OK"}

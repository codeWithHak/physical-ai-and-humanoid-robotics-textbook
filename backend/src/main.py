import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.chat import chat_router # Import chat_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://physical-ai-and-humanoid-robotics-h.vercel.app",
    "https://frontend-coq6lfeib-huzairs-projects-272a3e04.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api") # Include chat_router with prefix

@app.get("/")
async def read_root():
    logger.info("GET / endpoint accessed")
    return {"status": "Physical AI API Ready"}

@app.get("/health")
async def health_check():
    logger.info("GET /health endpoint accessed")
    return {"status": "OK"}
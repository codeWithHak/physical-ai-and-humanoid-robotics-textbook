import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://physical-ai-and-humanoid-robotics-h.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    logger.info("GET / endpoint accessed")
    return {"status": "Physical AI API Ready"}

@app.get("/health")
async def health_check():
    logger.info("GET /health endpoint accessed")
    return {"status": "OK"}
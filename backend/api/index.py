import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configure basic logging for local development (FR-009)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI() # T005

# T006: Implement CORS Middleware
origins = [
    "http://localhost:3000", # Development frontend
    "https://physical-ai-and-humanoid-robotics-h.vercel.app", # Production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# T007: Implement GET / endpoint
@app.get("/")
async def read_root():
    logger.info("GET / endpoint accessed")
    return {"status": "Physical AI API Ready"}

# T008: Implement GET /health endpoint
@app.get("/health")
async def health_check():
    logger.info("GET /health endpoint accessed")
    return {"status": "OK"}
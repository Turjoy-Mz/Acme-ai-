"""FastAPI application factory and main entry point."""
from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from app.config import API_TITLE, API_VERSION, HOST, PORT
from app.middleware import log_requests, api_key_middleware
from app.models import HealthCheckResponse
from app.routers import ingest, retrieve, generate
from app.services.faiss_service import FAISSService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize services
faiss_service = FAISSService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    logger.info("Healthcare RAG Assistant starting up...")
    logger.info(f"FAISS index ready with {faiss_service.get_documents_count()} documents")
    yield
    logger.info("Healthcare RAG Assistant shutting down...")

# Create FastAPI app
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description="Healthcare Knowledge Assistant powered by RAG (Retrieval-Augmented Generation)",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.middleware("http")(log_requests)
app.middleware("http")(api_key_middleware)

# Include routers
app.include_router(ingest.router)
app.include_router(retrieve.router)
app.include_router(generate.router)

@app.get("/", tags=["health"])
async def root():
    """Root endpoint."""
    return {
        "message": "Healthcare RAG Assistant API",
        "version": API_VERSION,
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthCheckResponse, tags=["health"])
async def health_check():
    """Health check endpoint."""
    return HealthCheckResponse(
        status="healthy",
        version=API_VERSION,
        faiss_ready=faiss_service.index.ntotal > 0,
        documents_indexed=faiss_service.get_documents_count()
    )

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on {HOST}:{PORT}")
    uvicorn.run(
        "app.main:app",
        host=HOST,
        port=PORT,
        reload=False,
        log_level="info"
    )

"""Pydantic models for request/response validation."""
from typing import Optional
from pydantic import BaseModel, Field

class IngestRequest(BaseModel):
    """Request model for document ingestion."""
    filename: str = Field(..., description="Name of the document")
    content: str = Field(..., description="Document content in txt format")
    language: Optional[str] = Field("en", description="Document language (en/ja)")

class IngestResponse(BaseModel):
    """Response model for document ingestion."""
    success: bool
    message: str
    document_id: Optional[str] = None
    chunks_created: Optional[int] = None

class RetrieveRequest(BaseModel):
    """Request model for document retrieval."""
    query: str = Field(..., description="Search query")
    language: Optional[str] = Field("en", description="Query language (en/ja)")
    top_k: Optional[int] = Field(3, description="Number of results to return")

class Document(BaseModel):
    """Model for a retrieved document."""
    doc_id: str
    content: str
    similarity_score: float
    source_language: str

class RetrieveResponse(BaseModel):
    """Response model for document retrieval."""
    success: bool
    query: str
    query_language: str
    results: list[Document]
    total_results: int

class GenerateRequest(BaseModel):
    """Request model for LLM response generation."""
    query: str = Field(..., description="Medical question/query")
    language: Optional[str] = Field("en", description="Query language (en/ja)")
    output_language: Optional[str] = Field(None, description="Output language (if different from query)")
    include_sources: Optional[bool] = Field(True, description="Include source documents in response")

class GenerateResponse(BaseModel):
    """Response model for LLM generation."""
    success: bool
    query: str
    response: str
    output_language: str
    source_documents: list[Document]
    sources_used: int

class HealthCheckResponse(BaseModel):
    """Response model for health check."""
    status: str
    version: str
    faiss_ready: bool
    documents_indexed: int

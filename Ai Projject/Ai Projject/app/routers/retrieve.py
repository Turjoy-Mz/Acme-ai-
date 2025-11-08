"""Document retrieval router."""
from fastapi import APIRouter, HTTPException, status
from app.models import RetrieveRequest, RetrieveResponse, Document
from app.services.faiss_service import FAISSService
from app.services.language_detector import LanguageDetector
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/retrieve", tags=["retrieval"])
faiss_service = FAISSService()
lang_detector = LanguageDetector()

@router.post("", response_model=RetrieveResponse)
async def retrieve_documents(request: RetrieveRequest):
    """
    Retrieve relevant medical documents.
    
    - **query**: Medical question or search query
    - **language**: Query language (en/ja, auto-detected if not provided)
    - **top_k**: Number of results to return (default: 3)
    """
    try:
        # Validate query
        if not request.query or len(request.query.strip()) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Query must be at least 3 characters"
            )
        
        # Detect language if not provided
        language = request.language or lang_detector.detect(request.query)
        
        # Retrieve documents
        results = faiss_service.retrieve_documents(
            query=request.query,
            top_k=request.top_k or 3
        )
        
        if not results:
            return RetrieveResponse(
                success=True,
                query=request.query,
                query_language=language,
                results=[],
                total_results=0
            )
        
        # Convert to Document models
        documents = [
            Document(
                doc_id=r["doc_id"],
                content=r["content"],
                similarity_score=round(r["similarity_score"], 4),
                source_language=r["source_language"]
            )
            for r in results
        ]
        
        return RetrieveResponse(
            success=True,
            query=request.query,
            query_language=language,
            results=documents,
            total_results=len(documents)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in retrieve endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving documents: {str(e)}"
        )

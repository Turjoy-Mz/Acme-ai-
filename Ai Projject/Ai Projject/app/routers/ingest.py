"""Document ingestion router."""
from fastapi import APIRouter, HTTPException, status
from app.models import IngestRequest, IngestResponse
from app.services.faiss_service import FAISSService
from app.services.language_detector import LanguageDetector
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ingest", tags=["ingestion"])
faiss_service = FAISSService()
lang_detector = LanguageDetector()

@router.post("", response_model=IngestResponse)
async def ingest_document(request: IngestRequest):
    """
    Ingest a medical document.
    
    - **filename**: Name of the document
    - **content**: Document content (text format)
    - **language**: Document language (en/ja, auto-detected if not provided)
    """
    try:
        # Validate content
        if not request.content or len(request.content.strip()) < 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Document content must be at least 50 characters"
            )
        
        # Detect language if not provided
        language = request.language or lang_detector.detect(request.content)
        
        # Ingest document
        success, message, chunks = faiss_service.ingest_document(
            content=request.content,
            filename=request.filename,
            language=language
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        return IngestResponse(
            success=True,
            message=message,
            document_id=request.filename,
            chunks_created=chunks
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in ingest endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error ingesting document: {str(e)}"
        )

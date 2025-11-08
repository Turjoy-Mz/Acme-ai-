"""LLM response generation router."""
from fastapi import APIRouter, HTTPException, status
from app.models import GenerateRequest, GenerateResponse, Document
from app.services.faiss_service import FAISSService
from app.services.language_detector import LanguageDetector
from app.services.translator import Translator
from app.services.llm_service import MockLLMService
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/generate", tags=["generation"])
faiss_service = FAISSService()
lang_detector = LanguageDetector()
translator = Translator()

@router.post("", response_model=GenerateResponse)
async def generate_response(request: GenerateRequest):
    """
    Generate a medical assistant response using RAG.
    
    - **query**: Medical question or query
    - **language**: Query language (en/ja, auto-detected if not provided)
    - **output_language**: Optional output language (defaults to query language)
    - **include_sources**: Include source documents in response
    """
    try:
        # Validate query
        if not request.query or len(request.query.strip()) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Query must be at least 3 characters"
            )
        
        # Detect query language
        query_language = request.language or lang_detector.detect(request.query)
        
        # Determine output language
        output_language = request.output_language or query_language
        
        # Retrieve relevant documents
        retrieved_docs = faiss_service.retrieve_documents(query=request.query, top_k=3)
        
        # Translate query to LLM's preferred language if needed
        llm_query = request.query
        if query_language == "ja":
            llm_query = translator.translate(request.query, "ja", "en")
        
        # Generate response
        response_text = MockLLMService.generate_response(
            query=llm_query,
            retrieved_documents=retrieved_docs,
            language=output_language
        )
        
        # Translate response if output language differs from query language
        if output_language != query_language:
            response_text = translator.translate(
                response_text,
                query_language,
                output_language
            )
        
        # Prepare documents for response
        source_documents = [
            Document(
                doc_id=doc["doc_id"],
                content=doc["content"][:200],  # Truncate for response
                similarity_score=round(doc["similarity_score"], 4),
                source_language=doc["source_language"]
            )
            for doc in retrieved_docs
        ] if request.include_sources else []
        
        return GenerateResponse(
            success=True,
            query=request.query,
            response=response_text,
            output_language=output_language,
            source_documents=source_documents,
            sources_used=len(retrieved_docs)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in generate endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating response: {str(e)}"
        )

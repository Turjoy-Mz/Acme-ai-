"""FAISS vector database service for semantic search."""
import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer
from pathlib import Path
import logging
from typing import List, Tuple, Dict, Any
from app.config import (
    FAISS_INDEX_PATH, FAISS_METADATA_PATH, EMBEDDING_MODEL,
    FAISS_DIMENSION, CHUNK_SIZE
)
from app.utils.helpers import (
    chunk_text, save_metadata, load_metadata, generate_document_id
)

logger = logging.getLogger(__name__)

class FAISSService:
    """Service for managing FAISS vector index."""
    
    def __init__(self):
        """Initialize FAISS service with embeddings model."""
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.index = self._load_or_create_index()
        self.metadata = load_metadata(FAISS_METADATA_PATH)
    
    def _load_or_create_index(self) -> faiss.IndexFlatL2:
        """Load existing FAISS index or create new one."""
        if FAISS_INDEX_PATH.exists():
            try:
                logger.info(f"Loading FAISS index from {FAISS_INDEX_PATH}")
                index = faiss.read_index(str(FAISS_INDEX_PATH))
                return index
            except Exception as e:
                logger.error(f"Error loading index: {e}, creating new index")
        
        logger.info("Creating new FAISS index")
        return faiss.IndexFlatL2(FAISS_DIMENSION)
    
    def ingest_document(self, content: str, filename: str, language: str = "en") -> Tuple[bool, str, int]:
        """
        Ingest a document into FAISS index.
        
        Args:
            content: Document content
            filename: Document filename
            language: Document language
        
        Returns:
            Tuple of (success, message, chunks_created)
        """
        try:
            # Chunk the document
            chunks = chunk_text(content, chunk_size=CHUNK_SIZE)
            
            if not chunks:
                return False, "Document too small or empty", 0
            
            # Generate embeddings for all chunks
            embeddings = self.model.encode(chunks, show_progress_bar=False)
            embeddings = np.array(embeddings).astype('float32')
            
            # Add to FAISS index
            initial_size = self.index.ntotal
            self.index.add(embeddings)
            
            # Save metadata for each chunk
            for i, chunk in enumerate(chunks):
                doc_id = generate_document_id(filename, i)
                self.metadata[doc_id] = {
                    "filename": filename,
                    "chunk_index": i,
                    "content": chunk,
                    "language": language,
                    "faiss_index": initial_size + i
                }
            
            # Persist index and metadata
            self._save_index()
            save_metadata(self.metadata, FAISS_METADATA_PATH)
            
            message = f"Successfully ingested {len(chunks)} chunks from {filename}"
            logger.info(message)
            return True, message, len(chunks)
        
        except Exception as e:
            error_msg = f"Error ingesting document: {str(e)}"
            logger.error(error_msg)
            return False, error_msg, 0
    
    def retrieve_documents(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve top-k similar documents for a query.
        
        Args:
            query: Search query
            top_k: Number of results to return
        
        Returns:
            List of retrieved documents with similarity scores
        """
        if self.index.ntotal == 0:
            logger.warning("FAISS index is empty")
            return []
        
        try:
            # Generate embedding for query
            query_embedding = self.model.encode([query], show_progress_bar=False)
            query_embedding = np.array(query_embedding).astype('float32')
            
            # Search in FAISS
            distances, indices = self.index.search(query_embedding, top_k)
            
            results = []
            for distance, idx in zip(distances[0], indices):
                # Find metadata for this index
                metadata_entry = None
                for doc_id, meta in self.metadata.items():
                    if meta["faiss_index"] == int(idx):
                        metadata_entry = meta
                        break
                
                if metadata_entry:
                    # Convert L2 distance to similarity score (0-1)
                    similarity = 1 / (1 + float(distance))
                    results.append({
                        "doc_id": doc_id,
                        "content": metadata_entry["content"],
                        "similarity_score": similarity,
                        "source_language": metadata_entry["language"],
                        "filename": metadata_entry["filename"]
                    })
            
            return results
        
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            return []
    
    def get_documents_count(self) -> int:
        """Get total number of indexed documents."""
        return len(self.metadata)
    
    def _save_index(self):
        """Save FAISS index to disk."""
        try:
            FAISS_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
            faiss.write_index(self.index, str(FAISS_INDEX_PATH))
            logger.info(f"FAISS index saved to {FAISS_INDEX_PATH}")
        except Exception as e:
            logger.error(f"Error saving FAISS index: {e}")
    
    def clear_index(self):
        """Clear the FAISS index and metadata."""
        self.index = faiss.IndexFlatL2(FAISS_DIMENSION)
        self.metadata = {}
        self._save_index()
        save_metadata(self.metadata, FAISS_METADATA_PATH)
        logger.info("FAISS index cleared")

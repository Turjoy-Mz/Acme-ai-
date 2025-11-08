"""Utility helper functions."""
import json
from pathlib import Path
from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)

def chunk_text(text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
    """
    Split text into overlapping chunks.
    
    Args:
        text: Text to chunk
        chunk_size: Size of each chunk
        overlap: Overlap between chunks
    
    Returns:
        List of text chunks
    """
    chunks = []
    step = chunk_size - overlap
    
    for i in range(0, len(text), step):
        chunk = text[i:i + chunk_size]
        if len(chunk) > 50:  # Only include meaningful chunks
            chunks.append(chunk)
    
    return chunks

def save_metadata(metadata: Dict[str, Any], path: Path) -> bool:
    """Save metadata to JSON file."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error saving metadata: {e}")
        return False

def load_metadata(path: Path) -> Dict[str, Any]:
    """Load metadata from JSON file."""
    try:
        if not path.exists():
            return {}
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading metadata: {e}")
        return {}

def generate_document_id(filename: str, chunk_index: int) -> str:
    """Generate unique document ID."""
    return f"{filename.replace('.txt', '')}_{chunk_index}"

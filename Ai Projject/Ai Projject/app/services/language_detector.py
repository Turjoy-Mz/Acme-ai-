"""Language detection service."""
from langdetect import detect, DetectorFactory
import logging

# Set seed for reproducibility
DetectorFactory.seed = 0

logger = logging.getLogger(__name__)

class LanguageDetector:
    """Detect language of text."""
    
    @staticmethod
    def detect(text: str, supported_languages: list = ["en", "ja"]) -> str:
        """
        Detect language of given text.
        
        Args:
            text: Text to detect language for
            supported_languages: List of supported languages
        
        Returns:
            Language code (en, ja, or en as fallback)
        """
        try:
            detected = detect(text[:500])  # Use first 500 chars
            if detected in supported_languages:
                return detected
            return "en"  # Default to English
        except Exception as e:
            logger.warning(f"Language detection failed: {e}, defaulting to English")
            return "en"
    
    @staticmethod
    def is_japanese(text: str) -> bool:
        """Check if text contains Japanese characters."""
        import re
        # Check for Hiragana, Katakana, or Kanji
        japanese_pattern = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]')
        return bool(japanese_pattern.search(text))

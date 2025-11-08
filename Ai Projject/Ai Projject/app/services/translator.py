"""Translation service for bilingual support."""
from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

class Translator:
    """Translate text between languages."""
    
    def __init__(self):
        """Initialize translation pipelines."""
        try:
            self.en_to_ja = pipeline("translation_en_to_ja", model="Helsinki-NLP/opus-mt-en-ja")
            self.ja_to_en = pipeline("translation_ja_to_en", model="Helsinki-NLP/opus-mt-ja-en")
        except Exception as e:
            logger.warning(f"Translation models not loaded: {e}")
            self.en_to_ja = None
            self.ja_to_en = None
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate text from source to target language.
        
        Args:
            text: Text to translate
            source_lang: Source language code (en/ja)
            target_lang: Target language code (en/ja)
        
        Returns:
            Translated text or original text if translation fails
        """
        # No translation needed
        if source_lang == target_lang:
            return text
        
        # English to Japanese
        if source_lang == "en" and target_lang == "ja":
            return self._translate_en_to_ja(text)
        
        # Japanese to English
        if source_lang == "ja" and target_lang == "en":
            return self._translate_ja_to_en(text)
        
        return text
    
    def _translate_en_to_ja(self, text: str) -> str:
        """Translate English to Japanese."""
        if not self.en_to_ja:
            logger.warning("EN-JA translator not available")
            return text
        
        try:
            result = self.en_to_ja(text, max_length=500)
            return result[0]["translation_text"]
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return text
    
    def _translate_ja_to_en(self, text: str) -> str:
        """Translate Japanese to English."""
        if not self.ja_to_en:
            logger.warning("JA-EN translator not available")
            return text
        
        try:
            result = self.ja_to_en(text, max_length=500)
            return result[0]["translation_text"]
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return text

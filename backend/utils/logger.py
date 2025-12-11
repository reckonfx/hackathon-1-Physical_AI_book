import logging
import sys
from datetime import datetime
from typing import Any, Dict


class TranslationLogger:
    """
    Custom logger for translation service with structured logging.
    """

    def __init__(self, name: str = "translation_service"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Avoid adding multiple handlers if logger already has them
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log_translation_request(self, request_data: Dict[str, Any], client_ip: str = None):
        """Log translation request details."""
        self.logger.info(f"Translation request from {client_ip or 'unknown'}: "
                        f"target_lang={request_data.get('target_language')}, "
                        f"char_count={len(request_data.get('text', ''))}")

    def log_translation_response(self, response_data: Dict[str, Any], processing_time: float):
        """Log translation response details."""
        self.logger.info(f"Translation completed: "
                        f"target_lang={response_data.get('target_language')}, "
                        f"processing_time={processing_time:.2f}ms")

    def log_error(self, error_type: str, error_message: str, context: Dict[str, Any] = None):
        """Log error with context."""
        context_str = f", context={context}" if context else ""
        self.logger.error(f"{error_type}: {error_message}{context_str}")

    def log_language_detection(self, text_sample: str, detected_lang: str, confidence: float):
        """Log language detection result."""
        self.logger.info(f"Language detection: detected={detected_lang}, "
                        f"confidence={confidence:.2f}, text_len={len(text_sample)}")

    def log_rate_limit_event(self, client_ip: str, limit: int, window: int):
        """Log rate limit events."""
        self.logger.warning(f"Rate limit triggered for {client_ip}: "
                           f"limit={limit}, window={window}s")
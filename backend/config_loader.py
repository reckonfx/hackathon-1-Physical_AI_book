import os
from typing import Dict, Any
from dotenv import load_dotenv


class ConfigLoader:
    """
    Configuration loader for different deployment stages (development, staging, production).
    """

    def __init__(self, env_file: str = ".env"):
        self.env_file = env_file
        self.environment = os.getenv("ENVIRONMENT", "development").lower()
        load_dotenv(self.env_file)

    def get_config(self) -> Dict[str, Any]:
        """
        Get configuration based on the current environment.
        """
        base_config = {
            "environment": self.environment,
            "debug": self._get_bool("DEBUG", self.environment == "development"),
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
            "port": int(os.getenv("PORT", "8000")),
            "host": os.getenv("HOST", "0.0.0.0"),
            # Translation API
            "translation_api_key": os.getenv("TRANSLATION_API_KEY"),
            "translation_api_url": os.getenv("TRANSLATION_API_URL", "https://translation.googleapis.com/language/translate/v2"),
            "detection_api_url": os.getenv("DETECTION_API_URL", "https://translation.googleapis.com/language/translate/v2/detect"),
            # Rate limiting
            "rate_limit_requests": int(os.getenv("RATE_LIMIT_REQUESTS", "100")),
            "rate_limit_window": int(os.getenv("RATE_LIMIT_WINDOW", "3600")),
            # Character limits
            "character_limit": int(os.getenv("CHARACTER_LIMIT", "1000")),
            # Supported languages
            "supported_languages": os.getenv("SUPPORTED_LANGUAGES", "en,es,fr,de,zh,ja,ko,ru,pt,ar").split(","),
            # Technical terms
            "technical_terms": os.getenv("TECHNICAL_TERMS", "SLAM,ROS,Gazebo,Isaac,VLA,AI,ML,NN").split(","),
        }

        # Environment-specific overrides
        if self.environment == "production":
            base_config.update({
                "debug": False,
                "log_level": os.getenv("LOG_LEVEL", "WARNING"),
                "rate_limit_requests": int(os.getenv("RATE_LIMIT_REQUESTS", "1000")),
                "rate_limit_window": int(os.getenv("RATE_LIMIT_WINDOW", "3600")),
            })
        elif self.environment == "staging":
            base_config.update({
                "debug": os.getenv("DEBUG", "false").lower() == "true",
                "log_level": os.getenv("LOG_LEVEL", "INFO"),
            })
        else:  # development
            base_config.update({
                "debug": True,
                "log_level": os.getenv("LOG_LEVEL", "DEBUG"),
            })

        return base_config

    def _get_bool(self, key: str, default: bool) -> bool:
        """Helper method to get boolean values from environment variables."""
        value = os.getenv(key)
        if value is None:
            return default
        return value.lower() in ("true", "1", "yes", "on")


# Global config instance
config_loader = ConfigLoader()
config = config_loader.get_config()
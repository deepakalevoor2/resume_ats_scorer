import os
import logging
from pydantic import BaseModel
from typing import Optional, Dict, Any

class Settings(BaseModel):
    """Application settings."""
    # API settings
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    
    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # CrewAI settings
    CREW_VERBOSE: bool = True
    
    # File upload settings
    UPLOAD_DIR: str = "/tmp/resume_uploads"
    MAX_UPLOAD_SIZE: int = 10_485_760  # 10MB
    
    # OpenAI settings (if needed for CrewAI)
    OPENAI_API_KEY: Optional[str] = None
    
    # Custom model settings
    MODEL_WEIGHTS: Dict[str, float] = {
        "content_match": 0.5,  # 50% of total score
        "format_compatibility": 0.2,  # 20% of total score
        "section_specific": 0.3,  # 30% of total score
    }


# Initialize settings
settings = Settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT
)

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

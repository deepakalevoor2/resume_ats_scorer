import os
import logging
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any

class Settings(BaseModel):
    """Application settings."""
    # API settings
    API_PREFIX: str = Field(default="/api/v1", description="API prefix for all endpoints")
    DEBUG: bool = Field(default=False, description="Debug mode flag")
    
    # Logging settings
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Logging format"
    )
    
    # CrewAI settings
    CREW_VERBOSE: bool = Field(default=True, description="CrewAI verbose mode")
    
    # File upload settings
    UPLOAD_DIR: str = Field(
        default="/tmp/resume_uploads",
        description="Directory for uploaded files"
    )
    MAX_UPLOAD_SIZE: int = Field(
        default=10_485_760,  # 10MB
        description="Maximum upload size in bytes"
    )
    
    # OpenAI settings (if needed for CrewAI)
    OPENAI_API_KEY: Optional[str] = Field(
        default=None,
        description="OpenAI API key"
    )
    
    # Custom model settings
    MODEL_WEIGHTS: Dict[str, float] = Field(
        default={
            "content_match": 0.5,  # 50% of total score
            "format_compatibility": 0.2,  # 20% of total score
            "section_specific": 0.3,  # 30% of total score
        },
        description="Weights for different scoring components"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "API_PREFIX": "/api/v1",
                "DEBUG": False,
                "LOG_LEVEL": "INFO",
                "CREW_VERBOSE": True,
                "UPLOAD_DIR": "/tmp/resume_uploads",
                "MAX_UPLOAD_SIZE": 10485760,
                "MODEL_WEIGHTS": {
                    "content_match": 0.5,
                    "format_compatibility": 0.2,
                    "section_specific": 0.3
                }
            }
        }
    }

    @field_validator('LOG_LEVEL')
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Invalid log level. Must be one of {valid_levels}")
        return v.upper()

    @field_validator('MODEL_WEIGHTS')
    @classmethod
    def validate_model_weights(cls, v: Dict[str, float]) -> Dict[str, float]:
        total = sum(v.values())
        if abs(total - 1.0) > 0.001:  # Allow small floating point errors
            raise ValueError(f"Model weights must sum to 1.0, got {total}")
        return v


# Initialize settings
settings = Settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT
)

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

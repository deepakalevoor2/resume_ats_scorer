import logging
import sys
from logging.handlers import RotatingFileHandler
import os
from .config import settings

# Define custom logging configuration
def setup_logging(log_file="resume_ats_scorer.log"):
    """Configure application logging."""
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    log_file_path = os.path.join(logs_dir, log_file)
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Configure formatter
    formatter = logging.Formatter(settings.LOG_FORMAT)
    
    # Configure console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Configure file handler with rotation
    file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=10_485_760,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Return configured logger
    return logger


# Create a logger specifically for the resume_ats_scorer package
app_logger = setup_logging()
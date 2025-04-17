import logging
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile
from typing import Optional
from enum import Enum
from pydantic import ValidationError

from ..core.crew_manager import ResumeCrewManager
from ..models.schemas import ScoringRequest, ResumeScoreResult, FileType, JobPlatform

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Resume ATS Score Checker API",
    description="API for analyzing resumes against job descriptions for ATS compatibility",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize the crew manager
crew_manager = ResumeCrewManager()


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to the Resume ATS Score Checker API"}


@app.post("/score", response_model=ResumeScoreResult)
async def score_resume(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...),
    job_platform: JobPlatform = Form(JobPlatform.OTHER)
):
    """Score a resume against a job description."""
    try:
        # Determine file type
        file_extension = os.path.splitext(resume_file.filename)[1].lower()
        
        if file_extension == ".pdf":
            file_type = FileType.PDF
        elif file_extension == ".docx":
            file_type = FileType.DOCX
        elif file_extension == ".html":
            file_type = FileType.HTML
        elif file_extension == ".txt":
            file_type = FileType.TXT
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_extension}")
        
        # Save uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            temp_file.write(await resume_file.read())
            temp_file_path = temp_file.name
        
        try:
            # Create scoring request
            request = ScoringRequest(
                resume_file_path=temp_file_path,
                job_description=job_description,
                job_platform=job_platform,
                file_type=file_type
            )
            
            # Process the request
            result = await crew_manager.score_resume(request)
            
            return result
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
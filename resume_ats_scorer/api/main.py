import logging
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile
from typing import Optional
from enum import Enum
from pydantic import ValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil

from ..core.crew_manager import ResumeCrewManager
from ..models.schemas import ScoringRequest, ResumeScoreResult, FileType, JobPlatform
from .routes import resume, job_description, scoring
from ..core.exceptions import (
    ResumeATSException,
    FileValidationError,
    ParsingError,
    UnsupportedFileTypeError,
    FileNotFoundError,
    ScoringError,
    JobDescriptionError
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Resume ATS Scorer API",
    description="""
    A comprehensive API for analyzing resumes against job descriptions and providing ATS compatibility scores.
    
    ## Features
    
    * Resume parsing and analysis
    * Job description processing
    * ATS compatibility scoring
    * Improvement recommendations
    
    ## Supported File Formats
    
    * PDF
    * DOCX
    * HTML
    * TXT
    """,
    version="1.0.0",
    contact={
        "name": "Resume ATS Scorer Team",
        "email": "support@resumeatsscorer.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
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

# Include routers
app.include_router(resume.router, prefix="/api/v1/resume", tags=["Resume"])
app.include_router(job_description.router, prefix="/api/v1/job-description", tags=["Job Description"])
app.include_router(scoring.router, prefix="/api/v1/scoring", tags=["Scoring"])

# Custom exception handlers
@app.exception_handler(ResumeATSException)
async def resume_ats_exception_handler(request, exc: ResumeATSException):
    logger.error(f"Resume ATS Error: {str(exc)}")
    if isinstance(exc, FileValidationError):
        return JSONResponse(
            status_code=400,
            content={"detail": f"File validation error: {str(exc)}"}
        )
    elif isinstance(exc, ParsingError):
        return JSONResponse(
            status_code=422,
            content={"detail": f"Parsing error: {str(exc)}"}
        )
    elif isinstance(exc, UnsupportedFileTypeError):
        return JSONResponse(
            status_code=400,
            content={"detail": f"Unsupported file type: {str(exc)}"}
        )
    elif isinstance(exc, FileNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail": f"File not found: {str(exc)}"}
        )
    elif isinstance(exc, ScoringError):
        return JSONResponse(
            status_code=500,
            content={"detail": f"Scoring error: {str(exc)}"}
        )
    elif isinstance(exc, JobDescriptionError):
        return JSONResponse(
            status_code=400,
            content={"detail": f"Job description error: {str(exc)}"}
        )
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred"}
    )

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Resume ATS Scorer API",
        version="1.0.0",
        description="""
        API for analyzing resumes against job descriptions and providing ATS compatibility scores.
        
        ## Authentication
        
        This API uses API key authentication. Include your API key in the `X-API-Key` header.
        
        ## Rate Limiting
        
        * Free tier: 100 requests per day
        * Pro tier: 1000 requests per day
        * Enterprise: Custom limits
        
        ## Error Codes
        
        * 400: Bad Request
        * 401: Unauthorized
        * 403: Forbidden
        * 404: Not Found
        * 422: Unprocessable Entity
        * 429: Too Many Requests
        * 500: Internal Server Error
        """,
        routes=app.routes,
    )
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key"
        }
    }
    
    # Add security requirements
    openapi_schema["security"] = [{"ApiKeyAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/", tags=["Info"])
async def root():
    """Root endpoint providing basic API information."""
    return {
        "name": "Resume ATS Scorer API",
        "version": "1.0.0",
        "description": "API for analyzing resumes against job descriptions",
        "documentation": "/docs",
        "redoc": "/redoc"
    }

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

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

# Temporary file handling
@app.on_event("startup")
async def startup_event():
    """Create temporary directory for file uploads."""
    temp_dir = Path(tempfile.gettempdir()) / "resume_ats_scorer"
    temp_dir.mkdir(exist_ok=True)
    logger.info(f"Created temporary directory: {temp_dir}")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up temporary files on shutdown."""
    temp_dir = Path(tempfile.gettempdir()) / "resume_ats_scorer"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
        logger.info(f"Cleaned up temporary directory: {temp_dir}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
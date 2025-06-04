import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any
from ...models.schemas import (
    JobDescriptionRequest,
    ParsedJobDescription,
    JobSource
)
from resume_ats_scorer.utils.text_processors import extract_job_requirements

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1",
    tags=["job-description"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}}
)

class JobDescriptionRequest(BaseModel):
    job_description: str

@router.get("/health")
async def health_check():
    """Health check endpoint for job description service"""
    return {"status": "ok", "service": "job-description"}

@router.post("/analyze")
async def analyze_job_description(request: JobDescriptionRequest) -> Any:
    """Analyze a job description and extract requirements."""
    try:
        logger.info(f"Received job description for analysis: {request.job_description[:30]}...")
        requirements = extract_job_requirements(request.job_description)
        return {"requirements": requirements}
    except Exception as e:
        logger.exception(f"Error analyzing job description: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing job description: {str(e)}") 
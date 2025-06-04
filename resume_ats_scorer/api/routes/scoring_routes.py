import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any
from ..models.schemas import ErrorResponse, KeywordAnalysis, JobRequirements
from utils.scoring import calculate_resume_score

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1",
    tags=["scoring"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}}
)

class ScoringRequest(BaseModel):
    resume_text: str
    resume_filename: str
    resume_keywords: KeywordAnalysis
    job_requirements: JobRequirements
    job_title: str
    file_type: str

@router.get("/health")
async def health_check():
    """Health check endpoint for scoring service"""
    return {"status": "ok", "service": "scoring"}

@router.post("/score")
async def score(request: ScoringRequest) -> Any:
    """Score endpoint using calculate_resume_score."""
    try:
        logger.info(f"Received data for scoring: {request.resume_filename}")
        response = calculate_resume_score(
            resume_text=request.resume_text,
            resume_filename=request.resume_filename,
            resume_keywords=request.resume_keywords,
            job_requirements=request.job_requirements,
            job_title=request.job_title,
            file_type=request.file_type
        )
        return response
    except Exception as e:
        logger.exception(f"Error in scoring: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in scoring: {str(e)}") 
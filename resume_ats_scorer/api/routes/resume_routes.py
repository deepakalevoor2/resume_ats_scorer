import logging
import tempfile
import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List

from ...models.schemas import (
    ResumeUploadRequest,
    ResumeScoreResponse,
    FileType,
    JobSource,
    ParsedResume,
    ParsedJobDescription,
    ErrorResponse
)
from resume_ats_scorer.utils.file_handlers import save_upload_file, extract_text_from_file
from resume_ats_scorer.utils.scoring import calculate_resume_score
from resume_ats_scorer.utils.text_processors import extract_keywords_from_resume, extract_job_requirements
from resume_ats_scorer.utils.agents import create_crew_for_analysis

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1",
    tags=["resume"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}}
)


@router.post("/score-resume", response_model=ResumeScoreResponse)
async def score_resume(
    background_tasks: BackgroundTasks,
    resume_file: UploadFile = File(...),
    job_description: str = Form(...),
    job_source: JobSource = Form(JobSource.OTHER),
    job_title: str = Form(...)
):
    """
    Upload a resume and job description to get an ATS compatibility score.
    """
    try:
        logger.info(f"Processing resume upload: {resume_file.filename}")
        
        # Validate file type
        file_extension = os.path.splitext(resume_file.filename)[1].lower().replace('.', '')
        if file_extension not in ["pdf", "docx", "txt", "html"]:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type: {file_extension}. Please upload PDF, DOCX, TXT, or HTML."
            )
        
        # Save uploaded file to temp directory
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
            temp_path = temp_file.name
            await save_upload_file(resume_file, temp_path)
        
        # Extract text from resume
        try:
            resume_text = extract_text_from_file(temp_path, file_extension)
            if not resume_text or len(resume_text.strip()) < 100:
                raise HTTPException(
                    status_code=400,
                    detail="Could not extract sufficient text from the resume. Please check the file."
                )
        finally:
            # Clean up temp file
            background_tasks.add_task(os.unlink, temp_path)
        
        # Process job description and resume
        resume_request = ResumeUploadRequest(
            job_description=job_description,
            job_source=job_source,
            job_title=job_title
        )
        
        # Create a crew for analysis using CrewAI
        crew = create_crew_for_analysis()
        
        # Extract keywords and requirements
        resume_keywords = extract_keywords_from_resume(resume_text)
        job_requirements = extract_job_requirements(job_description, job_source)
        
        # Calculate score
        score_response = calculate_resume_score(
            resume_text=resume_text,
            resume_filename=resume_file.filename,
            resume_keywords=resume_keywords,
            job_requirements=job_requirements,
            job_title=job_title,
            file_type=file_extension
        )
        
        logger.info(f"Resume scored successfully: {resume_file.filename} - Total Score: {score_response.total_score}")
        return score_response
        
    except HTTPException as e:
        logger.error(f"HTTP error during resume scoring: {str(e)}")
        raise
    except Exception as e:
        logger.exception(f"Error scoring resume: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing resume: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "resume-ats-scorer"}
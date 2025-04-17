from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime
import re


class FileType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    HTML = "html"


class JobSource(str, Enum):
    LINKEDIN = "linkedin"
    NAUKRI = "naukri"
    INDEED = "indeed"
    MONSTER = "monster"
    GLASSDOOR = "glassdoor"
    OTHER = "other"


class SectionScore(BaseModel):
    name: str
    score: float
    max_score: float
    feedback: str


class ContentMatch(BaseModel):
    score: float = Field(..., ge=0, le=40)
    matched_keywords: List[str]
    missing_keywords: List[str]
    feedback: str


class FormatCompatibility(BaseModel):
    score: float = Field(..., ge=0, le=20)
    issues: List[str]
    feedback: str


class SectionAnalysis(BaseModel):
    score: float = Field(..., ge=0, le=30)
    sections: List[SectionScore]
    feedback: str


class OverallScore(BaseModel):
    score: float = Field(..., ge=0, le=10)
    feedback: str


class ResumeUploadRequest(BaseModel):
    job_description: str
    job_source: JobSource = JobSource.OTHER
    job_title: str


class KeywordAnalysis(BaseModel):
    hard_skills: List[str]
    soft_skills: List[str]
    experience: Dict[str, int]
    education: List[str]


class JobRequirements(BaseModel):
    required_skills: List[str]
    preferred_skills: List[str]
    experience_required: Optional[int] = None
    education_required: Optional[List[str]] = None


class ResumeScoreResponse(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    filename: str
    content_match: ContentMatch
    format_compatibility: FormatCompatibility
    section_analysis: SectionAnalysis
    overall_score: OverallScore
    total_score: float = Field(..., ge=0, le=100)
    keyword_analysis: KeywordAnalysis
    job_requirements: JobRequirements
    improvement_suggestions: List[str]

    @validator('total_score')
    def validate_total_score(cls, v, values):
        expected_total = (
            values.get('content_match', ContentMatch(score=0, matched_keywords=[], missing_keywords=[], feedback="")).score +
            values.get('format_compatibility', FormatCompatibility(score=0, issues=[], feedback="")).score +
            values.get('section_analysis', SectionAnalysis(score=0, sections=[], feedback="")).score +
            values.get('overall_score', OverallScore(score=0, feedback="")).score
        )
        
        if abs(v - expected_total) > 0.5:  # Allow small rounding errors
            raise ValueError(f"Total score {v} does not match sum of individual scores {expected_total}")
        return round(v, 1)


class ErrorResponse(BaseModel):
    error: str
    details: Optional[Any] = None
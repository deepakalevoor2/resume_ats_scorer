from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class FileType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    HTML = "html"
    TXT = "txt"


class ResumeSection(str, Enum):
    CONTACT = "contact"
    SUMMARY = "summary"
    EXPERIENCE = "experience"
    EDUCATION = "education"
    SKILLS = "skills"
    CERTIFICATIONS = "certifications"
    PROJECTS = "projects"
    LANGUAGES = "languages"
    OTHER = "other"


class JobPlatform(str, Enum):
    LINKEDIN = "linkedin"
    INDEED = "indeed"
    GLASSDOOR = "glassdoor"
    MONSTER = "monster"
    OTHER = "other"


class ParsedResume(BaseModel):
    raw_text: str = Field(..., description="The raw text extracted from the resume")
    sections: Dict[ResumeSection, str] = Field(default_factory=dict, description="Resume content organized by sections")
    keywords: List[str] = Field(default_factory=list, description="Keywords extracted from the resume")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata about the resume")

    model_config = {
        "json_schema_extra": {
            "example": {
                "raw_text": "John Doe\nSoftware Engineer\n...",
                "sections": {
                    "contact": "John Doe\njohn@example.com",
                    "experience": "Software Engineer at Company\n..."
                },
                "keywords": ["python", "machine learning"],
                "metadata": {"file_type": "pdf"}
            }
        }
    }


class JobRequirement(BaseModel):
    category: str = Field(..., description="Category of the requirement (e.g., skill, experience)")
    description: str = Field(..., description="Description of the requirement")
    importance: float = Field(default=1.0, ge=0.0, le=1.0, description="Importance weight of this requirement (0-1)")
    required: bool = Field(default=True, description="Whether this requirement is mandatory")

    model_config = {
        "json_schema_extra": {
            "example": {
                "category": "skill",
                "description": "Python programming",
                "importance": 0.8,
                "required": True
            }
        }
    }


class ParsedJobDescription(BaseModel):
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    description: str = Field(..., description="Full job description text")
    requirements: List[JobRequirement] = Field(default_factory=list, description="Extracted job requirements")
    keywords: List[str] = Field(default_factory=list, description="Keywords extracted from the job description")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata about the job posting")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Senior Software Engineer",
                "company": "Tech Corp",
                "description": "Looking for a senior software engineer...",
                "requirements": [
                    {
                        "category": "skill",
                        "description": "Python",
                        "importance": 0.8,
                        "required": True
                    }
                ],
                "keywords": ["python", "aws"],
                "metadata": {"platform": "linkedin"}
            }
        }
    }


class SectionScore(BaseModel):
    section: ResumeSection
    score: float = Field(..., ge=0, le=10, description="Score for this section (0-10)")
    max_score: float = Field(default=10, description="Maximum possible score for this section")
    feedback: str = Field(..., description="Feedback on this section")
    matches: List[str] = Field(default_factory=list, description="Matching keywords or phrases")
    missing: List[str] = Field(default_factory=list, description="Missing keywords or phrases")

    model_config = {
        "json_schema_extra": {
            "example": {
                "section": "experience",
                "score": 8.5,
                "max_score": 10,
                "feedback": "Strong experience section",
                "matches": ["python", "aws"],
                "missing": ["kubernetes"]
            }
        }
    }


class ResumeScoreResult(BaseModel):
    total_score: float = Field(..., ge=0, le=100, description="Overall ATS compatibility score (0-100)")
    content_match_score: float = Field(..., ge=0, le=50, description="Content match score (0-50)")
    format_compatibility_score: float = Field(..., ge=0, le=20, description="Format compatibility score (0-20)")
    section_scores: List[SectionScore] = Field(default_factory=list, description="Scores for each resume section")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations for improvement")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp of when the score was generated")

    model_config = {
        "json_schema_extra": {
            "example": {
                "total_score": 85.5,
                "content_match_score": 42.5,
                "format_compatibility_score": 18.0,
                "section_scores": [
                    {
                        "section": "experience",
                        "score": 8.5,
                        "max_score": 10,
                        "feedback": "Strong experience section",
                        "matches": ["python", "aws"],
                        "missing": ["kubernetes"]
                    }
                ],
                "recommendations": ["Add more details about Kubernetes experience"],
                "created_at": "2024-03-20T12:00:00"
            }
        }
    }

    @field_validator('total_score')
    @classmethod
    def validate_total_score(cls, v: float) -> float:
        return round(v, 2)


class ScoringRequest(BaseModel):
    resume_file_path: str = Field(..., description="Path to the uploaded resume file")
    job_description: str = Field(..., description="Job description text")
    job_platform: JobPlatform = Field(default=JobPlatform.OTHER, description="Platform where the job was posted")
    file_type: FileType = Field(..., description="Type of resume file")
    additional_context: Dict[str, Any] = Field(default_factory=dict, description="Additional context for scoring")

    model_config = {
        "json_schema_extra": {
            "example": {
                "resume_file_path": "/path/to/resume.pdf",
                "job_description": "Looking for a senior software engineer...",
                "job_platform": "linkedin",
                "file_type": "pdf",
                "additional_context": {"industry": "tech"}
            }
        }
    }
from pydantic import BaseModel, Field, field_validator
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
    name: str = Field(..., description="Name of the section")
    score: float = Field(..., ge=0, le=10, description="Score for this section (0-10)")
    max_score: float = Field(default=10, description="Maximum possible score for this section")
    feedback: str = Field(..., description="Feedback on this section")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Experience",
                "score": 8.5,
                "max_score": 10,
                "feedback": "Strong experience section with relevant details"
            }
        }
    }


class ContentMatch(BaseModel):
    score: float = Field(..., ge=0, le=40, description="Content match score (0-40)")
    matched_keywords: List[str] = Field(default_factory=list, description="Keywords that matched")
    missing_keywords: List[str] = Field(default_factory=list, description="Keywords that were missing")
    feedback: str = Field(..., description="Feedback on content match")

    model_config = {
        "json_schema_extra": {
            "example": {
                "score": 35.5,
                "matched_keywords": ["python", "aws"],
                "missing_keywords": ["kubernetes"],
                "feedback": "Good match with most required skills"
            }
        }
    }


class FormatCompatibility(BaseModel):
    score: float = Field(..., ge=0, le=20, description="Format compatibility score (0-20)")
    issues: List[str] = Field(default_factory=list, description="Format-related issues found")
    feedback: str = Field(..., description="Feedback on format compatibility")

    model_config = {
        "json_schema_extra": {
            "example": {
                "score": 18.0,
                "issues": ["Font size too small in some sections"],
                "feedback": "Good overall format with minor issues"
            }
        }
    }


class SectionAnalysis(BaseModel):
    score: float = Field(..., ge=0, le=30, description="Section analysis score (0-30)")
    sections: List[SectionScore] = Field(default_factory=list, description="Scores for each section")
    feedback: str = Field(..., description="Feedback on section analysis")

    model_config = {
        "json_schema_extra": {
            "example": {
                "score": 25.5,
                "sections": [
                    {
                        "name": "Experience",
                        "score": 8.5,
                        "max_score": 10,
                        "feedback": "Strong experience section"
                    }
                ],
                "feedback": "Well-structured sections with good content"
            }
        }
    }


class OverallScore(BaseModel):
    score: float = Field(..., ge=0, le=10, description="Overall score (0-10)")
    feedback: str = Field(..., description="Overall feedback")

    model_config = {
        "json_schema_extra": {
            "example": {
                "score": 8.5,
                "feedback": "Strong resume overall"
            }
        }
    }


class ResumeUploadRequest(BaseModel):
    job_description: str = Field(..., description="Job description text")
    job_source: JobSource = Field(default=JobSource.OTHER, description="Source of the job posting")
    job_title: str = Field(..., description="Job title")

    model_config = {
        "json_schema_extra": {
            "example": {
                "job_description": "Looking for a senior software engineer...",
                "job_source": "linkedin",
                "job_title": "Senior Software Engineer"
            }
        }
    }


class KeywordAnalysis(BaseModel):
    hard_skills: List[str] = Field(default_factory=list, description="Hard skills found")
    soft_skills: List[str] = Field(default_factory=list, description="Soft skills found")
    experience: Dict[str, int] = Field(default_factory=dict, description="Experience in years by category")
    education: List[str] = Field(default_factory=list, description="Education details")

    model_config = {
        "json_schema_extra": {
            "example": {
                "hard_skills": ["python", "aws"],
                "soft_skills": ["leadership", "communication"],
                "experience": {"python": 5, "aws": 3},
                "education": ["B.S. Computer Science"]
            }
        }
    }


class JobRequirements(BaseModel):
    required_skills: List[str] = Field(default_factory=list, description="Required skills")
    preferred_skills: List[str] = Field(default_factory=list, description="Preferred skills")
    experience_required: Optional[int] = Field(default=None, description="Years of experience required")
    education_required: Optional[List[str]] = Field(default=None, description="Required education")

    model_config = {
        "json_schema_extra": {
            "example": {
                "required_skills": ["python", "aws"],
                "preferred_skills": ["kubernetes"],
                "experience_required": 5,
                "education_required": ["B.S. Computer Science"]
            }
        }
    }


class ResumeScoreResponse(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp of the analysis")
    filename: str = Field(..., description="Name of the resume file")
    content_match: ContentMatch
    format_compatibility: FormatCompatibility
    section_analysis: SectionAnalysis
    overall_score: OverallScore
    total_score: float = Field(..., ge=0, le=100, description="Total ATS compatibility score (0-100)")
    keyword_analysis: KeywordAnalysis
    job_requirements: JobRequirements
    improvement_suggestions: List[str] = Field(default_factory=list, description="Suggestions for improvement")

    model_config = {
        "json_schema_extra": {
            "example": {
                "timestamp": "2024-03-20T12:00:00",
                "filename": "resume.pdf",
                "content_match": {
                    "score": 35.5,
                    "matched_keywords": ["python", "aws"],
                    "missing_keywords": ["kubernetes"],
                    "feedback": "Good match with most required skills"
                },
                "format_compatibility": {
                    "score": 18.0,
                    "issues": ["Font size too small in some sections"],
                    "feedback": "Good overall format with minor issues"
                },
                "section_analysis": {
                    "score": 25.5,
                    "sections": [
                        {
                            "name": "Experience",
                            "score": 8.5,
                            "max_score": 10,
                            "feedback": "Strong experience section"
                        }
                    ],
                    "feedback": "Well-structured sections with good content"
                },
                "overall_score": {
                    "score": 8.5,
                    "feedback": "Strong resume overall"
                },
                "total_score": 87.5,
                "keyword_analysis": {
                    "hard_skills": ["python", "aws"],
                    "soft_skills": ["leadership", "communication"],
                    "experience": {"python": 5, "aws": 3},
                    "education": ["B.S. Computer Science"]
                },
                "job_requirements": {
                    "required_skills": ["python", "aws"],
                    "preferred_skills": ["kubernetes"],
                    "experience_required": 5,
                    "education_required": ["B.S. Computer Science"]
                },
                "improvement_suggestions": ["Add more details about Kubernetes experience"]
            }
        }
    }

    @field_validator('total_score')
    @classmethod
    def validate_total_score(cls, v: float, info) -> float:
        values = info.data
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
    error: str = Field(..., description="Error message")
    details: Optional[Any] = Field(default=None, description="Additional error details")

    model_config = {
        "json_schema_extra": {
            "example": {
                "error": "Invalid file format",
                "details": "Only PDF, DOCX, TXT, and HTML files are supported"
            }
        }
    }
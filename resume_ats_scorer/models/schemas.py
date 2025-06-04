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
    matches: List[str] = Field(default_factory=list, description="Matching keywords or phrases")
    missing: List[str] = Field(default_factory=list, description="Missing keywords or phrases")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Experience",
                "score": 8.5,
                "max_score": 10,
                "feedback": "Strong experience section with relevant details",
                "matches": ["python", "aws"],
                "missing": ["kubernetes"]
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
                        "feedback": "Strong experience section",
                        "matches": ["python", "aws"],
                        "missing": ["kubernetes"]
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
    """Response model for resume scoring."""
    success: bool = Field(..., description="Whether the scoring was successful")
    overall_score: float = Field(..., description="Overall ATS compatibility score (0-100)")
    content_score: float = Field(..., description="Content match score (0-100)")
    format_score: float = Field(..., description="Format compatibility score (0-100)")
    section_scores: Dict[str, float] = Field(..., description="Scores for each resume section")
    recommendations: List[str] = Field(..., description="List of improvement recommendations")
    breakdown: Dict[str, Dict[str, float]] = Field(
        ...,
        description="Detailed breakdown of scoring weights and calculations",
        example={
            "content_match": {
                "keyword_matching": 0.8,
                "experience_relevance": 0.7
            },
            "format_compatibility": {
                "document_structure": 0.9,
                "ats_friendly_elements": 0.85
            },
            "section_weights": {
                "summary": 0.05,
                "experience": 0.07,
                "skills": 0.05,
                "education": 0.03
            }
        }
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "overall_score": 85.5,
                "content_score": 35.5,
                "format_score": 18.0,
                "section_scores": {
                    "contact": 10.0,
                    "summary": 8.5,
                    "experience": 8.5,
                    "education": 8.5,
                    "skills": 8.5,
                    "certifications": 10.0,
                    "projects": 10.0,
                    "languages": 10.0,
                    "other": 10.0
                },
                "recommendations": [
                    "Add more details about Kubernetes experience",
                    "Increase font size in some sections"
                ],
                "breakdown": {
                    "content_match": {
                        "keyword_matching": 0.8,
                        "experience_relevance": 0.7
                    },
                    "format_compatibility": {
                        "document_structure": 0.9,
                        "ats_friendly_elements": 0.85
                    },
                    "section_weights": {
                        "summary": 0.05,
                        "experience": 0.07,
                        "skills": 0.05,
                        "education": 0.03
                    }
                }
            }
        }
    }

    @field_validator('overall_score')
    @classmethod
    def validate_overall_score(cls, v: float) -> float:
        return round(v, 2)

    @field_validator('content_score')
    @classmethod
    def validate_content_score(cls, v: float) -> float:
        return round(v, 2)

    @field_validator('format_score')
    @classmethod
    def validate_format_score(cls, v: float) -> float:
        return round(v, 2)


class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    details: Optional[Any] = Field(default=None, description="Additional error details")

    model_config = {
        "json_schema_extra": {
            "example": {
                "error": "Invalid file format",
                "details": {"supported_formats": ["pdf", "docx", "txt", "html"]}
            }
        }
    }
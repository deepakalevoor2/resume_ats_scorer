import pytest
import os
import tempfile
from pathlib import Path
from resume_ats_scorer.core.config import Settings
import json
import shutil

@pytest.fixture(scope="session")
def test_settings():
    """Create test settings with temporary directories."""
    # Create temporary directories
    temp_dir = Path(tempfile.mkdtemp())
    upload_dir = temp_dir / "uploads"
    upload_dir.mkdir()
    
    # Create test settings
    settings = Settings(
        UPLOAD_DIR=str(upload_dir),
        MAX_FILE_SIZE=10 * 1024 * 1024,  # 10MB
        ALLOWED_FILE_TYPES=[".pdf", ".docx", ".html", ".txt"],
        LOG_LEVEL="DEBUG",
        TESTING=True
    )
    
    yield settings
    
    # Cleanup
    shutil.rmtree(temp_dir)

@pytest.fixture(autouse=True)
def setup_test_env(test_settings, monkeypatch):
    """Set up test environment variables."""
    monkeypatch.setenv("TESTING", "true")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("UPLOAD_DIR", test_settings.UPLOAD_DIR)

@pytest.fixture
def sample_resume_content():
    """Sample resume content for testing."""
    return """
    PROFESSIONAL SUMMARY
    Experienced software developer with 5+ years of experience in Python and web development.
    
    WORK EXPERIENCE
    Senior Developer at Tech Corp (2020-Present)
    - Led development of REST APIs using Django
    - Implemented AWS cloud solutions
    - Mentored junior developers
    
    EDUCATION
    BS in Computer Science
    University of Technology (2015-2019)
    
    SKILLS
    Python, Django, REST APIs, AWS, SQL, Git
    """

@pytest.fixture
def sample_job_description():
    """Sample job description for testing."""
    return {
        "title": "Senior Software Engineer",
        "description": "Looking for an experienced Python developer with cloud experience",
        "requirements": [
            "5+ years of Python development",
            "Experience with Django framework",
            "REST API development",
            "AWS cloud services",
            "Strong problem-solving skills"
        ],
        "preferred_skills": [
            "Docker",
            "CI/CD",
            "Microservices architecture"
        ]
    }

@pytest.fixture
def mock_resume_file(sample_resume_content):
    """Create a mock resume file for testing."""
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        f.write(sample_resume_content.encode())
        return f.name

@pytest.fixture
def mock_job_description_file(sample_job_description):
    """Create a mock job description file for testing."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        f.write(json.dumps(sample_job_description).encode())
        return f.name 
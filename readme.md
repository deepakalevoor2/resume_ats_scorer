# Resume ATS Scorer

A multi-agent system for analyzing resumes against job descriptions and providing ATS (Applicant Tracking System) compatibility scores.

## Features

- **Resume Parsing**: Extract text from various file formats (PDF, DOCX, HTML, TXT)
- **Keyword Analysis**: Identify key skills and qualifications
- **Job Description Processing**: Parse and analyze job requirements
- **ATS Compatibility Scoring**: Evaluate resume format and content
- **Improvement Recommendations**: Suggest ways to enhance ATS compatibility

## Installation

### Prerequisites

- Python 3.12 or higher
- Docker (optional)

### Using pip

```bash
pip install resume-ats-scorer
```

### From source

```bash
git clone https://github.com/deepakalevoor2/resume_ats_scorer.git
cd resume_ats_scorer
pip install -e .
```

### Using Docker

```bash
docker pull deepakalevoor2/resume-ats-scorer:latest
docker run -p 8000:8000 resume-ats-scorer
```

## Usage

### API Server

Start the API server:

```bash
uvicorn resume_ats_scorer.api.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000` with documentation at `http://localhost:8000/docs`.

### Python Package

```python
from resume_ats_scorer import ResumeATSScorer

# Initialize the scorer
scorer = ResumeATSScorer()

# Score a resume against a job description
result = scorer.score_resume(
    resume_path="path/to/resume.pdf",
    job_description={
        "title": "Senior Software Engineer",
        "description": "Looking for a Python developer...",
        "requirements": ["Python", "Django", "AWS"]
    }
)

# Get the score and recommendations
print(f"ATS Score: {result.score}")
print("Recommendations:", result.recommendations)
```

## API Endpoints

### Resume Analysis

- `POST /api/v1/resume/upload`: Upload a resume file
- `GET /api/v1/resume/{resume_id}`: Get resume analysis results

### Job Description

- `POST /api/v1/job-description/submit`: Submit a job description
- `GET /api/v1/job-description/{job_id}`: Get job description details

### Scoring

- `POST /api/v1/scoring/score`: Score a resume against a job description
- `GET /api/v1/scoring/recommendations/{resume_id}/{job_id}`: Get improvement recommendations

## Scoring Mechanism

The scoring system uses a multi-dimensional approach (Total Score = 100):

### 1. Content Match (50 points)
- Keyword Matching (30 points)
- Experience Relevance (20 points)

### 2. Format Compatibility (30 points)
- Document Structure (15 points)
- ATS-Friendly Elements (15 points)

### 3. Section-Specific Scores (20 points)
- Professional Summary (5 points)
- Work Experience (7 points)
- Skills Section (5 points)
- Education (3 points)

## Development

### Setup Development Environment

```bash
git clone https://github.com/deepakalevoor2/resume_ats_scorer.git
cd resume_ats_scorer
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -e ".[dev]"
pre-commit install
```

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Format code
black .
isort .

# Lint code
flake8
mypy .

# Security check
bandit -r resume_ats_scorer
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) for the multi-agent framework
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [spaCy](https://spacy.io/) for NLP capabilities

## Support

For support, email support@resumeatsscorer.com or open an issue in the GitHub repository.
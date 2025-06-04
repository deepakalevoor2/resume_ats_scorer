# Resume ATS Scorer

[![CI/CD Pipeline](https://github.com/yourusername/resume-ats-scorer/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/yourusername/resume-ats-scorer/actions/workflows/ci-cd.yml)
[![codecov](https://codecov.io/gh/yourusername/resume-ats-scorer/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/resume-ats-scorer)

A multi-agent system for analyzing resumes against job descriptions and providing ATS (Applicant Tracking System) compatibility scores.

## Features

- **Resume Parsing**: Extract text from various file formats (PDF, DOCX, HTML, TXT)
- **Keyword Analysis**: Identify key skills and qualifications
- **Job Description Processing**: Parse and analyze job requirements
- **ATS Compatibility Scoring**: Evaluate resume format and content
- **Improvement Recommendations**: Suggest ways to enhance ATS compatibility

## Docker Image

The application is available as a Docker image on Docker Hub:

```bash
docker pull yourusername/resume-ats-scorer:latest
```

### Running with Docker

1. Pull the image:
```bash
docker pull yourusername/resume-ats-scorer:latest
```

2. Run the container:
```bash
docker run -d \
  --name resume-ats-scorer \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_api_key \
  -e API_KEY=your_api_key \
  -e DEBUG=false \
  -e LOG_LEVEL=INFO \
  -v /path/to/uploads:/app/uploads \
  -v /path/to/logs:/app/logs \
  yourusername/resume-ats-scorer:latest
```

The application will be available at `http://localhost:8000`.

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes | - |
| `API_KEY` | API key for securing endpoints | No | - |
| `DEBUG` | Enable debug mode | No | false |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | No | INFO |
| `UPLOAD_DIR` | Directory for uploaded files | No | /app/uploads |
| `MAX_UPLOAD_SIZE` | Maximum file upload size in bytes | No | 10485760 (10MB) |

### Volume Mounts

| Path | Description | Required |
|------|-------------|----------|
| `/app/uploads` | Directory for storing uploaded resumes | No |
| `/app/logs` | Directory for application logs | No |

### Docker Compose

For development or testing, you can use Docker Compose:

```yaml
version: '3.8'

services:
  resume-ats-scorer:
    image: yourusername/resume-ats-scorer:latest
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=your_api_key
      - API_KEY=your_api_key
      - DEBUG=false
      - LOG_LEVEL=INFO
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
```

Save this as `docker-compose.yml` and run:
```bash
docker-compose up -d
```

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
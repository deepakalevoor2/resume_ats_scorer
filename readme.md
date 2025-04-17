# Resume ATS Score Checker

A Python package that analyzes resumes against job descriptions to provide ATS compatibility scores and recommendations for improvement.

## Features

- **Resume Parser**: Extract text from uploaded resume files (PDF, DOCX, HTML, TXT)
- **Keyword Analyst**: Extract and analyze keywords from uploaded resumes
- **Job Description Parser**: Extract key requirements from job postings (Naukri, LinkedIn, etc.)
- **Matching Algorithm**: Compare resume content against job requirements
- **Scoring System**: Generate a numeric score based on keyword matching and formatting analysis
- **Recommendation Engine**: Suggest improvements & feedback to increase ATS compatibility

## Scoring Mechanism

The system uses a multi-dimensional scoring approach with a maximum total score of 100 points:

### Content Match (50 points)
Measures how well the resume content aligns with job requirements:
- Keyword matches
- Required skills presence
- Experience relevance

### Format Compatibility (20 points)
Evaluates how well the resume format works with ATS systems:
- Clear section headings
- Standard formatting
- Proper use of text vs. tables/graphics

### Section-Specific Analysis (30 points)
Targeted scores for key resume sections:
- Skills Match (10 points)
- Experience Match (10 points)
- Education Match (5 points)
- Overall Formatting (5 points)

## Examples

### Score Interpretation

| Score Range | Interpretation |
|-------------|----------------|
| 90-100      | Excellent - Highly ATS compatible |
| 75-89       | Good - Generally ATS compatible |  
| 60-74       | Fair - Some improvements needed |
| Below 60    | Poor - Significant improvements needed |

### Sample Recommendations

- "Add these missing keywords: Python, AWS, Docker"
- "Improve your Skills section by using more specific technical terms"
- "Use strong action verbs in your Experience section"
- "Consider adding quantifiable achievements with numbers and percentages"

## Installation

```bash
pip install resume-ats-scorer
```

## Usage

### As a Python Package

```python
from resume_ats_scorer.core.crew_manager import ResumeCrewManager
from resume_ats_scorer.models.schemas import ScoringRequest, FileType, JobPlatform

# Create a scoring request
request = ScoringRequest(
    resume_file_path="/path/to/resume.pdf",
    job_description="Job description text...",
    job_platform=JobPlatform.LINKEDIN,
    file_type=FileType.PDF
)

# Process the request
crew_manager = ResumeCrewManager()
result = await crew_manager.score_resume(request)

# Print the results
print(f"Total Score: {result.total_score}")
print(f"Content Match Score: {result.content_match_score}")
print(f"Format Compatibility Score: {result.format_compatibility_score}")
print("Recommendations:")
for rec in result.recommendations:
    print(f"- {rec}")
```

### Using the API

Start the API server:

```bash
uvicorn resume_ats_scorer.api.main:app --reload
```

Then make requests to the API:

```bash
curl -X POST "http://localhost:8000/score" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
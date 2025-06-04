# Resume ATS Scoring Mechanism

## Overview
The Resume ATS Scorer uses a multi-dimensional approach to evaluate resumes against job requirements. The total score is 100 points, distributed across different aspects of the resume.

## Scoring Components

### 1. Content Match (50 points)
- **Keyword Matching (30 points)**
  - Exact matches with job requirements: 2 points each
  - Related/synonym matches: 1 point each
  - Industry-specific terminology: 1.5 points each
  - Maximum of 30 points

- **Experience Relevance (20 points)**
  - Years of relevant experience: 10 points
  - Project relevance: 10 points

### 2. Format Compatibility (30 points)
- **Document Structure (15 points)**
  - Proper section headers: 5 points
  - Consistent formatting: 5 points
  - Clear hierarchy: 5 points

- **ATS-Friendly Elements (15 points)**
  - Standard fonts: 5 points
  - No tables/images: 5 points
  - Proper spacing: 5 points

### 3. Section-Specific Scores (20 points)
- **Professional Summary (5 points)**
  - Clarity and relevance: 5 points

- **Work Experience (7 points)**
  - Achievement-oriented descriptions: 4 points
  - Quantifiable results: 3 points

- **Skills Section (5 points)**
  - Technical skills alignment: 3 points
  - Soft skills relevance: 2 points

- **Education (3 points)**
  - Degree relevance: 2 points
  - Additional certifications: 1 point

## Example Scoring

### Example 1: Software Engineer Position
```
Job Requirements:
- Python programming (5 years)
- Django framework
- REST API development
- AWS experience

Resume Content:
- 4 years Python experience
- 2 years Django
- REST API projects
- No AWS experience

Score Breakdown:
- Content Match: 35/50
  - Keyword Matching: 20/30
  - Experience Relevance: 15/20
- Format Compatibility: 25/30
- Section-Specific: 18/20
Total Score: 78/100
```

### Example 2: Marketing Manager Position
```
Job Requirements:
- Digital marketing strategy
- Social media management
- Content creation
- Analytics experience

Resume Content:
- Strong digital marketing background
- Social media campaigns
- Content strategy
- Google Analytics certified

Score Breakdown:
- Content Match: 45/50
  - Keyword Matching: 28/30
  - Experience Relevance: 17/20
- Format Compatibility: 28/30
- Section-Specific: 19/20
Total Score: 92/100
```

## Improvement Recommendations
The system provides specific recommendations based on score components:
1. Content Match < 40: Focus on aligning skills and experience
2. Format Compatibility < 25: Improve document structure
3. Section-Specific < 15: Enhance section content and organization

## Notes
- Scores are weighted based on job level and industry
- Minimum passing score is typically 70/100
- Recommendations are prioritized based on score impact 
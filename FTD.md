# Resume ATS Score Checker Project - Functional and Technical Design Document

## 1. Introduction

This document outlines the functional and technical design for a Resume ATS (Applicant Tracking System) Score Checker project. The goal is to build an MVP (Minimum Viable Product) that can parse resumes and job descriptions, match them, generate a score reflecting ATS compatibility, and provide recommendations for improvement.  The project will leverage CrewAI for multi-agent collaboration and FastAPI for building a scalable RESTful API.

## 2. Goals

*   Develop a system that accurately assesses resume compatibility with ATS systems.
*   Provide users with actionable feedback to improve their resume's ATS score.
*   Create a scalable and maintainable application using modern Python development practices.
*   Package and deploy the application using Docker for easy distribution and deployment.

## 3. User Stories

(Refer to the user stories provided in the prompt.  They are the foundation of this design.)

## 4. Functional Design

### 4.1. Core Components

*   **Resume Parser Agent:**
    *   **Functionality:** Extracts text content from resume files in PDF, DOCX, and HTML formats.
    *   **Input:** Resume file (PDF, DOCX, HTML).
    *   **Output:** Plain text representation of the resume content.
    *   **Libraries:** `unstructured`, `docling`, `PyPDF2`, `python-docx`, `beautifulsoup4`.
*   **Resume Keyword Analyst Agent:**
    *   **Functionality:** Identifies and extracts relevant keywords from the parsed resume text.
    *   **Input:** Plain text resume content (output from Resume Parser).
    *   **Output:** List of keywords with associated frequencies or weights.
    *   **Techniques:** Natural Language Processing (NLP) techniques like TF-IDF, keyword extraction algorithms (e.g., RAKE, YAKE), and potentially pre-trained language models.
*   **Job Description Parser Agent:**
    *   **Functionality:** Extracts key requirements and keywords from job descriptions obtained from sources like Naukri and LinkedIn.
    *   **Input:** Job description text (from web scraping or API).
    *   **Output:** List of key requirements and keywords.
    *   **Web Scraping:** Use libraries like `BeautifulSoup4` and `requests` to scrape job descriptions from websites.  Consider using APIs if available.
    *   **Handling Variations:** Implement robust parsing logic to handle variations in job description formats.
*   **Matching Algorithm:**
    *   **Functionality:** Compares the extracted resume keywords and content against the job requirements.
    *   **Input:** List of resume keywords, plain text resume content, list of job requirements, and job description text.
    *   **Output:** A match score and a list of matched/unmatched keywords and requirements.
    *   **Algorithm:**  Implement a similarity scoring algorithm (e.g., cosine similarity, Jaccard index) based on keyword matching.  Consider incorporating semantic similarity using word embeddings (e.g., Word2Vec, GloVe, or Sentence Transformers).
*   **Scoring System:**
    *   **Functionality:** Generates a numeric score (out of 100) based on keyword matching and formatting analysis.
    *   **Input:** Matching algorithm results, resume format analysis results.
    *   **Output:** A numeric score (0-100) and a detailed breakdown of the score calculation.
    *   **Multi-Dimensional Approach:**
        *   **Content Match:**  Weighted score based on the percentage of job requirements matched by the resume content.
        *   **Format Compatibility:**  Score based on the resume's adherence to ATS-friendly formatting guidelines (e.g., use of standard headings, bullet points, avoiding tables and images).
        *   **Section-Specific Scores:**  Scores for key resume sections (Skills, Experience, Education) based on the relevance and completeness of the information.
    *   **Weighting:** The weights for each dimension (Content Match, Format Compatibility, Section-Specific Scores) will be configurable.
*   **Recommendation Engine:**
    *   **Functionality:** Suggests improvements and feedback to increase ATS compatibility.
    *   **Input:** Scoring system results, resume content, job description.
    *   **Output:** A list of prioritized recommendations with explanations.
    *   **Recommendations:**
        *   Keyword optimization: Suggest adding missing keywords or rephrasing existing ones.
        *   Formatting improvements:  Suggest using standard headings, bullet points, and avoiding tables and images.
        *   Content enhancements:  Suggest adding more details to specific sections (e.g., Skills, Experience) to better match the job requirements.

### 4.2. Workflow

1.  The user uploads a resume file (PDF, DOCX, or HTML) and provides a job description (either by uploading a file or providing a URL).
2.  The **Resume Parser Agent** extracts the text content from the resume.
3.  The **Resume Keyword Analyst Agent** identifies and extracts keywords from the parsed resume text.
4.  The **Job Description Parser Agent** extracts key requirements and keywords from the job description.
5.  The **Matching Algorithm** compares the extracted resume content and keywords against the job requirements.
6.  The **Scoring System** generates a numeric score based on the matching results and formatting analysis.
7.  The **Recommendation Engine** suggests improvements and feedback to increase ATS compatibility.
8.  The system displays the ATS score, a breakdown of the score calculation, and a list of recommendations to the user.

## 5. Technical Design

### 5.1. Architecture

The application will follow a modular, multi-agent architecture using CrewAI and FastAPI.

*   **Programming Language:** Python 3.12
*   **Frameworks:**
    *   **FastAPI:** For building RESTful APIs.
    *   **CrewAI (version 0.114):** For multi-agent orchestration and collaboration.
    *   **Pydantic (V2 = 2.11):** For data validation and serialization.
*   **Libraries:**
    *   `unstructured`, `docling`, `PyPDF2`, `python-docx`, `beautifulsoup4`, `requests`, `nltk`, `scikit-learn`, `sentence-transformers` (and others as needed).
*   **Database (Optional for MVP):**  Consider using a lightweight database like SQLite or PostgreSQL for storing resumes, job descriptions, and scoring results.  For the MVP, in-memory data structures might suffice.
*   **Containerization:** Docker
*   **Deployment:** DockerHub

### 5.2. API Endpoints (FastAPI)

*   `/parse_resume` (POST): Accepts a resume file and returns the extracted text content.
*   `/extract_keywords_resume` (POST): Accepts resume text and returns a list of keywords.
*   `/parse_job_description` (POST): Accepts a job description (text or URL) and returns the extracted requirements.
*   `/match` (POST): Accepts resume text and job description text and returns the match score and details.
*   `/score` (POST): Accepts resume text and job description text and returns the ATS score, breakdown, and recommendations.

### 5.3. Agent Implementation (CrewAI)

The following agents will be implemented using CrewAI:

*   **Resume Parser Agent:** Responsible for parsing resume files.
*   **Resume Keyword Analyst Agent:** Responsible for extracting keywords from resumes.
*   **Job Description Parser Agent:** Responsible for parsing job descriptions.
*   **Matcher Agent:** Responsible for comparing resumes and job descriptions.
*   **Scorer Agent:** Responsible for calculating the ATS score.
*   **Recommender Agent:** Responsible for generating recommendations.

The CrewAI framework will be used to define the roles, goals, and tools for each agent, and to orchestrate their collaboration.

### 5.4. Data Structures

*   **Resume:**
    *   `file_name`: String
    *   `file_type`: String (PDF, DOCX, HTML)
    *   `text_content`: String
    *   `keywords`: List of Strings
*   **JobDescription:**
    *   `source`: String (e.g., Naukri, LinkedIn)
    *   `text_content`: String
    *   `requirements`: List of Strings
    *   `keywords`: List of Strings
*   **MatchResult:**
    *   `resume_id`: Integer (or UUID)
    *   `job_description_id`: Integer (or UUID)
    *   `match_score`: Float (0-1)
    *   `matched_keywords`: List of Strings
    *   `unmatched_keywords`: List of Strings
    *   `matched_requirements`: List of Strings
    *   `unmatched_requirements`: List of Strings
*   **ATSScore:**
    *   `resume_id`: Integer (or UUID)
    *   `job_description_id`: Integer (or UUID)
    *   `total_score`: Integer (0-100)
    *   `content_match_score`: Integer (0-100)
    *   `format_compatibility_score`: Integer (0-100)
    *   `section_specific_scores`: Dictionary (e.g., `{'Skills': 80, 'Experience': 90, 'Education': 75}`)
    *   `recommendations`: List of Strings

### 5.5. Technology Stack

*   **Python 3.12:** Core programming language.
*   **FastAPI:** REST API framework.
*   **CrewAI (0.114):** Multi-agent framework.
*   **Pydantic (2.11):** Data validation and settings management.
*   **Unstructured, Docling, PyPDF2, python-docx, BeautifulSoup4:** Document parsing libraries.
*   **NLTK, scikit-learn, sentence-transformers:** NLP libraries for keyword extraction and semantic similarity.
*   **Requests:** For making HTTP requests (e.g., web scraping).
*   **Docker:** Containerization.
*   **DockerHub:** Container registry.
*   **Logging:** Python's built-in `logging` module.

### 5.6. Development Standards

*   **PEP8:** Adhere to PEP8 coding style guidelines.
*   **Modular Coding:** Follow a modular coding approach with clear separation of concerns.
*   **Logging:** Implement comprehensive logging using the Python `logging` module.
*   **Version Control:** Use Git for version control.
*   **Testing:** Implement unit tests and integration tests.

### 5.7. Deployment

1.  Create a Dockerfile to containerize the application.
2.  Build a Docker image from the Dockerfile.
3.  Push the Docker image to a public DockerHub repository.
4.  Deploy the Docker image to a suitable environment (e.g., cloud platform, server).

## 6. Scoring Mechanism Documentation

A separate document will be created to explain the scoring mechanism in detail, including:

*   The different dimensions of the scoring system (Content Match, Format Compatibility, Section-Specific Scores).
*   The weighting of each dimension.
*   How each dimension is calculated.
*   Examples of how different resume characteristics affect the score.
*   Information on how to interpret the ATS score.

## 7. Project Setup and Dependencies

1.  **Python 3.12:** Ensure Python 3.12 is installed.
2.  **Virtual Environment:** Create a virtual environment using `venv` or `conda`.
3.  **requirements.txt:** Create a `requirements.txt` file listing all project dependencies with specific versions.  Use `pip freeze > requirements.txt` to generate the file after installing the dependencies.
4.  **Install Dependencies:** Install the dependencies using `pip install -r requirements.txt`.

## 8. Future Enhancements

*   Integration with more job board APIs (e.g., Indeed, Monster).
*   More sophisticated NLP techniques for keyword extraction and semantic similarity.
*   Support for more resume formats.
*   Personalized recommendations based on user profiles.
*   A user interface (UI) for uploading resumes and viewing results.
*   Implement user authentication and authorization.
*   Implement caching mechanisms to improve performance.

## 9. Open Issues

*   The specific weights for the scoring dimensions need to be determined through experimentation and analysis.
*   The web scraping logic for job descriptions needs to be robust and adaptable to changes in website layouts.
*   The performance of the matching algorithm needs to be optimized for large datasets.

This document provides a comprehensive overview of the functional and technical design for the Resume ATS Score Checker project. It will be used as a guide for development and will be updated as needed.


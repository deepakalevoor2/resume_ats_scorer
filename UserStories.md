Implement Resume Parser Agent
Description: As a user, I want the system to be able to parse resumes in PDF, DOCX, and HTML formats so that the text content can be extracted for analysis.
Acceptance Criteria:

The system can successfully extract text from PDF, DOCX, and HTML resume files.

The extracted text is accurate and preserves the original content’s meaning.

The parser utilizes libraries like unstructured and docling for efficient parsing.

The agent handles common parsing errors gracefully and logs them appropriately.

The agent is implemented as a modular component within the CrewAI framework.
Priority: High
Status: To Do

Implement Resume Keyword Analyst Agent
Description: As a user, I want the system to be able to identify and extract relevant keywords from the parsed resume text so that these keywords can be used for matching against job descriptions.
Acceptance Criteria:

The system can accurately identify and extract keywords from the parsed resume text.

The keyword extraction process is efficient and scalable.

The agent is implemented as a modular component within the CrewAI framework.

The extracted keywords are stored in a structured format for further processing.
Priority: High
Status: To Do

Implement Job Description Parser Agent
Description: As a user, I want the system to be able to parse job descriptions from sources like Naukri and LinkedIn so that key requirements can be extracted for matching against resumes.
Acceptance Criteria:

The system can successfully extract key requirements from job descriptions obtained from Naukri, LinkedIn, or similar sources.

The parser can handle variations in job description formats.

The agent is implemented as a modular component within the CrewAI framework.

The extracted requirements are stored in a structured format for further processing.
Priority: High
Status: To Do

Implement Matching Algorithm
Description: As a user, I want the system to compare the extracted resume content against the job requirements so that a match score can be generated.
Acceptance Criteria:

The system can accurately compare resume content against job requirements.

The matching algorithm considers keyword similarity, context, and relevance.

The algorithm is efficient and scalable to handle a large number of resumes and job descriptions.

The matching results are stored in a structured format for scoring.
Priority: High
Status: To Do

Implement Scoring System with Multi‑Dimensional Approach
Description: As a user, I want the system to generate a numeric score based on keyword matching and formatting analysis, using a multi‑dimensional approach that evaluates content match, format compatibility, and section‑specific scores.
Acceptance Criteria:

The system generates a numeric score (out of 100) based on keyword matching and formatting analysis.

The scoring system uses a multi‑dimensional approach, evaluating content match, format compatibility, and section‑specific scores.

The scoring system is configurable, allowing for adjustments to weighting of different dimensions.

The system provides a clear explanation of how the score is calculated.

Section‑specific scores are calculated for key resume sections (e.g., Skills, Experience, Education).
Priority: High
Status: To Do

Create Scoring Mechanism Documentation
Description: As a user, I want a document explaining the scoring mechanism with examples so that I can understand how the ATS score is calculated.
Acceptance Criteria:

The document clearly explains the scoring mechanism, including the weighting of different dimensions.

The document provides examples of how different resume characteristics affect the score.

The document is well‑organized and easy to understand.

The document includes information on how to interpret the ATS score.
Priority: Medium
Status: To Do

Implement Recommendation Engine
Description: As a user, I want the system to suggest improvements and feedback to increase ATS compatibility so that I can optimize my resume.
Acceptance Criteria:

The system provides specific and actionable recommendations for improving ATS compatibility.

The recommendations are tailored to the specific resume and job description.

The recommendations are prioritized based on their potential impact on the ATS score.

The system provides explanations for why each recommendation is being made.
Priority: High
Status: To Do

Set up Project with Python 3.12
Description: As a developer, I need to set up the project to use Python 3.12 so that I can utilize the latest language features and improvements.
Acceptance Criteria:

The project is configured to use Python 3.12.

All dependencies are compatible with Python 3.12.

The project can be run successfully using Python 3.12.
Priority: High
Status: To Do

Implement Logging Module
Description: As a developer, I need to implement a proper logging module for log tracing so that I can effectively debug and monitor the application.
Acceptance Criteria:

A logging module is implemented to track application events and errors.

Log messages include relevant information such as timestamp, log level, and source code location.

Log levels (e.g., DEBUG, INFO, WARNING, ERROR) are used appropriately.

Logs are stored in a persistent location for analysis.

Sensitive information is not logged.
Priority: High
Status: To Do

Create requirements.txt File
Description: As a developer, I need to create a requirements.txt file so that all project dependencies can be easily installed.
Acceptance Criteria:

A requirements.txt file is created that lists all project dependencies.

The file includes specific versions for each dependency to ensure reproducibility.

The file is up‑to‑date and accurately reflects all project dependencies.
Priority: High
Status: To Do

Adhere to PEP8 Coding Standards
Description: As a developer, I need to follow all PEP8 rules of Python so that the code is consistent and readable.
Acceptance Criteria:

The codebase adheres to PEP8 coding standards.

Code is properly formatted and indented.

Variable and function names are descriptive and follow naming conventions.

Code is reviewed to ensure compliance with PEP8 standards.
Priority: High
Status: To Do

Implement Modular Coding Approach
Description: As a developer, I need to follow a modular coding approach so that the codebase is well‑organized and maintainable.
Acceptance Criteria:

The codebase is divided into modular components with clear responsibilities.

Modules are loosely coupled and communicate through well‑defined interfaces.

Code is reusable and easy to test.

The project structure promotes maintainability and scalability.
Priority: High
Status: To Do

Build Scalable RESTful APIs using FastAPI
Description: As a developer, I need to build scalable RESTful APIs using FastAPI so that the system can be accessed and integrated with other applications.
Acceptance Criteria:

RESTful APIs are built using FastAPI.

APIs are well‑documented and follow RESTful principles.

APIs are scalable and can handle a large number of requests.

APIs include appropriate authentication and authorization mechanisms.

API endpoints are defined for key functionalities (e.g., resume parsing, job description parsing, scoring).
Priority: High
Status: To Do

Create a PYPI Python Package
Description: As a developer, I need to create a PYPI Python package so that the system can be easily installed and distributed.
Acceptance Criteria:

A PYPI package is created for the project.

The package includes all necessary code and resources.

The package can be installed using pip.

The package is well‑documented and includes installation instructions.
Priority: Medium
Status: To Do

Create Dockerfile
Description: As a developer, I need to create a Dockerfile so that the application can be easily containerized.
Acceptance Criteria:

A Dockerfile is created for the project.

The Dockerfile specifies the base image, dependencies, and application code.

The Dockerfile builds a Docker image that can run the application.

The Docker image is optimized for size and performance.
Priority: High
Status: To Do

Dockerize the App & Upload Image to DockerHub
Description: As a developer, I need to dockerize the app and upload the image to DockerHub so that it can be easily deployed and shared.
Acceptance Criteria:

The application is successfully dockerized.

A Docker image is created and pushed to a public DockerHub repository.

The DockerHub repository includes clear instructions on how to run the image.

The Docker image is up‑to‑date and reflects the latest version of the application.
Priority: High
Status: To Do

Implement CrewAI Framework
Description: As a developer, I need to implement CrewAI framework version 0.114 and Pydantic V2 = 2.11 so that the agents can communicate and collaborate effectively.
Acceptance Criteria:

The project uses CrewAI version 0.114 and Pydantic V2 = 2.11.

Agents are defined and configured within the CrewAI framework.

Agents can communicate and collaborate to achieve the project goals.

The CrewAI framework is properly integrated and functioning as expected.
Priority: High
Status: To Do
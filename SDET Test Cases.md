🤖 AIMessage

AI is now acting as Software Development Engineer in Test (SDET) and creating test cases. Here are the generated test cases: Okay, I will write test cases based on the user stories, functional and technical design, and security review comments. I will prioritize testing the core functionalities and security aspects.

Here are the test cases:

I. Resume Parser Agent Test Cases

RP_001: Successful PDF Parsing
Description: Verify that the agent can successfully extract text from a valid PDF resume file.
Steps:
Upload a valid PDF resume file.
Call the parse_resume API endpoint.
Verify that the API returns a 200 OK status code.
Verify that the response contains the extracted text content.
Verify that the extracted text is accurate and preserves the original content's meaning.
Expected Result: The agent successfully extracts text from the PDF resume file, and the extracted text is accurate.
Acceptance Criteria: "The system can successfully extract text from PDF resume files." and "The extracted text is accurate and preserves the original content's meaning."
RP_002: Successful DOCX Parsing
Description: Verify that the agent can successfully extract text from a valid DOCX resume file.
Steps:
Upload a valid DOCX resume file.
Call the parse_resume API endpoint.
Verify that the API returns a 200 OK status code.
Verify that the response contains the extracted text content.
Verify that the extracted text is accurate and preserves the original content's meaning.
Expected Result: The agent successfully extracts text from the DOCX resume file, and the extracted text is accurate.
Acceptance Criteria: "The system can successfully extract text from DOCX resume files." and "The extracted text is accurate and preserves the original content's meaning."
RP_003: Successful HTML Parsing
Description: Verify that the agent can successfully extract text from a valid HTML resume file.
Steps:
Upload a valid HTML resume file.
Call the parse_resume API endpoint.
Verify that the API returns a 200 OK status code.
Verify that the response contains the extracted text content.
Verify that the extracted text is accurate and preserves the original content's meaning.
Expected Result: The agent successfully extracts text from the HTML resume file, and the extracted text is accurate.
Acceptance Criteria: "The system can successfully extract text from HTML resume files." and "The extracted text is accurate and preserves the original content's meaning."
RP_004: Invalid File Type
Description: Verify that the agent handles invalid file types gracefully.
Steps:
Upload a file with an invalid file type (e.g., TXT, JPG).
Call the parse_resume API endpoint.
Verify that the API returns a 400 Bad Request status code.
Verify that the response contains an appropriate error message.
Verify that the error is logged.
Expected Result: The agent rejects the invalid file type and returns an appropriate error message.
Acceptance Criteria: "The agent handles common parsing errors gracefully and logs them appropriately."
RP_005: Corrupted File
Description: Verify that the agent handles corrupted files gracefully.
Steps:
Upload a corrupted PDF, DOCX, or HTML file.
Call the parse_resume API endpoint.
Verify that the API returns a 500 Internal Server Error status code.
Verify that the response contains an appropriate error message.
Verify that the error is logged.
Expected Result: The agent handles the corrupted file gracefully and returns an appropriate error message.
Acceptance Criteria: "The agent handles common parsing errors gracefully and logs them appropriately."
RP_006: File Size Limit
Description: Verify that the agent enforces a file size limit.
Steps:
Upload a file exceeding the maximum allowed file size.
Call the parse_resume API endpoint.
Verify that the API returns a 413 Payload Too Large status code.
Verify that the response contains an appropriate error message.
Verify that the error is logged.
Expected Result: The agent rejects the file exceeding the size limit and returns an appropriate error message.
Acceptance Criteria: Implied by the need to prevent DoS attacks (Security Review).
RP_007: ClamAV Scan - Clean File
Description: Verify that the ClamAV scan passes for a clean file.
Steps:
Upload a clean PDF, DOCX, or HTML file.
Call the parse_resume API endpoint.
Verify that the API returns a 200 OK status code.
Verify that the response contains the extracted text content.
Expected Result: The ClamAV scan passes, and the agent processes the file.
Acceptance Criteria: Implied by the need for virus scanning (Security Review).
RP_008: ClamAV Scan - Infected File
Description: Verify that the ClamAV scan detects an infected file.
Steps:
Upload a PDF, DOCX, or HTML file containing a virus (use a test virus).
Call the parse_resume API endpoint.
Verify that the API returns a 400 Bad Request or 500 Internal Server Error status code.
Verify that the response contains an appropriate error message indicating a virus was detected.
Verify that the error is logged.
Expected Result: The ClamAV scan detects the virus, and the agent rejects the file.
Acceptance Criteria: Implied by the need for virus scanning (Security Review).
RP_009: Secure Filename Generation
Description: Verify that the agent generates a secure filename for uploaded files.
Steps:
Upload a file with a potentially malicious filename (e.g., containing spaces, special characters, or command injection attempts).
Call the parse_resume API endpoint.
Verify that the file is saved with a secure, generated filename (UUID).
Verify that the system functions correctly despite the original filename.
Expected Result: The agent generates a secure filename, preventing filename-based attacks.
Acceptance Criteria: "The ResumeParserAgent uses generate_secure_filename to prevent filename-based attacks." (Security Review).
II. Resume Keyword Analyst Agent Test Cases

RKA_001: Keyword Extraction from Valid Resume Text
Description: Verify that the agent can accurately extract keywords from valid resume text.
Steps:
Provide valid resume text as input to the extract_keywords_resume API endpoint.
Verify that the API returns a 200 OK status code.
Verify that the response contains a list of keywords.
Verify that the extracted keywords are relevant to the resume text.
Expected Result: The agent accurately extracts relevant keywords from the resume text.
Acceptance Criteria: "The system can accurately identify and extract keywords from the parsed resume text."
RKA_002: Keyword Extraction with Empty Resume Text
Description: Verify that the agent handles empty resume text gracefully.
Steps:
Provide empty resume text as input to the extract_keywords_resume API endpoint.
Verify that the API returns a 200 OK status code.
Verify that the response contains an empty list of keywords or an appropriate message.
Expected Result: The agent handles empty resume text gracefully and returns an empty list of keywords or an appropriate message.
Acceptance Criteria: "The keyword extraction process is efficient and scalable." (Handles edge cases).
RKA_003: Keyword Extraction with Special Characters
Description: Verify that the agent handles special characters in the resume text correctly.
Steps:
Provide resume text containing special characters as input to the extract_keywords_resume API endpoint.
Verify that the API returns a 200 OK status code.
Verify that the extracted keywords are accurate and do not contain unwanted special characters.
Expected Result: The agent handles special characters correctly and extracts accurate keywords.
Acceptance Criteria: Implied by the need for accurate keyword extraction.
RKA_004: Keyword Extraction - Large Resume Text
Description: Verify that the agent can handle large resume texts efficiently.
Steps:
Provide a large resume text as input to the extract_keywords_resume API endpoint.
Verify that the API returns a 200 OK status code.
Measure the time taken for keyword extraction.
Verify that the keyword extraction process is completed within an acceptable time frame.
Expected Result: The agent extracts keywords from the large resume text efficiently.
Acceptance Criteria: "The keyword extraction process is efficient and scalable."
RKA_005: Keyword Extraction - Input Sanitization
Description: Verify that the agent sanitizes the input text to prevent prompt injection.
Steps:
Provide resume text containing potentially malicious content (e.g., prompt injection attempts) as input to the extract_keywords_resume API endpoint.
Verify that the API returns a 200 OK status code.
Verify that the extracted keywords do not reflect the injected prompt.
Verify that the agent's behavior is not influenced by the injected prompt.
Expected Result: The agent sanitizes the input text and prevents prompt injection.
Acceptance Criteria: "Implement input validation and sanitization to remove potentially malicious content from the resume and job description text before passing it to the agents." (Security Review).
III. Job Description Parser Agent Test Cases

JDP_001: Successful Parsing from Text Input
Description: Verify that the agent can successfully extract key requirements from a job description provided as text input.
Steps:
Provide a job description as text input to the parse_job_description API endpoint.
Verify that the API returns a 200 OK status code.
Verify that the response contains a list of key requirements.
Verify that the extracted requirements are relevant to the job description.
Expected Result: The agent successfully extracts key requirements from the job description text.
Acceptance Criteria: "The system can successfully extract key requirements from job descriptions obtained from Naukri, LinkedIn, or similar sources."
JDP_002: Successful Parsing from URL (Naukri)
Description: Verify that the agent can successfully extract key requirements from a job description URL from Naukri.
Steps:
Provide a valid Naukri job description URL to the parse_job_description API endpoint.
Verify that the API returns a 200 OK status code.
Verify that the response contains a list of key requirements.
Verify that the extracted requirements are relevant to the job description.
Expected Result: The agent successfully extracts key requirements from the Naukri job description URL.
Acceptance Criteria: "The system can successfully extract key requirements from job descriptions obtained from Naukri, LinkedIn, or similar sources."
JDP_003: Successful Parsing from URL (LinkedIn)
Description: Verify that the agent can successfully extract key requirements from a job description URL from LinkedIn.
Steps:
Provide a valid LinkedIn job description URL to the parse_job_description API endpoint.
Verify that the API returns a 200 OK status code.
Verify that the response contains a list of key requirements.
Verify that the extracted requirements are relevant to the job description.
Expected Result: The agent successfully extracts key requirements from the LinkedIn job description URL.
Acceptance Criteria: "The system can successfully extract key requirements from job descriptions obtained from Naukri, LinkedIn, or similar sources."
JDP_004: Invalid Job Description URL
Description: Verify that the agent handles invalid job description URLs gracefully.
Steps:
Provide an invalid job description URL to the parse_job_description API endpoint.
Verify that the API returns a 400 Bad Request or 500 Internal Server Error status code.
Verify that the response contains an appropriate error message.
Verify that the error is logged.
Expected Result: The agent handles the invalid job description URL gracefully and returns an appropriate error message.
Acceptance Criteria: "The parser can handle variations in job description formats." (Handles invalid URLs).
JDP_005: Job Description Not Found (404)
Description: Verify that the agent handles job description URLs that return a 404 error.
Steps:
Provide a job description URL that returns a 404 error to the parse_job_description API endpoint.
Verify that the API returns a 400 Bad Request or 500 Internal Server Error status code.
Verify that the response contains an appropriate error message.
Verify that the error is logged.
Expected Result: The agent handles the 404 error gracefully and returns an appropriate error message.
Acceptance Criteria: "The parser can handle variations in job description formats." (Handles 404 errors).
JDP_006: Web Scraping - Robots.txt Respect
Description: Verify that the agent respects the robots.txt file when scraping job descriptions.
Steps:
Provide a job description URL from a website that disallows scraping in its robots.txt file to the parse_job_description API endpoint.
Verify that the API returns a 403 Forbidden or 500 Internal Server Error status code.
Verify that the response contains an appropriate error message.
Verify that the error is logged.
Expected Result: The agent respects the robots.txt file and does not scrape the job description.
Acceptance Criteria: "The JobDescriptionParserAgent checks robots.txt before scraping." (Security Review).
JDP_007: Web Scraping - User-Agent Rotation
Description: Verify that the agent uses a variety of User-Agent strings to avoid being blocked.
Steps:
Repeatedly call the parse_job_description API endpoint with different job description URLs from the same website.
Monitor the User-Agent strings used in the HTTP requests.
Verify that the agent uses a different User-Agent string for each request.
Expected Result: The agent rotates User-Agent strings to avoid being blocked.
Acceptance Criteria: "It uses a list of User-Agent strings to avoid being blocked." (Security Review).
JDP_008: Web Scraping - Timeout Handling
Description: Verify that the agent handles timeouts when scraping job descriptions.
Steps:
Provide a job description URL that is known to be slow or unresponsive to the parse_job_description API endpoint.
Verify that the API returns a 500 Internal Server Error status code after a certain timeout period.
Verify that the response contains an appropriate error message.
Verify that the error is logged.
Expected Result: The agent handles timeouts gracefully and returns an appropriate error message.
Acceptance Criteria: "It sets a timeout for HTTP requests to prevent hanging." (Security Review).
JDP_009: Input Sanitization - Job Description Text
Description: Verify that the agent sanitizes the job description text to prevent prompt injection.
Steps:
Provide a job description text containing potentially malicious content (e.g., prompt injection attempts) as input to the parse_job_description API endpoint.
Verify that the API returns a 200 OK status code.
Verify that the extracted requirements do not reflect the injected prompt.
Verify that the agent's behavior is not influenced by the injected prompt.
Expected Result: The agent sanitizes the input text and prevents prompt injection.
Acceptance Criteria: "Implement input validation and sanitization to remove potentially malicious content from the resume and job description text before passing it to the agents." (Security Review).
IV. Matching Algorithm Test Cases

MA_001: Successful Matching - High Similarity
Description: Verify that the matching algorithm returns a high match score when the resume and job description have high similarity.
Steps:
Provide a resume and job description with high similarity to the match API endpoint.
Verify that the API returns a 200 OK status code.
Verify that the response contains a match score close to 1.0.
Verify that the response contains a list of matched keywords and requirements.
Expected Result: The matching algorithm returns a high match score and identifies the matched keywords and requirements.
Acceptance Criteria: "The system can accurately compare resume content against job requirements."
MA_002: Successful Matching - Low Similarity
Description: Verify that the matching algorithm returns a low match score when the resume and job description have low similarity.
Steps:
Provide a resume and job description with low similarity to the match API endpoint.
Verify that the API returns a 200 OK status code.
Verify that the response contains a match score close to 0.0.
Verify that the response contains a list of unmatched keywords and requirements.
Expected Result: The matching algorithm returns a low match score and identifies the unmatched keywords and requirements.
Acceptance Criteria: "The system can accurately compare resume content against job requirements."
MA_003: Matching with Empty Resume
Description: Verify that the matching algorithm handles an empty resume gracefully.
Steps:
Provide an empty resume and a valid job description to the match API endpoint.
Verify that the API returns a 200 OK status code.
Verify that the response contains a match score close to 0.0.
Verify that the response contains a list of unmatched keywords and requirements.
Expected Result: The matching algorithm handles an empty resume gracefully and returns a low match score.
Acceptance Criteria: "The algorithm is efficient and scalable to handle a large number of resumes and job descriptions." (Handles edge cases).
MA_004: Matching with Empty Job Description
Description: Verify that the matching algorithm handles an empty job description gracefully.
Steps:
Provide a valid resume and an empty job description to the match API endpoint.
Verify that the API returns a 200 OK status code.
Verify that the response contains a match score close to 0.0.
Verify that the response contains a list of unmatched keywords and requirements.
Expected Result: The matching algorithm handles an empty job description gracefully and returns a low match score.
Acceptance Criteria: "The algorithm is efficient and scalable to handle a large number of resumes and job descriptions." (Handles edge cases).
MA_005: Matching - Keyword Similarity
Description: Verify that the matching algorithm considers keyword similarity when calculating the match score.
Steps:
Provide a resume and job description with similar keywords (e.g., "software engineer" vs. "software developer") to the match API endpoint.
Verify that the API returns a 200 OK status code.
Verify that the response contains a relatively high match score.
Verify that the response identifies the similar keywords as matches.
Expected Result: The matching algorithm considers keyword similarity and returns a higher match score.
Acceptance Criteria: "The matching algorithm considers keyword similarity, context, and relevance."
MA_006: Matching - Context and Relevance
Description: Verify that the matching algorithm considers context and relevance when calculating the match score.
Steps:
Provide a resume and job description where the same keyword has different meanings in different contexts to the match API endpoint.
Verify that the API returns a 200 OK status code.
Verify that the response contains a match score that reflects the relevance of the keyword in each context.
Expected Result: The matching algorithm considers context and relevance and returns an appropriate match score.
Acceptance Criteria: "The matching algorithm considers keyword similarity, context, and relevance."
MA_007: Matching - Large Datasets (Performance)
Description: Verify that the matching algorithm can handle large datasets efficiently.
Steps:
Create a large dataset of resumes and job descriptions.
Measure the time taken to match each resume against each job description.
Verify that the matching process is completed within an acceptable time frame.
Expected Result: The matching algorithm can handle large datasets efficiently.
Acceptance Criteria: "The algorithm is efficient and scalable to handle a large number of resumes and job descriptions."
V. Scoring System Test Cases

SS_001: Valid Score Generation
Description: Verify that the scoring system generates a valid numeric score (0-100) based on keyword matching and formatting analysis.
Steps:
Provide a resume and job description to the score API endpoint.
Verify that the API returns a 200 OK status code.
Verify that the response contains a total_score value between 0 and 100.
Expected Result: The scoring system generates a valid numeric score.
Acceptance Criteria: "The system generates a numeric score (out of 100) based on keyword matching and formatting analysis."
SS_002: Content Match Score Calculation
Description: Verify that the content match score is calculated correctly based on the percentage of job requirements matched by the resume content.
Steps:
Provide a resume and job description to the score API endpoint.
Analyze the resume and job description to determine the expected content match score.
Verify that the content_match_score in the API response matches the expected value.
Expected Result: The content match score is calculated correctly.
Acceptance Criteria: "The scoring system uses a multi-dimensional approach, evaluating content match..."
SS_003: Format Compatibility Score Calculation
Description: Verify that the format compatibility score is calculated correctly based on the resume's adherence to ATS-friendly formatting guidelines.
Steps:
Provide a resume and job description to the score API endpoint.
Analyze the resume's formatting to determine the expected format compatibility score.
Verify that the format_compatibility_score in the API response matches the expected value.
Expected Result: The format compatibility score is calculated correctly.
Acceptance Criteria: "The scoring system uses a multi-dimensional approach, evaluating ... format compatibility..."
SS_004: Section-Specific Scores Calculation
Description: Verify that section-specific scores are calculated for key resume sections (Skills, Experience, Education).
Steps:
Provide a resume and job description to the score API endpoint.
Verify that the response contains section_specific_scores for Skills, Experience, and Education.
Analyze the resume to determine the expected scores for each section.
Verify that the section_specific_scores in the API response match the expected values.
Expected Result: Section-specific scores are calculated correctly.
Acceptance Criteria: "Section-Specific Scores are calculated for key resume sections (e.g., Skills, Experience, Education)."
SS_005: Score Weighting Configuration
Description: Verify that the scoring system is configurable, allowing for adjustments to the weighting of different dimensions.
Steps:
Configure the weights for Content Match, Format Compatibility, and Section-Specific Scores.
Provide a resume and job description to the score API endpoint.
Verify that the total_score is calculated based on the configured weights.
Repeat the test with different weight configurations.
Expected Result: The scoring system is configurable, and the total score is calculated based on the configured weights.
Acceptance Criteria: "The scoring system is configurable, allowing for adjustments to weighting of different dimensions."
SS_006: Score Explanation
Description: Verify that the system provides a clear explanation of how the score is calculated.
Steps:
Provide a resume and job description to the score API endpoint.
Verify that the response includes a detailed breakdown of the score calculation, including the contribution of each dimension.
Expected Result: The system provides a clear explanation of how the score is calculated.
Acceptance Criteria: "The system provides a clear explanation of how the score is calculated."
VI. Recommendation Engine Test Cases

RE_001: Keyword Optimization Recommendations
Description: Verify that the system provides keyword optimization recommendations when the resume is missing relevant keywords.
Steps:
Provide a resume and job description to the score API endpoint.
Analyze the resume and job description to identify missing keywords.
Verify that the recommendations in the API response include suggestions for adding the missing keywords.
Expected Result: The system provides keyword optimization recommendations.
Acceptance Criteria: "The system provides specific and actionable recommendations for improving ATS compatibility."
RE_002: Formatting Improvement Recommendations
Description: Verify that the system provides formatting improvement recommendations when the resume has formatting issues.
Steps:
Provide a resume with formatting issues (e.g., use of tables, images, non-standard headings) and a job description to the score API endpoint.
Verify that the recommendations in the API response include suggestions for improving the resume's formatting.
Expected Result: The system provides formatting improvement recommendations.
Acceptance Criteria: "The system provides specific and actionable recommendations for improving ATS compatibility."
RE_003: Content Enhancement Recommendations
Description: Verify that the system provides content enhancement recommendations when the resume lacks sufficient details in specific sections.
Steps:
Provide a resume with insufficient details in specific sections (e.g., Skills, Experience) and a job description to the score API endpoint.
Verify that the recommendations in the API response include suggestions for adding more details to the relevant sections.
Expected Result: The system provides content enhancement recommendations.
Acceptance Criteria: "The system provides specific and actionable recommendations for improving ATS compatibility."
RE_004: Tailored Recommendations
Description: Verify that the recommendations are tailored to the specific resume and job description.
Steps:
Provide different resumes and job descriptions to the score API endpoint.
Verify that the recommendations in the API response are different for each resume and job description pair.
Expected Result: The recommendations are tailored to the specific resume and job description.
Acceptance Criteria: "The recommendations are tailored to the specific resume and job description."
RE_005: Prioritized Recommendations
Description: Verify that the recommendations are prioritized based on their potential impact on the ATS score.
Steps:
Provide a resume and job description to the score API endpoint.
Analyze the recommendations in the API response to determine their order.
Verify that the recommendations with the highest potential impact on the ATS score are listed first.
Expected Result: The recommendations are prioritized based on their potential impact on the ATS score.
Acceptance Criteria: "The recommendations are prioritized based on their potential impact on the ATS score."
RE_006: Recommendation Explanations
Description: Verify that the system provides explanations for why each recommendation is being made.
Steps:
Provide a resume and job description to the score API endpoint.
Verify that each recommendation in the API response includes an explanation of why it is being made.
Expected Result: The system provides explanations for each recommendation.
Acceptance Criteria: "The system provides explanations for why each recommendation is being made."
VII. Security Test Cases

SEC_001: API Key Protection
Description: Verify that the API key is not exposed in log messages or error messages.
Steps:
Call any API endpoint without providing a valid API key.
Verify that the API returns an appropriate error message.
Examine the log messages to ensure that the API key is not present.
Expected Result: The API key is not exposed in log messages or error messages.
Acceptance Criteria: "The sanitize_log_message function is used to redact sensitive information from log messages, which is important." (Security Review).
SEC_002: Rate Limiting
Description: Verify that rate limiting is implemented to prevent abuse of the API.
Steps:
Repeatedly call any API endpoint within a short period of time.
Verify that the API returns a 429 Too Many Requests status code after exceeding the rate limit.
Expected Result: Rate limiting is enforced, and the API returns a 429 error after exceeding the limit.
Acceptance Criteria: "Suggestion: Consider implementing rate limiting to prevent abuse of the API." (Security Review).
SEC_003: Input Validation - Malicious Input
Description: Verify that the system handles malicious input gracefully and does not crash or expose sensitive information.
Steps:
Provide malicious input (e.g., SQL injection attempts, cross-site scripting attacks) to any API endpoint.
Verify that the API returns an appropriate error message.
Verify that the system does not crash or expose sensitive information.
Expected Result: The system handles malicious input gracefully and does not crash or expose sensitive information.
Acceptance Criteria: "Prioritize input validation and sanitization to prevent prompt injection and other vulnerabilities." (Security Review).
SEC_004: Logging - Sensitive Information Redaction
Description: Verify that sensitive information (e.g., passwords, email addresses, phone numbers) is redacted from log messages.
Steps:
Perform actions that might generate log messages containing sensitive information.
Examine the log messages to ensure that sensitive information is redacted.
Expected Result: Sensitive information is redacted from log messages.
Acceptance Criteria: "The sanitize_log_message function is used to redact sensitive information from log messages." (Security Review).
SEC_005: Dependency Vulnerability Check
Description: Verify that the project dependencies are regularly updated to patch security vulnerabilities.
Steps:
Run a tool like pip-audit to check for known vulnerabilities in the project dependencies.
Update the dependencies to the latest versions.
Repeat the vulnerability check to ensure that the vulnerabilities have been patched.
Expected Result: The project dependencies are up-to-date and do not contain any known vulnerabilities.
Acceptance Criteria: "Regularly update dependencies to patch security vulnerabilities. Use a tool like pip-audit to check for known vulnerabilities in dependencies." (Security Review).
VIII. CrewAI Framework Test Cases

CA_001: Agent Communication
Description: Verify that the agents can communicate and collaborate effectively within the CrewAI framework.
Steps:
Run the entire workflow (resume parsing, keyword extraction, job description parsing, matching, scoring, recommendation).
Monitor the communication between the agents.
Verify that the agents are passing data and instructions to each other correctly.
Expected Result: The agents communicate and collaborate effectively.
Acceptance Criteria: "Agents can communicate and collaborate to achieve the project goals."
CA_002: Agent Task Execution
Description: Verify that each agent is executing its assigned tasks correctly.
Steps:
Run the entire workflow.
Monitor the actions performed by each agent.
Verify that each agent is performing its assigned tasks according to its role and goals.
Expected Result: Each agent executes its assigned tasks correctly.
Acceptance Criteria: "Agents are defined and configured within the CrewAI framework."
CA_003: CrewAI Version Compatibility
Description: Verify that the project is using the correct version of CrewAI (0.114) and Pydantic (V2 = 2.11).
Steps:
Check the requirements.txt file to ensure that the correct versions of CrewAI and Pydantic are specified.
Run the application and verify that it is using the specified versions of CrewAI and Pydantic.
Expected Result: The project is using the correct versions of CrewAI and Pydantic.
Acceptance Criteria: "The project uses CrewAI version 0.114 and Pydantic V2 = 2.11."
IX. Logging Test Cases

LG_001: Log Message Format
Description: Verify that log messages include relevant information such as timestamp, log level, and source code location.
Steps:
Perform various actions within the application.
Examine the log files to verify that log messages include the required information.
Expected Result: Log messages include timestamp, log level, and source code location.
Acceptance
🤖 AIMessage

AI is now acting as Software Development Engineer in Test (SDET) and creating test cases. Here are the generated test cases: Okay, I will generate test cases based on the user stories, functional and technical design, and security review comments. I will address the security concerns raised in the review.

Here are the test cases:

General Test Cases (Applicable to Multiple Components)

TC_GEN_001: Input Validation - Empty Input:
Description: Verify that the system handles empty input gracefully for all relevant API endpoints and agent functions.
Steps: Send an empty file or empty text string to the API endpoint or agent function.
Expected Result: The system returns an appropriate error message indicating that the input is invalid.
TC_GEN_002: Input Validation - Invalid Input Type:
Description: Verify that the system handles invalid input types gracefully for all relevant API endpoints and agent functions.
Steps: Send an input of the wrong data type (e.g., a number instead of a string) to the API endpoint or agent function.
Expected Result: The system returns an appropriate error message indicating that the input type is invalid.
TC_GEN_003: Logging - Correct Log Levels:
Description: Verify that log messages are written with the correct log levels (DEBUG, INFO, WARNING, ERROR).
Steps: Perform various actions in the system and check the log files to ensure that the log levels are appropriate for the events that occurred.
Expected Result: Log messages are written with the correct log levels.
TC_GEN_004: Logging - Sensitive Data Redaction:
Description: Verify that sensitive data is not logged or is properly redacted in log messages.
Steps: Perform actions that might involve sensitive data (e.g., uploading a resume with personal information) and check the log files to ensure that the data is not logged or is properly redacted.
Expected Result: Sensitive data is not logged or is properly redacted.
TC_GEN_005: Error Handling - Graceful Error Handling:
Description: Verify that the system handles errors gracefully and provides informative error messages to the user.
Steps: Simulate various error conditions (e.g., file not found, network error) and check that the system handles the errors gracefully and provides informative error messages.
Expected Result: The system handles errors gracefully and provides informative error messages.
TC_GEN_006: API Authentication - Invalid API Key:
Description: Verify that the API returns an error when an invalid API key is provided.
Steps: Send a request to an API endpoint with an invalid API key.
Expected Result: The API returns an error message indicating that the API key is invalid.
TC_GEN_007: API Authentication - No API Key:
Description: Verify that the API returns an error when no API key is provided.
Steps: Send a request to an API endpoint without an API key.
Expected Result: The API returns an error message indicating that an API key is required.
Resume Parser Agent Test Cases

TC_RP_001: File Parsing - PDF:
Description: Verify that the system can successfully extract text from a PDF resume file.
Steps: Upload a PDF resume file to the /parse_resume endpoint.
Expected Result: The system returns the extracted text content of the resume.
TC_RP_002: File Parsing - DOCX:
Description: Verify that the system can successfully extract text from a DOCX resume file.
Steps: Upload a DOCX resume file to the /parse_resume endpoint.
Expected Result: The system returns the extracted text content of the resume.
TC_RP_003: File Parsing - HTML:
Description: Verify that the system can successfully extract text from an HTML resume file.
Steps: Upload an HTML resume file to the /parse_resume endpoint.
Expected Result: The system returns the extracted text content of the resume.
TC_RP_004: File Parsing - Large File:
Description: Verify that the system handles large resume files gracefully.
Steps: Upload a large resume file (close to the max_file_size limit) to the /parse_resume endpoint.
Expected Result: The system successfully extracts the text content of the resume within a reasonable time frame.
TC_RP_005: File Parsing - File Size Limit Exceeded:
Description: Verify that the system rejects resume files that exceed the max_file_size limit.
Steps: Upload a resume file that exceeds the max_file_size limit to the /parse_resume endpoint.
Expected Result: The system returns an error message indicating that the file size exceeds the limit.
TC_RP_006: File Parsing - Invalid File Type:
Description: Verify that the system rejects resume files with invalid file types.
Steps: Upload a file with an invalid file type (e.g., a JPG image) to the /parse_resume endpoint.
Expected Result: The system returns an error message indicating that the file type is invalid.
TC_RP_007: File Parsing - Corrupted File:
Description: Verify that the system handles corrupted resume files gracefully.
Steps: Upload a corrupted resume file to the /parse_resume endpoint.
Expected Result: The system returns an error message indicating that the file is corrupted or cannot be parsed.
TC_RP_008: File Parsing - Malicious File (ClamAV):
Description: Verify that the system detects and rejects malicious resume files using ClamAV.
Steps: Upload a resume file containing a known virus signature to the /parse_resume endpoint.
Expected Result: The system detects the virus and returns an error message indicating that the file is malicious.
TC_RP_009: File Parsing - HTML with JavaScript:
Description: Verify that the system handles HTML files with JavaScript safely.
Steps: Upload an HTML resume file containing JavaScript code to the /parse_resume endpoint.
Expected Result: The system extracts the text content of the resume without executing the JavaScript code. The extracted text should not contain any JavaScript code.
TC_RP_010: File Parsing - File Extension Mismatch:
Description: Verify that the system validates file type based on content and not just extension.
Steps: Rename a .txt file to .pdf and upload it to the /parse_resume endpoint.
Expected Result: The system identifies the file as an invalid type based on its content and returns an appropriate error message.
Resume Keyword Analyst Agent Test Cases

TC_RKA_001: Keyword Extraction - Basic:
Description: Verify that the system can extract relevant keywords from a resume text.
Steps: Send a resume text to the /extract_keywords_resume endpoint.
Expected Result: The system returns a list of relevant keywords.
TC_RKA_002: Keyword Extraction - Empty Text:
Description: Verify that the system handles empty resume text gracefully.
Steps: Send an empty string to the /extract_keywords_resume endpoint.
Expected Result: The system returns an empty list of keywords or an appropriate error message.
TC_RKA_003: Keyword Extraction - Long Text:
Description: Verify that the system can extract keywords from a long resume text.
Steps: Send a long resume text to the /extract_keywords_resume endpoint.
Expected Result: The system returns a list of relevant keywords within a reasonable time frame.
TC_RKA_004: Keyword Extraction - Special Characters:
Description: Verify that the system handles special characters in the resume text correctly.
Steps: Send a resume text containing special characters to the /extract_keywords_resume endpoint.
Expected Result: The system returns a list of relevant keywords, handling the special characters appropriately.
Job Description Parser Agent Test Cases

TC_JDP_001: Job Description Parsing - Text Input:
Description: Verify that the system can extract key requirements from a job description provided as text input.
Steps: Send a job description text to the /parse_job_description endpoint.
Expected Result: The system returns a list of key requirements.
TC_JDP_002: Job Description Parsing - URL Input:
Description: Verify that the system can extract key requirements from a job description provided as a URL.
Steps: Send a job description URL to the /parse_job_description endpoint.
Expected Result: The system returns a list of key requirements.
TC_JDP_003: Job Description Parsing - Empty Input:
Description: Verify that the system handles empty job description input gracefully.
Steps: Send an empty string to the /parse_job_description endpoint.
Expected Result: The system returns an empty list of requirements or an appropriate error message.
TC_JDP_004: Job Description Parsing - Invalid URL:
Description: Verify that the system handles invalid job description URLs gracefully.
Steps: Send an invalid URL to the /parse_job_description endpoint.
Expected Result: The system returns an error message indicating that the URL is invalid.
TC_JDP_005: Job Description Parsing - Website Unreachable:
Description: Verify that the system handles cases where the job description website is unreachable.
Steps: Send a URL to a website that is currently down or unreachable to the /parse_job_description endpoint.
Expected Result: The system returns an error message indicating that the website is unreachable.
TC_JDP_006: Job Description Parsing - Robots.txt Disallow:
Description: Verify that the system respects robots.txt and does not scrape disallowed pages.
Steps: Create a simple web server with a robots.txt file that disallows scraping of a specific job description page. Send the URL of that page to the /parse_job_description endpoint.
Expected Result: The system does not scrape the page and returns an error message indicating that scraping is disallowed by robots.txt.
TC_JDP_007: Job Description Parsing - Website Structure Change:
Description: Verify that the system handles changes in website structure gracefully.
Steps: Use a URL to a job description on a website, and then manually change the website's HTML structure. Send the same URL to the /parse_job_description endpoint.
Expected Result: The system either successfully extracts the key requirements or returns an error message indicating that the website structure has changed and the parser needs to be updated.
TC_JDP_008: Job Description Parsing - Long Description:
Description: Verify that the system can parse a very long job description.
Steps: Send a very long job description to the /parse_job_description endpoint.
Expected Result: The system successfully extracts the key requirements within a reasonable time frame.
Matching Algorithm Test Cases

TC_MA_001: Matching - Exact Match:
Description: Verify that the system generates a high match score when the resume content exactly matches the job requirements.
Steps: Send a resume text and a job description text that are identical to the /match endpoint.
Expected Result: The system returns a high match score (close to 1.0).
TC_MA_002: Matching - Partial Match:
Description: Verify that the system generates a reasonable match score when the resume content partially matches the job requirements.
Steps: Send a resume text and a job description text that have some overlapping keywords and requirements to the /match endpoint.
Expected Result: The system returns a match score that reflects the degree of overlap between the resume and the job description.
TC_MA_003: Matching - No Match:
Description: Verify that the system generates a low match score when the resume content does not match the job requirements.
Steps: Send a resume text and a job description text that have no overlapping keywords or requirements to the /match endpoint.
Expected Result: The system returns a low match score (close to 0.0).
TC_MA_004: Matching - Keyword Order:
Description: Verify that the matching algorithm is not overly sensitive to the order of keywords.
Steps: Send a resume text and a job description text that contain the same keywords but in different orders to the /match endpoint.
Expected Result: The system returns a match score that is not significantly affected by the keyword order.
TC_MA_005: Matching - Case Insensitivity:
Description: Verify that the matching algorithm is case-insensitive.
Steps: Send a resume text and a job description text that contain the same keywords but with different capitalization to the /match endpoint.
Expected Result: The system returns a match score as if the capitalization was the same.
TC_MA_006: Matching - Synonyms:
Description: Verify that the matching algorithm considers synonyms when comparing resume content and job requirements. (This requires synonym support in the algorithm).
Steps: Send a resume text that uses synonyms for keywords in the job description to the /match endpoint.
Expected Result: The system returns a higher match score than if synonyms were not considered.
Scoring System Test Cases

TC_SS_001: Scoring - Content Match Weighting:
Description: Verify that the content match score contributes to the overall ATS score according to its configured weight.
Steps: Configure the content match weight to a specific value. Send a resume and job description to the /score endpoint. Verify that the content match score contributes to the overall score as expected.
Expected Result: The overall score reflects the configured content match weight.
TC_SS_002: Scoring - Format Compatibility Weighting:
Description: Verify that the format compatibility score contributes to the overall ATS score according to its configured weight.
Steps: Configure the format compatibility weight to a specific value. Send a resume and job description to the /score endpoint. Create a resume with poor formatting. Verify that the format compatibility score contributes to the overall score as expected.
Expected Result: The overall score reflects the configured format compatibility weight.
TC_SS_003: Scoring - Section-Specific Scores Weighting:
Description: Verify that the section-specific scores contribute to the overall ATS score according to their configured weights.
Steps: Configure the weights for the Skills, Experience, and Education sections. Send a resume and job description to the /score endpoint. Verify that the section-specific scores contribute to the overall score as expected.
Expected Result: The overall score reflects the configured section-specific score weights.
TC_SS_004: Scoring - Perfect Score:
Description: Verify that the system generates a perfect score (100) when the resume perfectly matches the job requirements and has excellent formatting.
Steps: Send a resume and job description that are identical and have perfect formatting to the /score endpoint.
Expected Result: The system returns a total score of 100.
TC_SS_005: Scoring - Zero Score:
Description: Verify that the system generates a zero score when the resume does not match the job requirements and has poor formatting.
Steps: Send a resume and job description that have no overlap and have poor formatting to the /score endpoint.
Expected Result: The system returns a total score of 0.
TC_SS_006: Scoring - Invalid Weight Configuration:
Description: Verify that the system handles invalid weight configurations gracefully (e.g., weights that do not sum to 100).
Steps: Configure the weights for the scoring dimensions such that they do not sum to 100. Send a resume and job description to the /score endpoint.
Expected Result: The system returns an error message indicating that the weight configuration is invalid.
TC_SS_007: Scoring - Section Specific Scores Calculation:
Description: Verify that the section specific scores are calculated correctly.
Steps: Create a resume and job description. Analyze the expected scores for Skills, Experience, and Education based on the content. Send the resume and job description to the /score endpoint.
Expected Result: The section specific scores in the response match the expected values.
Recommendation Engine Test Cases

TC_RE_001: Recommendation - Keyword Optimization:
Description: Verify that the system suggests adding missing keywords to the resume.
Steps: Send a resume and job description to the /score endpoint where the resume is missing some keywords from the job description.
Expected Result: The system provides a recommendation to add the missing keywords to the resume.
TC_RE_002: Recommendation - Formatting Improvements:
Description: Verify that the system suggests formatting improvements to the resume.
Steps: Send a resume with poor formatting (e.g., using tables, images, non-standard headings) and a job description to the /score endpoint.
Expected Result: The system provides recommendations to improve the resume's formatting.
TC_RE_003: Recommendation - Content Enhancement:
Description: Verify that the system suggests adding more details to specific sections of the resume.
Steps: Send a resume and job description to the /score endpoint where the resume is lacking details in certain sections (e.g., Skills, Experience).
Expected Result: The system provides recommendations to add more details to the relevant sections of the resume.
TC_RE_004: Recommendation - Prioritization:
Description: Verify that the system prioritizes recommendations based on their potential impact on the ATS score.
Steps: Send a resume and job description to the /score endpoint. Analyze the recommendations provided by the system and verify that the recommendations with the greatest potential impact on the ATS score are listed first.
Expected Result: The recommendations are prioritized based on their potential impact on the ATS score.
TC_RE_005: Recommendation - Explanation:
Description: Verify that the system provides explanations for why each recommendation is being made.
Steps: Send a resume and job description to the /score endpoint. Verify that each recommendation is accompanied by an explanation of why it is being made.
Expected Result: Each recommendation includes an explanation.
Infrastructure and Development Test Cases

TC_ID_001: Python Version:
Description: Verify that the project is running with Python 3.12.
Steps: Check the Python version used by the application.
Expected Result: The application is running with Python 3.12.
TC_ID_002: Dependency Installation:
Description: Verify that all project dependencies are installed correctly using requirements.txt.
Steps: Install the dependencies using pip install -r requirements.txt and verify that all dependencies are installed without errors.
Expected Result: All dependencies are installed successfully.
TC_ID_003: PEP8 Compliance:
Description: Verify that the codebase adheres to PEP8 coding standards.
Steps: Run a PEP8 compliance checker (e.g., flake8) on the codebase.
Expected Result: The codebase passes the PEP8 compliance check without any errors or warnings.
TC_ID_004: Modular Coding:
Description: Verify that the codebase is divided into modular components with clear responsibilities.
Steps: Review the project structure and code to ensure that it is well-organized and that modules have clear responsibilities.
Expected Result: The codebase is modular and well-organized.
TC_ID_005: FastAPI API Functionality:
Description: Verify that all FastAPI API endpoints are functioning correctly.
Steps: Send requests to all API endpoints and verify that they return the expected results.
Expected Result: All API endpoints are functioning correctly.
TC_ID_006: CrewAI Integration:
Description: Verify that the CrewAI framework is properly integrated and functioning as expected.
Steps: Run the application and verify that the agents are communicating and collaborating to achieve the project goals.
Expected Result: The CrewAI framework is properly integrated and functioning as expected.
TC_ID_007: Dockerfile Build:
Description: Verify that the Dockerfile builds a Docker image that can run the application.
Steps: Build the Docker image using the Dockerfile and verify that the image is built successfully.
Expected Result: The Docker image is built successfully.
TC_ID_008: Docker Image Run:
Description: Verify that the Docker image can be run and that the application functions correctly within the container.
Steps: Run the Docker image and verify that the application is running and accessible.
Expected Result: The application is running and accessible within the Docker container.
TC_ID_009: DockerHub Push:
Description: Verify that the Docker image can be pushed to a public DockerHub repository.
Steps: Push the Docker image to a public DockerHub repository and verify that the image is successfully pushed.
Expected Result: The Docker image is successfully pushed to DockerHub.
Security Test Cases

TC_SEC_001: Input Sanitization - Malicious Input:
Description: Verify that the system sanitizes malicious input to prevent code injection attacks.
Steps: Send malicious input (e.g., SQL injection, XSS) to the API endpoints and agent functions.
Expected Result: The system sanitizes the input and prevents the malicious code from being executed.
TC_SEC_002: File Upload - Path Traversal:
Description: Verify that the system prevents path traversal vulnerabilities during file uploads.
Steps: Attempt to upload a file with a path that traverses outside of the allowed directory (e.g., ../../../../etc/passwd).
Expected Result: The system rejects the file upload and returns an error message.
TC_SEC_003: Web Scraping - Rate Limiting:
Description: Verify that the web scraping logic implements rate limiting to avoid overloading the target website.
Steps: Monitor the number of requests sent to the target website during web scraping and verify that the rate is within acceptable limits.
Expected Result: The web scraping logic implements rate limiting.
TC_SEC_004: robots.txt - Full Compliance:
Description: Verify that the web scraping logic fully complies with the robots.txt file of the target website.
Steps: Create a web server with a complex robots.txt file that disallows scraping of certain pages based on different user agents. Configure the web scraper to use different user agents and verify that it respects the robots.txt directives for each user agent.
Expected Result: The web scraping logic fully complies with the robots.txt file.
TC_SEC_005: Logging - No Sensitive Information:
Description: Verify that sensitive information (e.g., passwords, API keys) is not logged.
Steps: Review the log files to ensure that no sensitive information is being logged.
Expected Result: No sensitive information is logged.
TC_SEC_006: API Key Security - Brute Force:
Description: Verify that the API is protected against brute-force attacks on the API key.
Steps: Attempt to make a large number of requests to the API with different API keys in a short period of time.
Expected Result: The API implements rate limiting or other security measures to prevent brute-force attacks.
These test cases cover the user stories, functional and technical design, and security review comments. They should provide a good starting point for testing the Resume ATS Score Checker project. Remember to adapt and expand these test cases as needed during the development process.
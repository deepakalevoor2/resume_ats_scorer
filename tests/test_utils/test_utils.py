import unittest
import tempfile
import os
from unittest.mock import patch, MagicMock
import re

from utils.text_processors import (
    TextExtractor,
    KeywordExtractor,
    SectionExtractor,
    JobDescriptionParser,
    MatchingAlgorithm,
    ATSFormatChecker
)


class TestTextExtractor(unittest.TestCase):
    """Test the TextExtractor functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary files for testing
        self.pdf_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        self.docx_file = tempfile.NamedTemporaryFile(suffix='.docx', delete=False)
        self.html_file = tempfile.NamedTemporaryFile(suffix='.html', delete=False)
        
        # Write sample content to HTML file
        with open(self.html_file.name, 'w', encoding='utf-8') as f:
            f.write("<html><body><h1>Sample Resume</h1><p>Skills: Python, Java</p></body></html>")
        
        self.pdf_file.close()
        self.docx_file.close()
        self.html_file.close()
    
    def tearDown(self):
        """Clean up test environment."""
        os.unlink(self.pdf_file.name)
        os.unlink(self.docx_file.name)
        os.unlink(self.html_file.name)
    
    @patch('utils.text_processors.pdf_extract_text')
    def test_extract_from_pdf(self, mock_extract):
        """Test extracting text from PDF."""
        # Mock the PDF extraction
        mock_extract.return_value = "Sample PDF text"
        
        # Test extraction
        result = TextExtractor.extract_from_pdf(self.pdf_file.name)
        
        # Check the result
        self.assertEqual(result, "Sample PDF text")
        mock_extract.assert_called_once_with(self.pdf_file.name)
    
    @patch('utils.text_processors.docx2txt.process')
    def test_extract_from_docx(self, mock_process):
        """Test extracting text from DOCX."""
        # Mock the DOCX extraction
        mock_process.return_value = "Sample DOCX text"
        
        # Test extraction
        result = TextExtractor.extract_from_docx(self.docx_file.name)
        
        # Check the result
        self.assertEqual(result, "Sample DOCX text")
        mock_process.assert_called_once_with(self.docx_file.name)
    
    def test_extract_from_html(self):
        """Test extracting text from HTML."""
        # Test extraction
        result = TextExtractor.extract_from_html(self.html_file.name)
        
        # Check the result
        self.assertIn("Sample Resume", result)
        self.assertIn("Skills: Python, Java", result)
    
    def test_extract_from_file(self):
        """Test extracting text based on file extension."""
        # Patch the specific extraction methods
        with patch.object(TextExtractor, 'extract_from_pdf', return_value="PDF content"), \
             patch.object(TextExtractor, 'extract_from_docx', return_value="DOCX content"), \
             patch.object(TextExtractor, 'extract_from_html', return_value="HTML content"):
            
            # Test PDF extraction
            result = TextExtractor.extract_from_file(self.pdf_file.name)
            self.assertEqual(result, "PDF content")
            
            # Test DOCX extraction
            result = TextExtractor.extract_from_file(self.docx_file.name)
            self.assertEqual(result, "DOCX content")
            
            # Test HTML extraction
            result = TextExtractor.extract_from_file(self.html_file.name)
            self.assertEqual(result, "HTML content")
            
            # Test unsupported file type
            result = TextExtractor.extract_from_file("unsupported.xyz")
            self.assertEqual(result, "")


class TestKeywordExtractor(unittest.TestCase):
    """Test the KeywordExtractor functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.extractor = KeywordExtractor()
    
    def test_preprocess_text(self):
        """Test text preprocessing."""
        # Test preprocessing
        text = "This is a Sample Resume. It has Skills: Python, Java, and SQL!"
        result = self.extractor.preprocess_text(text)
        
        # Check the result
        self.assertEqual(result, "this is a sample resume it has skills python java and sql")
    
    def test_extract_keywords(self):
        """Test keyword extraction."""
        # Sample text
        text = """
        Experienced software developer with 5 years of experience in Python and Java.
        Proficient in web frameworks like Django and Flask.
        Familiar with AWS, Docker, and Kubernetes.
        """
        
        # Test extraction
        result = self.extractor.extract_keywords(text)
        
        # Check the result
        self.assertIsInstance(result, list)
        
        # Check that some expected keywords are included
        expected_keywords = ['python', 'java', 'django', 'flask', 'aws', 'docker', 'kubernetes']
        for keyword in expected_keywords:
            self.assertTrue(
                any(keyword in kw.lower() for kw in result),
                f"Expected '{keyword}' not found in extracted keywords: {result}"
            )
    
    def test_extract_technical_skills(self):
        """Test technical skills extraction."""
        # Sample text
        text = """
        Technical Skills: Python, Java, JavaScript, React, Node.js, MongoDB
        Familiar with AWS, Docker, and Git.
        """
        
        # Test extraction
        result = self.extractor.extract_technical_skills(text)
        
        # Check the result
        self.assertIsInstance(result, list)
        
        # Check that expected skills are included
        expected_skills = ['python', 'java', 'javascript', 'react', 'node.js', 'mongodb', 'aws', 'docker', 'git']
        for skill in expected_skills:
            self.assertTrue(
                skill in result,
                f"Expected skill '{skill}' not found in extracted skills: {result}"
            )


class TestSectionExtractor(unittest.TestCase):
    """Test the SectionExtractor functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.extractor = SectionExtractor()
    
    def test_extract_sections(self):
        """Test section extraction from resume text."""
        # Sample resume
        resume = """
        SUMMARY
        Experienced software developer with 5 years in Python and Java.
        
        EXPERIENCE
        Software Engineer, ABC Inc., 2018-Present
        - Developed web applications using Flask and Django
        
        EDUCATION
        B.S. Computer Science, XYZ University, 2018
        
        SKILLS
        Programming: Python, Java, JavaScript
        Frameworks: Django, Flask, React
        """
        
        # Test extraction
        result = self.extractor.extract_sections(resume)
        
        # Check the result
        self.assertIsInstance(result, dict)
        
        # Check that expected sections are extracted
        self.assertIn('summary', result)
        self.assertIn('experience', result)
        self.assertIn('education', result)
        self.assertIn('skills', result)
        
        # Check section content
        self.assertIn("Experienced software developer", result['summary'])
        self.assertIn("Software Engineer", result['experience'])
        self.assertIn("B.S. Computer Science", result['education'])
        self.assertIn("Programming: Python", result['skills'])


class TestJobDescriptionParser(unittest.TestCase):
    """Test the JobDescriptionParser functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.parser = JobDescriptionParser()
    
    def test_extract_requirements(self):
        """Test extracting requirements from job description."""
        # Sample job description
        job_desc = """
        We are looking for a Software Engineer with at least 3 years of experience in Python.
        Bachelor's degree in Computer Science or related field required.
        Skills required: Python, Django, RESTful API, AWS, Docker
        """
        
        # Test extraction
        result = self.parser.extract_requirements(job_desc)
        
        # Check the result
        self.assertIsInstance(result, dict)
        self.assertIn('skills', result)
        self.assertIn('education', result)
        self.assertIn('experience', result)
        
        # Check that expected requirements are extracted
        skills = result['skills']
        education = result['education']
        experience = result['experience']
        
        # Check skills
        expected_skills = ['python', 'django', 'aws', 'docker']
        for skill in expected_skills:
            self.assertTrue(
                skill in skills,
                f"Expected skill '{skill}' not found in extracted skills: {skills}"
            )
        
        # Check education
        self.assertTrue(any("bachelor" in edu.lower() for edu in education))
        
        # Check experience
        self.assertTrue(any("3 years" in exp.lower() for exp in experience))
    
    def test_parse_linkedin_job(self):
        """Test parsing LinkedIn job description."""
        # Sample LinkedIn job
        job_desc = """
        LinkedIn Job Posting
        
        Software Engineer
        
        Requirements:
        - 3+ years of Python experience
        - Bachelor's degree in Computer Science
        - Experience with Django and RESTful APIs
        """
        
        # Test parsing
        result = self.parser.parse_linkedin_job(job_desc)
        
        # Check the result
        self.assertIsInstance(result, dict)
        self.assertIn('skills', result)
        self.assertIn('education', result)
        self.assertIn('experience', result)
        
        # Should extract Python and Django
        skills = result['skills']
        self.assertTrue(any("python" in skill.lower() for skill in skills))
        self.assertTrue(any("django" in skill.lower() for skill in skills))
    
    def test_parse_naukri_job(self):
        """Test parsing Naukri job description."""
        # Sample Naukri job
        job_desc = """
        Naukri Job Posting
        
        Frontend Developer
        
        Job Description:
        We are looking for a Frontend Developer with:
        - 2+ years of experience
        - Bachelor's degree
        - Skills: JavaScript, React, HTML, CSS
        """
        
        # Test parsing
        result = self.parser.parse_naukri_job(job_desc)
        
        # Check the result
        self.assertIsInstance(result, dict)
        self.assertIn('skills', result)
        self.assertIn('education', result)
        self.assertIn('experience', result)
        
        # Should extract JavaScript and React
        skills = result['skills']
        self.assertTrue(any("javascript" in skill.lower() for skill in skills))
        self.assertTrue(any("react" in skill.lower() for skill in skills))


class TestMatchingAlgorithm(unittest.TestCase):
    """Test the MatchingAlgorithm functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.algorithm = MatchingAlgorithm()
    
    def test_calculate_similarity(self):
        """Test calculating similarity between resume and job description."""
        # Sample texts
        resume_text = "Experienced Python developer with Django and Flask experience"
        job_text = "Looking for Python developer with Django framework knowledge"
        
        # Test similarity calculation
        result = self.algorithm.calculate_similarity(resume_text, job_text)
        
        # Check the result
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)
        
        # The texts are similar, so the score should be reasonably high
        self.assertGreaterEqual(result, 0.5)
    
    def test_keyword_match_score(self):
        """Test calculating keyword match score."""
        # Sample keywords
        resume_keywords = ['python', 'django', 'flask', 'aws', 'docker']
        job_keywords = ['python', 'django', 'aws', 'kubernetes']
        
        # Test score calculation
        result = self.algorithm.keyword_match_score(resume_keywords, job_keywords)
        
        # Check the result
        self.assertIsInstance(result, float)
        
        # 3 out of 4 keywords match
        self.assertAlmostEqual(result, 0.75)
    
    def test_section_match_score(self):
        """Test calculating section match scores."""
        # Sample sections and requirements
        resume_sections = {
            'skills': 'Python, Django, Flask, AWS, Docker',
            'education': 'Bachelor of Science in Computer Science',
            'experience': '5 years of Python development experience'
        }
        
        job_requirements = {
            'skills': ['python', 'django', 'kubernetes'],
            'education': ['Bachelor\'s degree in Computer Science'],
            'experience': ['3+ years of experience']
        }
        
        # Test score calculation
        result = self.algorithm.section_match_score(resume_sections, job_requirements)
        
        # Check the result
        self.assertIsInstance(result, dict)
        self.assertIn('skills', result)
        self.assertIn('education', result)
        self.assertIn('experience', result)
        
        # Scores should be between 0 and 1
        self.assertGreaterEqual(result['skills'], 0.0)
        self.assertLessEqual(result['skills'], 1.0)
        self.assertGreaterEqual(result['education'], 0.0)
        self.assertLessEqual(result['education'], 1.0)
        self.assertGreaterEqual(result['experience'], 0.0)
        self.assertLessEqual(result['experience'], 1.0)


class TestATSFormatChecker(unittest.TestCase):
    """Test the ATSFormatChecker functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.checker = ATSFormatChecker()
    
    def test_check_format(self):
        """Test checking resume format for ATS compatibility."""
        # Sample well-formatted resume
        good_resume = """
        SUMMARY
        Experienced software developer with 5 years in Python and Java.
        
        EXPERIENCE
        Software Engineer, ABC Inc., Jan 2018 - Present
        • Developed web applications using Flask and Django
        • Implemented RESTful APIs for mobile applications
        
        EDUCATION
        B.S. Computer Science, XYZ University, May 2018
        
        SKILLS
        Programming: Python, Java, JavaScript
        Frameworks: Django, Flask, React
        """
        
        # Sample poorly formatted resume
        bad_resume = """
        John Doe | Software Developer
        -----------------------------
        
        Experience:
        ABC Inc. | 2018-2020
        XYZ Corp. | 2020-Present
        
        Skills
        ------
        * Python
        * Java
        
        Education
        ---------
        Computer Science Degree
        """
        
        # Test format checking for good resume
        good_result = self.checker.check_format(good_resume)
        
        # Check the result
        self.assertIsInstance(good_result, dict)
        self.assertIn('bullet_points', good_result)
        self.assertIn('date_consistency', good_result)
        self.assertIn('section_headers', good_result)
        self.assertIn('line_spacing', good_result)
        self.assertIn('no_common_issues', good_result)
        
        # Good resume should have high scores
        self.assertEqual(good_result['bullet_points'], 1.0)
        self.assertGreaterEqual(good_result['section_headers'], 0.75)
        
        # Test format checking for bad resume
        bad_result = self.checker.check_format(bad_resume)
        
        # Check the result
        self.assertIsInstance(bad_result, dict)
        
        # Bad resume should have lower scores in some areas
        self.assertEqual(bad_result['bullet_points'], 1.0)  # Still has bullets
        # But likely has issues with headers and formatting
        self.assertLessEqual(bad_result['section_headers'], good_result['section_headers'])
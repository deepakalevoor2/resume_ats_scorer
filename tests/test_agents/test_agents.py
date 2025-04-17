import os
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import json
from pathlib import Path

from agents.resume_parser_agent import ResumeParserAgent
from agents.keyword_analyst_agent import KeywordAnalystAgent
from agents.job_description_agent import JobDescriptionAgent
from agents.matching_agent import MatchingAgent
from agents.scoring_agent import ScoringAgent
from agents.recommendation_agent import RecommendationAgent
from crew.crew_manager import CrewManager


class TestResumeParserAgent(unittest.TestCase):
    """Test the ResumeParserAgent functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.agent = ResumeParserAgent()
        # Create a temporary PDF file for testing
        self.test_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        self.test_file.close()
    
    def tearDown(self):
        """Clean up test environment."""
        os.unlink(self.test_file.name)
    
    @patch('agents.resume_parser_agent.TextExtractor.extract_from_pdf')
    def test_parse_resume(self, mock_extract):
        """Test parsing a resume file."""
        # Mock the extraction function
        mock_extract.return_value = "Sample resume text with skills in Python and Java"
        
        # Test parsing
        result = self.agent.parse_resume(self.test_file.name)
        
        # Check that the extraction function was called
        mock_extract.assert_called_once_with(self.test_file.name)
        
        # Check the result
        self.assertIsInstance(result, dict)
        self.assertIn('content', result)
        self.assertEqual(result['content'], "Sample resume text with skills in Python and Java")
    
    def test_extract_sections(self):
        """Test extracting sections from a resume."""
        # Sample resume text
        resume_text = """
        SUMMARY
        Experienced software developer with 5 years in Python and Java.
        
        EXPERIENCE
        Software Engineer, ABC Inc., 2018-Present
        - Developed web applications using Flask and Django
        
        EDUCATION
        B.S. Computer Science, XYZ University, 2018
        """
        
        # Mock the parse_resume method
        self.agent.parse_resume = MagicMock(return_value={'content': resume_text})
        
        # Test section extraction
        result = self.agent.extract_sections(self.test_file.name)
        
        # Check the result
        self.assertIsInstance(result, dict)
        self.assertIn('sections', result)
        sections = result['sections']
        self.assertIn('summary', sections)
        self.assertIn('experience', sections)
        self.assertIn('education', sections)


class TestKeywordAnalystAgent(unittest.TestCase):
    """Test the KeywordAnalystAgent functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.agent = KeywordAnalystAgent()
    
    def test_extract_keywords(self):
        """Test extracting keywords from resume text."""
        # Sample resume text
        resume_text = """
        Experienced software developer with expertise in Python, Java, and SQL.
        Proficient in web development frameworks like Django and Flask.
        Familiar with cloud platforms including AWS and Azure.
        """
        
        # Test keyword extraction
        result = self.agent.extract_keywords(resume_text)
        
        # Check the result
        self.assertIsInstance(result, dict)
        self.assertIn('keywords', result)
        self.assertIsInstance(result['keywords'], list)
        
        # Check that some expected keywords are found
        keywords = result['keywords']
        for expected in ['python', 'java', 'sql', 'django', 'flask', 'aws', 'azure']:
            self.assertTrue(
                any(expected in keyword.lower() for keyword in keywords),
                f"Expected keyword '{expected}' not found in {keywords}"
            )


class TestJobDescriptionAgent(unittest.TestCase):
    """Test the JobDescriptionAgent functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.agent = JobDescriptionAgent()
    
    def test_parse_job_description(self):
        """Test parsing a job description."""
        # Sample job description
        job_desc = """
        We are looking for a Software Engineer with at least 3 years of experience in Python and Django.
        Bachelor's degree in Computer Science or related field required.
        Experience with AWS and Docker is a plus.
        """
        
        # Test job description parsing
        result = self.agent.parse_job_description(job_desc)
        
        # Check the result
        self.assertIsInstance(result, dict)
        self.assertIn('requirements', result)
        
        # Check that requirements are extracted
        requirements = result['requirements']
        self.assertIn('skills', requirements)
        self.assertIn('education', requirements)
        self.assertIn('experience', requirements)
        
        # Check that expected requirements are found
        skills = requirements['skills']
        education = requirements['education']
        experience = requirements['experience']
        
        self.assertTrue(any('python' in skill.lower() for skill in skills))
        self.assertTrue(any('django' in skill.lower() for skill in skills))
        self.assertTrue(any('bachelor' in edu.lower() for edu in education))
        self.assertTrue(any('3 years' in exp.lower() for exp in experience))


class TestMatchingAgent(unittest.TestCase):
    """Test the MatchingAgent functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.agent = MatchingAgent()
    
    def test_match_resume_to_job(self):
        """Test matching a resume to a job description."""
        # Sample resume and job data
        resume_data = {
            'content': "Experienced Python developer with 5 years of experience",
            'sections': {
                'experience': "5 years of Python development",
                'education': "B.S. Computer Science",
                'skills': "Python, Django, Flask, AWS"
            },
            'keywords': ['python', 'django', 'flask', 'aws']
        }
        
        job_data = {
            'content': "Looking for Python developer with Django experience",
            'requirements': {
                'skills': ['python', 'django'],
                'education': ['Bachelor\'s degree'],
                'experience': ['3 years']
            }
        }
        
        # Test matching
        result = self.agent.match_resume_to_job(resume_data, job_data)
        
        # Check the result
        self.assertIsInstance(result, dict)
        self.assertIn('match_score', result)
        self.assertIn('section_scores', result)
        
        # Match score should be between 0 and 1
        self.assertGreaterEqual(result['match_score'], 0.0)
        self.assertLessEqual(result['match_score'], 1.0)
        
        # Check section scores
        section_scores = result['section_scores']
        self.assertIn('skills', section_scores)
        self.assertIn('education', section_scores)
        self.assertIn('experience', section_scores)


class TestScoringAgent(unittest.TestCase):
    """Test the ScoringAgent functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.agent = ScoringAgent()
    
    def test_calculate_score(self):
        """Test calculating a score based on match results."""
        # Sample match results
        match_results = {
            'match_score': 0.8,
            'section_scores': {
                'skills': 0.9,
                'education': 0.7,
                'experience': 0.6
            }
        }
        
        # Sample format scores
        format_scores = {
            'bullet_points': 1.0,
            'date_consistency': 0.5,
            'section_headers': 0.8,
            'line_spacing': 1.0,
            'no_common_issues': 1.0
        }
        
        # Test score calculation
        result = self.agent.calculate_score(match_results, format_scores)
        
        # Check the result
        self.assertIsInstance(result, dict)
        self.assertIn('overall_score', result)
        self.assertIn('content_score', result)
        self.assertIn('format_score', result)
        self.assertIn('section_scores', result)
        
        # Scores should be between 0 and 100
        self.assertGreaterEqual(result['overall_score'], 0)
        self.assertLessEqual(result['overall_score'], 100)
        self.assertGreaterEqual(result['content_score'], 0)
        self.assertLessEqual(result['content_score'], 100)
        self.assertGreaterEqual(result['format_score'], 0)
        self.assertLessEqual(result['format_score'], 100)


class TestRecommendationAgent(unittest.TestCase):
    """Test the RecommendationAgent functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.agent = RecommendationAgent()
    
    def test_generate_recommendations(self):
        """Test generating recommendations based on scores."""
        # Sample scoring results
        scoring_results = {
            'overall_score': 65,
            'content_score': 70,
            'format_score': 60,
            'section_scores': {
                'skills': 0.6,
                'education': 0.8,
                'experience': 0.5
            }
        }
        
        # Sample job requirements
        job_requirements = {
            'skills': ['python', 'django', 'aws'],
            'education': ['Bachelor\'s degree'],
            'experience': ['3 years']
        }
        
        # Test recommendation generation
        result = self.agent.generate_recommendations(scoring_results, job_requirements)
        
        # Check the result
        self.assertIsInstance(result, dict)
        self.assertIn('recommendations', result)
        self.assertIsInstance(result['recommendations'], list)
        self.assertGreater(len(result['recommendations']), 0)


class TestCrewManager(unittest.TestCase):
    """Test the CrewManager functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.crew_manager = CrewManager()
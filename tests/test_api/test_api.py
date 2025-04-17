import os
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import json
from fastapi.testclient import TestClient
from pathlib import Path

from api.app import app
from api.routes import router


class TestAPIEndpoints(unittest.TestCase):
    """Test the API endpoints."""
    
    def setUp(self):
        """Set up test environment."""
        self.client = TestClient(app)
        
        # Create a temporary PDF file for testing
        content = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n" # Minimal valid PDF header
        self.test_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        self.test_file.write(content)
        self.test_file.close()
    
    def tearDown(self):
        """Clean up test environment."""
        os.unlink(self.test_file.name)
    
    def test_health_check(self):
        """Test the health check endpoint."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
    
    @patch('api.routes.CrewManager.process_resume')
    def test_upload_resume(self, mock_process_resume):
        """Test the resume upload endpoint."""
        # Mock the process_resume method
        mock_process_resume.return_value = {
            "success": True,
            "resume_id": "test-id",
            "parsed_content": "Sample resume content"
        }
        
        # Test file upload
        with open(self.test_file.name, "rb") as file:
            response = self.client.post(
                "/resume/upload",
                files={"file": ("test_resume.pdf", file, "application/pdf")}
            )
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["resume_id"], "test-id")
    
    @patch('api.routes.CrewManager.submit_job_description')
    def test_submit_job_description(self, mock_submit_job):
        """Test the job description submission endpoint."""
        # Mock the submit_job_description method
        mock_submit_job.return_value = {
            "success": True,
            "job_id": "test-job-id",
            "parsed_requirements": {
                "skills": ["python", "django"],
                "education": ["Bachelor's degree"],
                "experience": ["3 years"]
            }
        }
        
        # Test job description submission
        job_data = {
            "description": "Looking for a Python developer with 3 years of experience",
            "source": "LinkedIn"
        }
        response = self.client.post("/job/submit", json=job_data)
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["job_id"], "test-job-id")
        self.assertIn("parsed_requirements", data)
    
    @patch('api.routes.CrewManager.match_resume_to_job')
    def test_match_resume_to_job(self, mock_match):
        """Test the resume-job matching endpoint."""
        # Mock the match_resume_to_job method
        mock_match.return_value = {
            "success": True,
            "overall_score": 78,
            "content_score": 80,
            "format_score": 75,
            "section_scores": {
                "skills": 85,
                "education": 90,
                "experience": 70
            },
            "recommendations": [
                "Add more Django-specific experience details",
                "Format dates consistently"
            ]
        }
        
        # Test matching
        match_data = {
            "resume_id": "test-resume-id",
            "job_id": "test-job-id"
        }
        response = self.client.post("/match", json=match_data)
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("overall_score", data)
        self.assertIn("content_score", data)
        self.assertIn("format_score", data)
        self.assertIn("section_scores", data)
        self.assertIn("recommendations", data)
    
    @patch('api.routes.CrewManager.get_resume_details')
    def test_get_resume(self, mock_get_resume):
        """Test the get resume details endpoint."""
        # Mock the get_resume_details method
        mock_get_resume.return_value = {
            "success": True,
            "resume_id": "test-resume-id",
            "parsed_content": "Sample resume content",
            "sections": {
                "summary": "Experienced developer",
                "experience": "5 years of Python development",
                "education": "B.S. Computer Science"
            },
            "keywords": ["python", "django", "flask"]
        }
        
        # Test getting resume details
        response = self.client.get("/resume/test-resume-id")
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["resume_id"], "test-resume-id")
        self.assertIn("parsed_content", data)
        self.assertIn("sections", data)
        self.assertIn("keywords", data)
    
    @patch('api.routes.CrewManager.get_job_details')
    def test_get_job(self, mock_get_job):
        """Test the get job details endpoint."""
        # Mock the get_job_details method
        mock_get_job.return_value = {
            "success": True,
            "job_id": "test-job-id",
            "description": "Looking for a Python developer",
            "parsed_requirements": {
                "skills": ["python", "django"],
                "education": ["Bachelor's degree"],
                "experience": ["3 years"]
            }
        }
        
        # Test getting job details
        response = self.client.get("/job/test-job-id")
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["job_id"], "test-job-id")
        self.assertIn("description", data)
        self.assertIn("parsed_requirements", data)
    
    def test_error_handling(self):
        """Test error handling in the API."""
        # Test invalid endpoint
        response = self.client.get("/invalid_endpoint")
        self.assertEqual(response.status_code, 404)
        
        # Test invalid resume ID
        response = self.client.get("/resume/invalid_id")
        self.assertEqual(response.status_code, 404)
        
        # Test invalid job ID
        response = self.client.get("/job/invalid_id")
        self.assertEqual(response.status_code, 404)
        
        # Test invalid file upload
        response = self.client.post(
            "/resume/upload",
            files={"file": ("test.txt", b"Invalid content", "text/plain")}
        )
        self.assertEqual(response.status_code, 400)
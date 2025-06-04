import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import tempfile
import json
from resume_ats_scorer.api.main import app

client = TestClient(app)

@pytest.fixture
def sample_resume():
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        f.write(b'%PDF-1.4\n1 0 obj\n<</Type /Catalog /Pages 2 0 R>>\nendobj\n2 0 obj\n<</Type /Pages /Kids [3 0 R] /Count 1>>\nendobj\n3 0 obj\n<</Type /Page /Parent 2 0 R /Resources <<>> /Contents 4 0 R>>\nendobj\n4 0 obj\n<</Length 44>>\nstream\nBT\n/F1 12 Tf\n100 700 Td\n(Hello World) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000010 00000 n\n0000000053 00000 n\n0000000102 00000 n\n0000000172 00000 n\ntrailer\n<</Size 5 /Root 1 0 R>>\nstartxref\n242\n%%EOF')
        return f.name

@pytest.fixture
def sample_job_description():
    return {
        "title": "Senior Software Engineer",
        "description": "Looking for a Python developer with 5+ years of experience",
        "requirements": [
            "Python programming",
            "Django framework",
            "REST API development",
            "AWS experience"
        ]
    }

class TestAPI:
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "description" in data

    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_resume_upload(self, sample_resume):
        with open(sample_resume, "rb") as f:
            response = client.post(
                "/api/v1/resume/upload",
                files={"file": ("resume.pdf", f, "application/pdf")}
            )
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "status" in data
        assert data["status"] == "success"

    def test_resume_upload_invalid_file(self):
        response = client.post(
            "/api/v1/resume/upload",
            files={"file": ("test.txt", b"invalid content", "text/plain")}
        )
        assert response.status_code == 400

    def test_job_description_submit(self, sample_job_description):
        response = client.post(
            "/api/v1/job-description/submit",
            json=sample_job_description
        )
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "status" in data
        assert data["status"] == "success"

    def test_job_description_submit_invalid(self):
        response = client.post(
            "/api/v1/job-description/submit",
            json={"invalid": "data"}
        )
        assert response.status_code == 422

    def test_score_resume(self, sample_resume, sample_job_description):
        # First upload resume
        with open(sample_resume, "rb") as f:
            resume_response = client.post(
                "/api/v1/resume/upload",
                files={"file": ("resume.pdf", f, "application/pdf")}
            )
        resume_id = resume_response.json()["id"]

        # Submit job description
        job_response = client.post(
            "/api/v1/job-description/submit",
            json=sample_job_description
        )
        job_id = job_response.json()["id"]

        # Score resume
        response = client.post(
            "/api/v1/scoring/score",
            json={
                "resume_id": resume_id,
                "job_description_id": job_id
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "score" in data
        assert "sections" in data
        assert "recommendations" in data
        assert isinstance(data["score"], (int, float))
        assert isinstance(data["sections"], dict)
        assert isinstance(data["recommendations"], list)

    def test_score_resume_invalid_ids(self):
        response = client.post(
            "/api/v1/scoring/score",
            json={
                "resume_id": "invalid",
                "job_description_id": "invalid"
            }
        )
        assert response.status_code == 404

    def test_get_recommendations(self, sample_resume, sample_job_description):
        # First upload resume and submit job description
        with open(sample_resume, "rb") as f:
            resume_response = client.post(
                "/api/v1/resume/upload",
                files={"file": ("resume.pdf", f, "application/pdf")}
            )
        resume_id = resume_response.json()["id"]

        job_response = client.post(
            "/api/v1/job-description/submit",
            json=sample_job_description
        )
        job_id = job_response.json()["id"]

        # Get recommendations
        response = client.get(
            f"/api/v1/scoring/recommendations/{resume_id}/{job_id}"
        )
        assert response.status_code == 200
        data = response.json()
        assert "recommendations" in data
        assert isinstance(data["recommendations"], list)
        assert len(data["recommendations"]) > 0

    def test_get_recommendations_invalid_ids(self):
        response = client.get(
            "/api/v1/scoring/recommendations/invalid/invalid"
        )
        assert response.status_code == 404

    def test_api_documentation(self):
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_api_schema(self):
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema
        assert "components" in schema 
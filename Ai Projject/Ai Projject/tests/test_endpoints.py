"""Test API endpoints."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

API_KEY = "T1-ai-secret-key-2025"
HEADERS = {"X-API-Key": API_KEY}

class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check_success(self):
        """Test health check returns 200."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "version" in data

class TestIngestEndpoint:
    """Test document ingestion."""
    
    def test_ingest_valid_document(self):
        """Test ingesting a valid document."""
        payload = {
            "filename": "test_diabetes.txt",
            "content": "Type 2 diabetes management guidelines. Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "language": "en"
        }
        response = client.post("/ingest", json=payload, headers=HEADERS)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "chunks_created" in data
    
    def test_ingest_missing_api_key(self):
        """Test ingest without API key fails."""
        payload = {
            "filename": "test.txt",
            "content": "Some medical content about healthcare and treatment options for patients.",
        }
        response = client.post("/ingest", json=payload)
        assert response.status_code == 401

class TestRetrieveEndpoint:
    """Test document retrieval."""
    
    def test_retrieve_with_query(self):
        """Test retrieving documents."""
        payload = {
            "query": "diabetes management",
            "language": "en"
        }
        response = client.post("/retrieve", json=payload, headers=HEADERS)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "results" in data

class TestGenerateEndpoint:
    """Test LLM response generation."""
    
    def test_generate_response(self):
        """Test generating a response."""
        payload = {
            "query": "What is diabetes?",
            "language": "en"
        }
        response = client.post("/generate", json=payload, headers=HEADERS)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "response" in data

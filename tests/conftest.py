import pytest
from fastapi.testclient import TestClient
import os

# Set test environment
os.environ['ENVIRONMENT'] = 'test'
os.environ['JWT_SECRET_KEY'] = 'test-secret-key'
os.environ['DYNAMODB_ENDPOINT'] = 'http://localhost:8000'

from app.main import app

@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)

@pytest.fixture
def test_user_data():
    """Test user data"""
    return {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "business_name": "Test Business"
    }

@pytest.fixture
def test_lead_data():
    """Test lead data"""
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "5555551234",
        "company": "Acme Corp",
        "message": "Interested in services",
        "source": "website"
    }

@pytest.fixture
def auth_token(client, test_user_data):
    """Get auth token for testing - NOT ASYNC"""
    # Register user
    client.post("/auth/register", json=test_user_data)
    
    # Login
    response = client.post(
        "/auth/login",
        data={
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )
    
    return response.json()["access_token"]
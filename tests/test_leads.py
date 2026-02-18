import pytest
from fastapi import status

def test_create_lead(client, auth_token, test_lead_data):
    """Test creating a lead"""
    response = client.post(
        "/leads/",
        json=test_lead_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["first_name"] == test_lead_data["first_name"]
    assert data["email"] == test_lead_data["email"]
    assert data["status"] == "new"
    assert "id" in data

def test_list_leads(client, auth_token, test_lead_data):
    """Test listing leads"""
    # Create a lead first
    client.post(
        "/leads/",
        json=test_lead_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    # List leads
    response = client.get(
        "/leads/",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_lead(client, auth_token, test_lead_data):
    """Test getting a specific lead"""
    # Create lead
    create_response = client.post(
        "/leads/",
        json=test_lead_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    lead_id = create_response.json()["id"]
    
    # Get lead
    response = client.get(
        f"/leads/{lead_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == lead_id

def test_update_lead(client, auth_token, test_lead_data):
    """Test updating a lead"""
    # Create lead
    create_response = client.post(
        "/leads/",
        json=test_lead_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    lead_id = create_response.json()["id"]
    
    # Update lead
    update_data = {"status": "qualified"}
    response = client.patch(
        f"/leads/{lead_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "qualified"

def test_delete_lead(client, auth_token, test_lead_data):
    """Test deleting a lead"""
    # Create lead
    create_response = client.post(
        "/leads/",
        json=test_lead_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    lead_id = create_response.json()["id"]
    
    # Delete lead
    response = client.delete(
        f"/leads/{lead_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_unauthorized_access(client, test_lead_data):
    """Test that endpoints require authentication"""
    response = client.post("/leads/", json=test_lead_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_invalid_lead_data(client, auth_token):
    """Test validation of lead data"""
    invalid_data = {
        "first_name": "",  # Empty name
        "email": "not-an-email",  # Invalid email
        "phone": "123"  # Invalid phone
    }
    
    response = client.post(
        "/leads/",
        json=invalid_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
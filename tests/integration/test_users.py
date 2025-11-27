import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_user(db_session):
    """Test user registration endpoint"""
    # Use unique username to avoid conflicts with other tests
    unique_id = str(uuid.uuid4())[:8]
    username = f"testuser_{unique_id}"
    email = f"test_{unique_id}@example.com"
    
    response = client.post(
        "/users/register",
        json={
            "username": username,
            "password": "SecurePass123!",  # 15 chars - well within 72 limit
            "email": email
        }
    )
    
    assert response.status_code == 200, f"Got {response.status_code}: {response.text}"
    data = response.json()
    assert data["username"] == username
    assert data["email"] == email
    assert "password" not in data
    assert "id" in data


def test_login_user_success(db_session):
    """Test successful user login"""
    # Use unique username
    unique_id = str(uuid.uuid4())[:8]
    username = f"logintest_{unique_id}"
    email = f"login_{unique_id}@example.com"
    password = "SecurePass123!"
    
    # First register a user
    reg_response = client.post(
        "/users/register",
        json={
            "username": username,
            "password": password,
            "email": email
        }
    )
    assert reg_response.status_code == 200, f"Registration failed: {reg_response.text}"
    
    # Now try to login
    response = client.post(
        "/users/login",
        json={
            "username": username,
            "password": password
        }
    )
    
    assert response.status_code == 200, f"Got {response.status_code}: {response.text}"
    data = response.json()
    assert data["message"] == "Login successful"
    assert data["username"] == username


def test_login_user_fail(db_session):
    """Test failed user login with wrong password"""
    # Use unique username
    unique_id = str(uuid.uuid4())[:8]
    username = f"failtest_{unique_id}"
    
    # First register a user
    client.post(
        "/users/register",
        json={
            "username": username,
            "password": "SecurePass123!",
            "email": f"fail_{unique_id}@example.com"
        }
    )
    
    # Try to login with wrong password
    response = client.post(
        "/users/login",
        json={
            "username": username,
            "password": "WrongPass!"
        }
    )
    
    assert response.status_code == 401
    data = response.json()
    assert "Invalid" in data["detail"]


def test_register_duplicate_username(db_session):
    """Test that duplicate usernames are rejected"""
    # Use unique username
    unique_id = str(uuid.uuid4())[:8]
    username = f"duplicate_{unique_id}"
    
    # Register first user
    client.post(
        "/users/register",
        json={
            "username": username,
            "password": "SecurePass123!",
            "email": f"dup1_{unique_id}@example.com"
        }
    )
    
    # Try to register same username again
    response = client.post(
        "/users/register",
        json={
            "username": username,
            "password": "SecurePass123!",
            "email": f"dup2_{unique_id}@example.com"
        }
    )
    
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()


def test_login_nonexistent_user(db_session):
    """Test login with non-existent username"""
    # Use unique username to ensure it doesn't exist
    unique_id = str(uuid.uuid4())[:8]
    response = client.post(
        "/users/login",
        json={
            "username": f"nonexistent_{unique_id}",
            "password": "SomePass123!"
        }
    )
    
    assert response.status_code == 401
    data = response.json()
    assert "Invalid" in data["detail"]


def test_register_duplicate_email(db_session):
    """Test that duplicate emails are rejected"""
    # Use unique email
    unique_id = str(uuid.uuid4())[:8]
    email = f"same_{unique_id}@example.com"
    
    # Register first user
    client.post(
        "/users/register",
        json={
            "username": f"user1_{unique_id}",
            "password": "SecurePass123!",
            "email": email
        }
    )
    
    # Try to register different username with same email
    response = client.post(
        "/users/register",
        json={
            "username": f"user2_{unique_id}",
            "password": "SecurePass123!",
            "email": email
        }
    )
    
    assert response.status_code == 400
    assert "already" in response.json()["detail"].lower()
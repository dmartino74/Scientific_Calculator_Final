"""
Integration tests for user profile management, advanced calculations, and statistics
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)client = TestClient(app)


@pytest.fixture
def auth_headers(db_session):
    """Register a user and return authentication headers"""
    # Register a test user
    response = client.post("/users/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestAdvancedCalculations:
    """Test advanced calculation operations via API"""
    
    def test_power_operation(self, db_session, auth_headers):
        """Test power/exponentiation calculation"""
        response = client.post("/calculations", json={
            "a": 2,
            "b": 3,
            "type": "power"
        }, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 8
        assert data["type"] == "power"
    
    def test_modulus_operation(self, db_session, auth_headers):
        """Test modulus calculation"""
        response = client.post("/calculations", json={
            "a": 10,
            "b": 3,
            "type": "modulus"
        }, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 1
        assert data["type"] == "modulus"
    
    def test_sqrt_operation(self, db_session, auth_headers):
        """Test square root calculation"""
        response = client.post("/calculations", json={
            "a": 16,
            "b": 0,
            "type": "sqrt"
        }, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 4
        assert data["type"] == "sqrt"
    
    def test_sqrt_negative_number(self, db_session, auth_headers):
        """Test square root of negative number fails"""
        response = client.post("/calculations", json={
            "a": -4,
            "b": 0,
            "type": "sqrt"
        }, headers=auth_headers)
        
        assert response.status_code == 400
        assert "negative" in response.json()["detail"].lower()
    
    def test_modulus_by_zero(self, db_session, auth_headers):
        """Test modulus by zero fails"""
        response = client.post("/calculations", json={
            "a": 10,
            "b": 0,
            "type": "modulus"
        }, headers=auth_headers)
        
        assert response.status_code == 400
        assert "zero" in response.json()["detail"].lower()
    
    def test_edit_calculation_with_power(self, db_session, auth_headers):
        """Test editing calculation to use power operation"""
        # Create initial calculation
        create_response = client.post("/calculations", json={
            "a": 5,
            "b": 2,
            "type": "add"
        }, headers=auth_headers)
        calc_id = create_response.json()["id"]
        
        # Edit to power operation
        edit_response = client.put(f"/calculations/{calc_id}", json={
            "a": 3,
            "b": 4,
            "type": "power"
        }, headers=auth_headers)
        
        assert edit_response.status_code == 200
        data = edit_response.json()
        assert data["result"] == 81
        assert data["type"] == "power"


class TestUserProfileManagement:
    """Test user profile viewing and updating"""
    
    def test_get_current_user_profile(self, db_session, auth_headers):
        """Test getting current user's profile"""
        response = client.get("/users/me", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert "id" in data
        assert "created_at" in data
    
    def test_update_username(self, db_session, auth_headers):
        """Test updating username"""
        response = client.put("/users/me", json={
            "username": "newusername"
        }, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newusername"
    
    def test_update_email(self, db_session, auth_headers):
        """Test updating email"""
        response = client.put("/users/me", json={
            "email": "newemail@example.com"
        }, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "newemail@example.com"
    
    def test_update_both_username_and_email(self, db_session, auth_headers):
        """Test updating both username and email"""
        response = client.put("/users/me", json={
            "username": "brandnew",
            "email": "brandnew@example.com"
        }, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "brandnew"
        assert data["email"] == "brandnew@example.com"
    
    def test_update_username_already_exists(self, db_session, auth_headers):
        """Test updating to existing username fails"""
        # Create another user
        client.post("/users/register", json={
            "username": "otheruser",
            "email": "other@example.com",
            "password": "password123"
        })
        
        # Try to update to existing username
        response = client.put("/users/me", json={
            "username": "otheruser"
        }, headers=auth_headers)
        
        assert response.status_code == 400
        assert "exists" in response.json()["detail"].lower()


class TestPasswordChange:
    """Test password change functionality"""
    
    def test_change_password_success(self, db_session, auth_headers):
        """Test successful password change"""
        response = client.post("/users/me/change-password", json={
            "old_password": "testpass123",
            "new_password": "newpass456"
        }, headers=auth_headers)
        
        assert response.status_code == 200
        assert "success" in response.json()["message"].lower()
    
    def test_change_password_wrong_old_password(self, db_session, auth_headers):
        """Test password change with wrong old password"""
        response = client.post("/users/me/change-password", json={
            "old_password": "wrongpassword",
            "new_password": "newpass456"
        }, headers=auth_headers)
        
        assert response.status_code == 400
        assert "incorrect" in response.json()["detail"].lower()
    
    def test_login_after_password_change(self, db_session):
        """Test logging in with new password after change"""
        # Register user
        register_response = client.post("/users/register", json={
            "username": "passtest",
            "email": "passtest@example.com",
            "password": "oldpass123"
        })
        token = register_response.json()["access_token"]
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Change password
        client.post("/users/me/change-password", json={
            "old_password": "oldpass123",
            "new_password": "newpass456"
        }, headers=auth_headers)
        
        # Try to login with new password
        login_response = client.post("/users/login", json={
            "username": "passtest",
            "password": "newpass456"
        })
        
        assert login_response.status_code == 200
        assert "access_token" in login_response.json()


class TestCalculationStatistics:
    """Test calculation statistics endpoint"""
    
    def test_get_statistics_no_calculations(self, db_session, auth_headers):
        """Test statistics with no calculations"""
        response = client.get("/calculations/stats/summary", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_calculations"] == 0
        assert data["operation_counts"] == {}
        assert data["average_a"] == 0.0
        assert data["average_b"] == 0.0
        assert data["most_used_operation"] is None
    
    def test_get_statistics_with_calculations(self, db_session, auth_headers):
        """Test statistics with multiple calculations"""
        # Create several calculations
        calculations = [
            {"a": 10, "b": 5, "type": "add"},
            {"a": 20, "b": 10, "type": "add"},
            {"a": 15, "b": 3, "type": "subtract"},
            {"a": 8, "b": 2, "type": "multiply"},
            {"a": 100, "b": 10, "type": "divide"},
        ]
        
        for calc in calculations:
            client.post("/calculations", json=calc, headers=auth_headers)
        
        # Get statistics
        response = client.get("/calculations/stats/summary", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_calculations"] == 5
        assert data["operation_counts"]["add"] == 2
        assert data["operation_counts"]["subtract"] == 1
        assert data["operation_counts"]["multiply"] == 1
        assert data["operation_counts"]["divide"] == 1
        assert data["most_used_operation"] == "add"
        assert data["average_a"] == (10 + 20 + 15 + 8 + 100) / 5
        assert data["average_b"] == (5 + 10 + 3 + 2 + 10) / 5
    
    def test_statistics_isolated_per_user(self, db_session, auth_headers):
        """Test that statistics are isolated per user"""
        # Create calculation for first user
        client.post("/calculations", json={
            "a": 10, "b": 5, "type": "add"
        }, headers=auth_headers)
        
        # Register and login as second user
        register_response = client.post("/users/register", json={
            "username": "user2",
            "email": "user2@example.com",
            "password": "password123"
        })
        token2 = register_response.json()["access_token"]
        auth_headers2 = {"Authorization": f"Bearer {token2}"}
        
        # Get statistics for second user (should be empty)
        response = client.get("/calculations/stats/summary", headers=auth_headers2)
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_calculations"] == 0
    
    def test_statistics_with_advanced_operations(self, db_session, auth_headers):
        """Test statistics include advanced operations"""
        # Create calculations with new operation types
        calculations = [
            {"a": 2, "b": 3, "type": "power"},
            {"a": 2, "b": 4, "type": "power"},
            {"a": 10, "b": 3, "type": "modulus"},
            {"a": 16, "b": 0, "type": "sqrt"},
        ]
        
        for calc in calculations:
            client.post("/calculations", json=calc, headers=auth_headers)
        
        # Get statistics
        response = client.get("/calculations/stats/summary", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_calculations"] == 4
        assert data["operation_counts"]["power"] == 2
        assert data["operation_counts"]["modulus"] == 1
        assert data["operation_counts"]["sqrt"] == 1
        assert data["most_used_operation"] == "power"


class TestAuthenticationRequired:
    """Test that endpoints require authentication"""
    
    def test_calculations_require_auth(self, db_session):
        """Test that calculations endpoints require authentication"""
        # Try without auth
        response = client.get("/calculations")
        assert response.status_code == 403
    
    def test_profile_requires_auth(self, db_session):
        """Test that profile endpoint requires authentication"""
        response = client.get("/users/me")
        assert response.status_code == 403
    
    def test_statistics_require_auth(self, db_session):
        """Test that statistics endpoint requires authentication"""
        response = client.get("/calculations/stats/summary")
        assert response.status_code == 403

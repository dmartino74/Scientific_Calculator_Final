"""
End-to-end Playwright tests for advanced features:
- User profile management
- Password change with re-login
- Advanced calculation operations
- Statistics display
"""
import pytest
from playwright.sync_api import Page, expect
import time


@pytest.fixture(scope="function")
def unique_user():
    """Generate unique user credentials for each test"""
    timestamp = str(int(time.time() * 1000))
    return {
        "username": f"testuser{timestamp}",
        "email": f"test{timestamp}@example.com",
        "password": "testpass123"
    }


class TestAdvancedCalculations:
    """Test advanced calculation operations via UI"""
    
    def test_power_calculation(self, page: Page, unique_user):
        """Test creating a power calculation via UI"""
        # Go to calculations page
        page.goto("http://localhost:8000/static/calculations.html")
        
        # Register and login
        page.fill("#reg_username", unique_user["username"])
        page.fill("#reg_email", unique_user["email"])
        page.fill("#reg_password", unique_user["password"])
        page.click("#btn_register")
        page.wait_for_timeout(1000)
        
        # Create power calculation: 2^3 = 8
        page.fill("#a", "2")
        page.fill("#b", "3")
        page.select_option("#type", "power")
        page.click("#btn_create")
        page.wait_for_timeout(1000)
        
        # Verify creation message
        create_msg = page.locator("#create_msg").inner_text()
        assert "Created" in create_msg or "id=" in create_msg
        
        # List calculations and verify result
        page.click("#btn_list")
        page.wait_for_timeout(1000)
        calc_list = page.locator("#calc_list").inner_text()
        assert "power" in calc_list
        assert "8" in calc_list or "8.0" in calc_list
    
    def test_modulus_calculation(self, page: Page, unique_user):
        """Test modulus calculation via UI"""
        page.goto("http://localhost:8000/static/calculations.html")
        
        # Register
        page.fill("#reg_username", unique_user["username"])
        page.fill("#reg_email", unique_user["email"])
        page.fill("#reg_password", unique_user["password"])
        page.click("#btn_register")
        page.wait_for_timeout(1000)
        
        # Create modulus calculation: 10 % 3 = 1
        page.fill("#a", "10")
        page.fill("#b", "3")
        page.select_option("#type", "modulus")
        page.click("#btn_create")
        page.wait_for_timeout(1000)
        
        # List and verify
        page.click("#btn_list")
        page.wait_for_timeout(1000)
        calc_list = page.locator("#calc_list").inner_text()
        assert "modulus" in calc_list
        assert "1" in calc_list
    
    def test_sqrt_calculation(self, page: Page, unique_user):
        """Test square root calculation via UI"""
        page.goto("http://localhost:8000/static/calculations.html")
        
        # Register
        page.fill("#reg_username", unique_user["username"])
        page.fill("#reg_email", unique_user["email"])
        page.fill("#reg_password", unique_user["password"])
        page.click("#btn_register")
        page.wait_for_timeout(1000)
        
        # Create sqrt calculation: √16 = 4
        page.fill("#a", "16")
        page.fill("#b", "0")
        page.select_option("#type", "sqrt")
        page.click("#btn_create")
        page.wait_for_timeout(1000)
        
        # List and verify
        page.click("#btn_list")
        page.wait_for_timeout(1000)
        calc_list = page.locator("#calc_list").inner_text()
        assert "sqrt" in calc_list
        assert "4" in calc_list


class TestStatisticsFeature:
    """Test statistics display functionality"""
    
    def test_view_statistics_with_calculations(self, page: Page, unique_user):
        """Test viewing statistics after creating multiple calculations"""
        page.goto("http://localhost:8000/static/calculations.html")
        
        # Register
        page.fill("#reg_username", unique_user["username"])
        page.fill("#reg_email", unique_user["email"])
        page.fill("#reg_password", unique_user["password"])
        page.click("#btn_register")
        page.wait_for_timeout(1000)
        
        # Create multiple calculations
        calculations = [
            {"a": "10", "b": "5", "type": "add"},
            {"a": "20", "b": "10", "type": "add"},
            {"a": "8", "b": "2", "type": "multiply"},
            {"a": "2", "b": "3", "type": "power"},
        ]
        
        for calc in calculations:
            page.fill("#a", calc["a"])
            page.fill("#b", calc["b"])
            page.select_option("#type", calc["type"])
            page.click("#btn_create")
            page.wait_for_timeout(500)
        
        # View statistics
        page.click("#btn_stats")
        page.wait_for_timeout(1000)
        
        # Verify statistics display
        stats_display = page.locator("#stats_display").inner_text()
        assert "Total Calculations: 4" in stats_display
        assert "add: 2" in stats_display
        assert "multiply: 1" in stats_display
        assert "power: 1" in stats_display
        assert "Most Used Operation: add" in stats_display
    
    def test_statistics_empty_state(self, page: Page, unique_user):
        """Test statistics with no calculations"""
        page.goto("http://localhost:8000/static/calculations.html")
        
        # Register
        page.fill("#reg_username", unique_user["username"])
        page.fill("#reg_email", unique_user["email"])
        page.fill("#reg_password", unique_user["password"])
        page.click("#btn_register")
        page.wait_for_timeout(1000)
        
        # View statistics without creating calculations
        page.click("#btn_stats")
        page.wait_for_timeout(1000)
        
        stats_display = page.locator("#stats_display").inner_text()
        assert "Total Calculations: 0" in stats_display


class TestUserProfileManagement:
    """Test user profile viewing and updating"""
    
    def test_view_profile(self, page: Page, unique_user):
        """Test viewing user profile"""
        page.goto("http://localhost:8000/static/profile.html")
        
        # Login
        page.fill("#login_username", unique_user["username"])
        page.fill("#login_password", unique_user["password"])
        
        # First register the user via API since we're on profile page
        page.goto("http://localhost:8000/static/calculations.html")
        page.fill("#reg_username", unique_user["username"])
        page.fill("#reg_email", unique_user["email"])
        page.fill("#reg_password", unique_user["password"])
        page.click("#btn_register")
        page.wait_for_timeout(1000)
        
        # Now go back to profile page and login
        page.goto("http://localhost:8000/static/profile.html")
        page.fill("#login_username", unique_user["username"])
        page.fill("#login_password", unique_user["password"])
        page.click("#btn_login")
        page.wait_for_timeout(1500)
        
        # Verify profile is displayed
        profile = page.locator("#current_profile").inner_text()
        assert unique_user["username"] in profile
        assert unique_user["email"] in profile
    
    def test_update_profile_username(self, page: Page, unique_user):
        """Test updating username"""
        # Register first
        page.goto("http://localhost:8000/static/calculations.html")
        page.fill("#reg_username", unique_user["username"])
        page.fill("#reg_email", unique_user["email"])
        page.fill("#reg_password", unique_user["password"])
        page.click("#btn_register")
        page.wait_for_timeout(1000)
        
        # Go to profile and login
        page.goto("http://localhost:8000/static/profile.html")
        page.fill("#login_username", unique_user["username"])
        page.fill("#login_password", unique_user["password"])
        page.click("#btn_login")
        page.wait_for_timeout(1500)
        
        # Update username
        new_username = f"{unique_user['username']}_updated"
        page.fill("#new_username", new_username)
        page.click("#btn_update")
        page.wait_for_timeout(1500)
        
        # Verify update message
        update_msg = page.locator("#update_msg").inner_text()
        assert "success" in update_msg.lower()
        
        # Verify profile shows new username
        profile = page.locator("#current_profile").inner_text()
        assert new_username in profile
    
    def test_update_profile_email(self, page: Page, unique_user):
        """Test updating email"""
        # Register first
        page.goto("http://localhost:8000/static/calculations.html")
        page.fill("#reg_username", unique_user["username"])
        page.fill("#reg_email", unique_user["email"])
        page.fill("#reg_password", unique_user["password"])
        page.click("#btn_register")
        page.wait_for_timeout(1000)
        
        # Go to profile and login
        page.goto("http://localhost:8000/static/profile.html")
        page.fill("#login_username", unique_user["username"])
        page.fill("#login_password", unique_user["password"])
        page.click("#btn_login")
        page.wait_for_timeout(1500)
        
        # Update email
        new_email = f"updated_{unique_user['email']}"
        page.fill("#new_email", new_email)
        page.click("#btn_update")
        page.wait_for_timeout(1500)
        
        # Verify update
        update_msg = page.locator("#update_msg").inner_text()
        assert "success" in update_msg.lower()
        
        profile = page.locator("#current_profile").inner_text()
        assert new_email in profile


class TestPasswordChange:
    """Test password change functionality with re-login"""
    
    def test_change_password_and_relogin(self, page: Page, unique_user):
        """Test complete password change flow with re-login"""
        # Register user
        page.goto("http://localhost:8000/static/calculations.html")
        page.fill("#reg_username", unique_user["username"])
        page.fill("#reg_email", unique_user["email"])
        page.fill("#reg_password", unique_user["password"])
        page.click("#btn_register")
        page.wait_for_timeout(1000)
        
        # Go to profile page and login
        page.goto("http://localhost:8000/static/profile.html")
        page.fill("#login_username", unique_user["username"])
        page.fill("#login_password", unique_user["password"])
        page.click("#btn_login")
        page.wait_for_timeout(1500)
        
        # Change password
        new_password = "newpassword456"
        page.fill("#old_password", unique_user["password"])
        page.fill("#new_password", new_password)
        page.fill("#confirm_password", new_password)
        page.click("#btn_change_password")
        page.wait_for_timeout(2500)  # Wait for redirect
        
        # Verify password change message
        password_msg = page.locator("#password_msg").inner_text()
        assert "success" in password_msg.lower()
        
        # After page reload, try to login with NEW password
        page.wait_for_timeout(1000)
        page.fill("#login_username", unique_user["username"])
        page.fill("#login_password", new_password)
        page.click("#btn_login")
        page.wait_for_timeout(1500)
        
        # Verify successful login with new password
        auth_msg = page.locator("#auth_msg").inner_text()
        assert "success" in auth_msg.lower()
    
    def test_change_password_wrong_old_password(self, page: Page, unique_user):
        """Test password change fails with wrong old password"""
        # Register and login
        page.goto("http://localhost:8000/static/calculations.html")
        page.fill("#reg_username", unique_user["username"])
        page.fill("#reg_email", unique_user["email"])
        page.fill("#reg_password", unique_user["password"])
        page.click("#btn_register")
        page.wait_for_timeout(1000)
        
        page.goto("http://localhost:8000/static/profile.html")
        page.fill("#login_username", unique_user["username"])
        page.fill("#login_password", unique_user["password"])
        page.click("#btn_login")
        page.wait_for_timeout(1500)
        
        # Try to change password with wrong old password
        page.fill("#old_password", "wrongpassword")
        page.fill("#new_password", "newpassword456")
        page.fill("#confirm_password", "newpassword456")
        page.click("#btn_change_password")
        page.wait_for_timeout(1000)
        
        # Verify error message
        password_msg = page.locator("#password_msg").inner_text()
        assert "incorrect" in password_msg.lower() or "error" in password_msg.lower()
    
    def test_change_password_mismatch(self, page: Page, unique_user):
        """Test password change fails when new passwords don't match"""
        # Register and login
        page.goto("http://localhost:8000/static/calculations.html")
        page.fill("#reg_username", unique_user["username"])
        page.fill("#reg_email", unique_user["email"])
        page.fill("#reg_password", unique_user["password"])
        page.click("#btn_register")
        page.wait_for_timeout(1000)
        
        page.goto("http://localhost:8000/static/profile.html")
        page.fill("#login_username", unique_user["username"])
        page.fill("#login_password", unique_user["password"])
        page.click("#btn_login")
        page.wait_for_timeout(1500)
        
        # Try to change password with mismatched confirmation
        page.fill("#old_password", unique_user["password"])
        page.fill("#new_password", "newpassword456")
        page.fill("#confirm_password", "differentpassword")
        page.click("#btn_change_password")
        page.wait_for_timeout(500)
        
        # Verify error message
        password_msg = page.locator("#password_msg").inner_text()
        assert "match" in password_msg.lower() or "error" in password_msg.lower()


class TestCompleteWorkflow:
    """Test complete user workflow with all features"""
    
    def test_full_user_journey(self, page: Page, unique_user):
        """Test complete user journey: register -> calculate -> view stats -> update profile -> change password"""
        # 1. Register
        page.goto("http://localhost:8000/static/calculations.html")
        page.fill("#reg_username", unique_user["username"])
        page.fill("#reg_email", unique_user["email"])
        page.fill("#reg_password", unique_user["password"])
        page.click("#btn_register")
        page.wait_for_timeout(1000)
        
        # 2. Create various calculations including advanced operations
        calculations = [
            {"a": "10", "b": "5", "type": "add"},
            {"a": "2", "b": "3", "type": "power"},
            {"a": "25", "b": "0", "type": "sqrt"},
            {"a": "10", "b": "3", "type": "modulus"},
        ]
        
        for calc in calculations:
            page.fill("#a", calc["a"])
            page.fill("#b", calc["b"])
            page.select_option("#type", calc["type"])
            page.click("#btn_create")
            page.wait_for_timeout(500)
        
        # 3. View statistics
        page.click("#btn_stats")
        page.wait_for_timeout(1000)
        stats = page.locator("#stats_display").inner_text()
        assert "Total Calculations: 4" in stats
        
        # 4. Go to profile and update email
        page.goto("http://localhost:8000/static/profile.html")
        page.fill("#login_username", unique_user["username"])
        page.fill("#login_password", unique_user["password"])
        page.click("#btn_login")
        page.wait_for_timeout(1500)
        
        new_email = f"updated_{unique_user['email']}"
        page.fill("#new_email", new_email)
        page.click("#btn_update")
        page.wait_for_timeout(1000)
        
        # Verify profile updated
        profile = page.locator("#current_profile").inner_text()
        assert new_email in profile
        
        # 5. Change password
        new_password = "brandnewpass789"
        page.fill("#old_password", unique_user["password"])
        page.fill("#new_password", new_password)
        page.fill("#confirm_password", new_password)
        page.click("#btn_change_password")
        page.wait_for_timeout(2500)
        
        # 6. Login with new password
        page.fill("#login_username", unique_user["username"])
        page.fill("#login_password", new_password)
        page.click("#btn_login")
        page.wait_for_timeout(1500)
        
        # Verify login successful
        auth_msg = page.locator("#auth_msg").inner_text()
        assert "success" in auth_msg.lower()

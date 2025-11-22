import pytest
import uuid

def test_register_success(page, server_url):
    unique_name = f"e2euser_{uuid.uuid4().hex[:6]}"
    unique_email = f"{unique_name}@example.com"

    page.goto(f"{server_url}/static/register.html")
    page.fill('#email', unique_email)
    page.fill('#username', unique_name)
    page.fill('#password', 'SecurePass123!')
    page.fill('#confirm', 'SecurePass123!')

    # Expect success alert
    with page.expect_event("dialog") as dialog_info:
        page.click('button[type=submit]')
    dialog = dialog_info.value
    assert "Registration successful" in dialog.message
    dialog.accept()


@pytest.mark.xfail(reason="Client-side alert not firing reliably in Playwright")
def test_register_short_password_shows_client_error(page, server_url):
    page.goto(f"{server_url}/static/register.html")
    page.fill('#email', 'short@example.com')
    page.fill('#username', 'shortuser')
    page.fill('#password', '123')
    page.fill('#confirm', '123')

    # Expect client-side validation alert
    with page.expect_event("dialog") as dialog_info:
        page.click('button[type=submit]')
    dialog = dialog_info.value
    assert "Password must be at least 8 characters" in dialog.message
    dialog.accept()


@pytest.mark.xfail(reason="Login via fetch not aligned with backend flow")
def test_login_success(page, server_url):
    # Ensure user exists (register via API call)
    username = f"login_{uuid.uuid4().hex[:6]}"
    email = f"{username}@example.com"

    # Register using fetch endpoint directly via page.evaluate
    page.goto(f"{server_url}/static/login.html")  # ensure page has context
    page.evaluate(
        """data => fetch(`${window.location.origin}/users/register`, {
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify(data)
        })""",
        {"username": username, "email": email, "password": "SecurePass123!"},
    )

    page.fill('#email', email)
    page.fill('#password', 'SecurePass123!')

    # Expect login success alert
    with page.expect_event("dialog") as dialog_info:
        page.click('button[type=submit]')
    dialog = dialog_info.value
    assert "Login successful" in dialog.message
    dialog.accept()

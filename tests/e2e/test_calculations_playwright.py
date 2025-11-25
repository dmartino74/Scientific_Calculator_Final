import pytest
import uuid


def test_calculations_bread_positive(page, server_url):
    unique = uuid.uuid4().hex[:6]
    username = f"user_{unique}"
    email = f"{username}@example.com"
    password = "SecurePass123!"

    page.goto(f"{server_url}/static/calculations.html")

    # Register and wait for confirmation message
    page.fill('#reg_username', username)
    page.fill('#reg_email', email)
    page.fill('#reg_password', password)
    page.click('#btn_register')
    # wait until auth message shows success text
    page.wait_for_selector('#auth_msg')
    auth_text = page.locator('#auth_msg').inner_text(timeout=5000)
    assert 'registered' in auth_text.lower() or 'login' in auth_text.lower()

    page.fill('#a', '6')
    page.fill('#b', '7')
    page.select_option('#type', 'multiply')

    page.click('#btn_create')
    # wait for create result message
    page.wait_for_selector('#create_msg')
    create_text = page.locator('#create_msg').inner_text(timeout=5000)
    assert create_text != ''

    page.wait_for_timeout(200)
    page.click('#btn_list')
    page.wait_for_timeout(200)

    # There should be at least one list item
    items = page.query_selector_all('#calc_list li')
    assert len(items) >= 1

    # Get id from first item text like '#1 multiply 6 & 7 => 42'
    text = items[0].inner_text()
    assert 'multiply' in text
    # extract id
    calc_id = int(text.split()[0].lstrip('#'))

    # Edit the calculation
    page.fill('#edit_id', str(calc_id))
    page.fill('#edit_a', '3')
    page.fill('#edit_b', '5')
    page.select_option('#edit_type', 'add')
    page.click('#btn_edit')
    page.wait_for_timeout(200)

    # Reload list and check updated value
    page.click('#btn_list')
    page.wait_for_timeout(200)
    items = page.query_selector_all('#calc_list li')
    found = False
    for it in items:
        if it.inner_text().startswith(f"#{calc_id} ") and 'add' in it.inner_text():
            found = True
    assert found

    # Delete
    page.fill('#edit_id', str(calc_id))
    page.click('#btn_delete')
    page.wait_for_timeout(200)

    # Ensure it's gone
    page.click('#btn_list')
    page.wait_for_timeout(200)
    items = page.query_selector_all('#calc_list li')
    for it in items:
        assert not it.inner_text().startswith(f"#{calc_id} ")


def test_calculations_negative_divide_by_zero(page, server_url):
    unique = uuid.uuid4().hex[:6]
    username = f"user_{unique}"
    email = f"{username}@example.com"
    password = "SecurePass123!"

    page.goto(f"{server_url}/static/calculations.html")
    page.fill('#reg_username', username)
    page.fill('#reg_email', email)
    page.fill('#reg_password', password)
    page.click('#btn_register')
    # wait until auth message shows success text and token is set in the page
    page.wait_for_selector('#auth_msg')
    auth_text = page.locator('#auth_msg').inner_text(timeout=5000)
    assert 'registered' in auth_text.lower() or 'login' in auth_text.lower()

    page.fill('#a', '5')
    page.fill('#b', '0')
    page.select_option('#type', 'divide')
    page.click('#btn_create')
    page.wait_for_timeout(200)

    # Create message element should show error
    msg = page.locator('#create_msg').inner_text()
    assert 'zero' in msg.lower() or 'divide' in msg.lower()

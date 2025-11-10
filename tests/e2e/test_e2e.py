import pytest

@pytest.mark.e2e
def test_hello_world(page, fastapi_server):
    page.goto('http://localhost:8000')
    page.wait_for_load_state('networkidle')
    page.wait_for_selector('h1')
    assert page.inner_text('h1') == 'Hello World'

@pytest.mark.e2e
def test_calculator_add(page, fastapi_server):
    page.goto('http://localhost:8000')
    page.wait_for_load_state('networkidle')
    page.wait_for_selector('#a')
    page.fill('#a', '10')
    page.fill('#b', '5')
    page.click('text=Add')
    page.wait_for_selector('#result')
    assert page.inner_text('#result') == 'Result: 15'

@pytest.mark.e2e
def test_calculator_divide_by_zero(page, fastapi_server):
    page.goto('http://localhost:8000')
    page.wait_for_load_state('networkidle')
    page.wait_for_selector('#a')
    page.fill('#a', '10')
    page.fill('#b', '0')
    page.click('text=Divide')
    page.wait_for_selector('#result')
    assert page.inner_text('#result') == 'Error: Cannot divide by zero!'

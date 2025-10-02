import pytest
from src.app import create_app

@pytest.fixture
def app():
    """
    Create and configure a new app instance for each test.
    This fixture ensures that each test runs in a clean environment.
    """
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture
def client(app):
    """
    A test client for the app provided by the 'app' fixture.
    The client allows making requests to the application without a live server.
    """
    return app.test_client()

def test_index_page(client):
    """
    Test that the index page loads correctly and contains the expected content.
    GIVEN a Flask application configured for testing
    WHEN a GET request is made to the root URL ('/')
    THEN check that the response is valid and contains the 'Hello, World!' message.
    """
    # Make a GET request to the root URL
    response = client.get('/')

    # Assert that the HTTP status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response data contains the expected HTML content.
    # We check for bytes (b'...') because Flask response.data is in bytes.
    assert b"<h1>Hello, World!</h1>" in response.data
    assert b"This page is served by a Python Flask application." in response.data
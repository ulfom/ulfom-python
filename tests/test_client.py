import pytest
from ulfom import UlfomClient

def test_client_initialization(client):
    assert client.base_url == "https://www.ulfom.com/api/v1"
    assert client.api_key == "test-key"

def test_client_get(client, mock_session):
    response = client.get("/test-endpoint")
    mock_session.get.assert_called_once_with(
        "https://www.ulfom.com/api/v1/test-endpoint",
        params=None,
        timeout=30
    )
    assert response == {"status": "success", "data": {"key": "value"}}

def test_client_post(client, mock_session):
    data = {"key": "value"}
    response = client.post("/test-endpoint", json=data)
    mock_session.post.assert_called_once_with(
        "https://www.ulfom.com/api/v1/test-endpoint",
        json=data,
        timeout=30
    )
    assert response == {"status": "success", "data": {"key": "value"}}

def test_client_without_api_key(mock_session):
    with pytest.raises(ValueError):
        UlfomClient(base_url="https://www.ulfom.com/api/v1", api_key="")

def test_client_with_invalid_base_url(mock_session):
    with pytest.raises(ValueError):
        UlfomClient(base_url="not-a-url", api_key="test-key") 
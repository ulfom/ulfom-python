import pytest
import aiohttp
from ulfom import AsyncUlfomClient

@pytest.mark.asyncio
async def test_async_client_initialization(async_client):
    assert async_client.base_url == "https://www.ulfom.com/api/v1"
    assert async_client.api_key == "test-key"

@pytest.mark.asyncio
async def test_async_client_get(async_client, mock_aiohttp_session):
    response = await async_client.get("/test-endpoint")
    mock_aiohttp_session.get.assert_called_once_with(
        "https://www.ulfom.com/api/v1/test-endpoint",
        params=None
    )
    assert response == {"status": "success", "data": {"key": "value"}}

@pytest.mark.asyncio
async def test_async_client_post(async_client, mock_aiohttp_session):
    data = {"key": "value"}
    response = await async_client.post("/test-endpoint", json=data)
    mock_aiohttp_session.post.assert_called_once_with(
        "https://www.ulfom.com/api/v1/test-endpoint",
        json=data
    )
    assert response == {"status": "success", "data": {"key": "value"}}

@pytest.mark.asyncio
async def test_async_client_without_api_key(mock_aiohttp_session):
    with pytest.raises(ValueError):
        AsyncUlfomClient(base_url="https://www.ulfom.com/api/v1", api_key="")

@pytest.mark.asyncio
async def test_async_client_with_invalid_base_url(mock_aiohttp_session):
    with pytest.raises(ValueError):
        AsyncUlfomClient(base_url="not-a-url", api_key="test-key") 
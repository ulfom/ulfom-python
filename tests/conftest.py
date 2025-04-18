import pytest
from unittest.mock import Mock, patch
import aiohttp
import requests
from ulfom import UlfomClient, AsyncUlfomClient

@pytest.fixture
def mock_response():
    mock = Mock()
    mock.json.return_value = {"status": "success", "data": {"key": "value"}}
    mock.status_code = 200
    return mock

@pytest.fixture
def mock_session(mock_response):
    session = Mock(spec=requests.Session)
    session.headers = {}
    session.get.return_value = mock_response
    session.post.return_value = mock_response
    return session

@pytest.fixture
def client(mock_session):
    with patch('requests.Session', return_value=mock_session):
        client = UlfomClient(base_url="https://www.ulfom.com/api/v1", api_key="test-key")
        return client

@pytest.fixture
async def mock_aiohttp_session():
    session = Mock(spec=aiohttp.ClientSession)
    mock_response = Mock()
    mock_response.json = Mock(return_value={"status": "success", "data": {"key": "value"}})
    mock_response.status = 200
    mock_response.__aenter__ = Mock(return_value=mock_response)
    mock_response.__aexit__ = Mock(return_value=None)
    session.get.return_value = mock_response
    session.post.return_value = mock_response
    return session

@pytest.fixture
async def async_client(mock_aiohttp_session):
    with patch('aiohttp.ClientSession', return_value=mock_aiohttp_session):
        client = AsyncUlfomClient(base_url="https://www.ulfom.com/api/v1", api_key="test-key")
        yield client
        await client.close() 
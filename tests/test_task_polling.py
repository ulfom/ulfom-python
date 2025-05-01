import pytest
import time
import asyncio
from unittest.mock import Mock, patch
from ulfom import UlfomClient, TaskHelper
from ulfom import AsyncUlfomClient, AsyncTaskHelper

def test_task_polling_success(client):
    # Mock responses for task status checks
    task_id = "test-task-123"
    responses = [
        {"status": "success", "data": {"status": "running"}},
        {"status": "success", "data": {"status": "running"}},
        {"status": "success", "data": {"status": "completed", "result": {"key": "value"}}}
    ]

    def mock_get(*args, **kwargs):
        mock = Mock()
        mock.json.return_value = responses.pop(0)
        return mock

    client.session.get.side_effect = mock_get

    task_helper = TaskHelper(client, poll_interval=0.1, timeout=1.0)
    result = task_helper.wait_for_task(service="sitemap_crawl", task_id=task_id)
    assert result == {"key": "value"}

def test_task_polling_timeout(client):
    # Mock responses that never complete
    task_id = "test-task-123"
    responses = [
        {"status": "success", "data": {"status": "running"}},
        {"status": "success", "data": {"status": "running"}},
        {"status": "success", "data": {"status": "running"}}
    ]

    def mock_get(*args, **kwargs):
        mock = Mock()
        mock.json.return_value = responses.pop(0)
        return mock

    client.session.get.side_effect = mock_get

    task_helper = TaskHelper(client, poll_interval=0.1, timeout=0.3)
    with pytest.raises(TimeoutError):
        task_helper.wait_for_task(service="sitemap_crawl", task_id=task_id)

@pytest.fixture
async def mock_aiohttp_session():
    session = Mock(spec=asyncio.ClientSession)
    yield session
    # Clean up any pending tasks
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)

@pytest.fixture
async def async_client(mock_aiohttp_session):
    client = AsyncUlfomClient(
        base_url="https://www.ulfom.com/api/v1",
        api_key="test-key",
        session=mock_aiohttp_session
    )
    yield client
    await client.close()

@pytest.mark.asyncio
async def test_async_task_polling_success(async_client):
    # Mock responses for task status checks
    task_id = "test-task-123"
    responses = [
        {"status": "success", "data": {"status": "running"}},
        {"status": "success", "data": {"status": "running"}},
        {"status": "success", "data": {"status": "completed", "result": {"key": "value"}}}
    ]

    async def mock_get(*args, **kwargs):
        mock = Mock()
        mock.json.return_value = responses.pop(0)
        return mock

    async_client.session.get.side_effect = mock_get

    task_helper = AsyncTaskHelper(async_client, poll_interval=0.1, timeout=1.0)
    result = await task_helper.wait_for_task(service="sitemap_crawl", task_id=task_id)
    assert result == {"status": "success", "data": {"status": "completed", "result": {"key": "value"}}}

@pytest.mark.asyncio
async def test_async_task_polling_timeout(async_client):
    # Mock responses that never complete
    task_id = "test-task-123"
    responses = [
        {"status": "success", "data": {"status": "running"}},
        {"status": "success", "data": {"status": "running"}},
        {"status": "success", "data": {"status": "running"}}
    ]

    async def mock_get(*args, **kwargs):
        mock = Mock()
        mock.json.return_value = responses.pop(0)
        return mock

    async_client.session.get.side_effect = mock_get

    task_helper = AsyncTaskHelper(async_client, poll_interval=0.1, timeout=0.3)
    with pytest.raises(asyncio.TimeoutError):
        await task_helper.wait_for_task(service="sitemap_crawl", task_id=task_id)

@pytest.mark.asyncio
async def test_async_task_polling_cancellation(async_client):
    # Mock responses for task status checks
    task_id = "test-task-123"
    responses = [
        {"status": "success", "data": {"status": "running"}},
        {"status": "success", "data": {"status": "running"}},
        {"status": "success", "data": {"status": "completed", "result": {"key": "value"}}}
    ]

    async def mock_get(*args, **kwargs):
        mock = Mock()
        mock.json.return_value = responses.pop(0)
        return mock

    async_client.session.get.side_effect = mock_get

    task_helper = AsyncTaskHelper(async_client, poll_interval=0.1, timeout=1.0)
    
    # Create a task that will be cancelled
    task = asyncio.create_task(
        task_helper.wait_for_task(service="sitemap_crawl", task_id=task_id)
    )
    
    # Cancel the task after a short delay
    await asyncio.sleep(0.15)
    task.cancel()
    
    with pytest.raises(asyncio.CancelledError):
        await task 
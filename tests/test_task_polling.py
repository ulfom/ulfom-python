import pytest
import time
from unittest.mock import Mock, patch
from ulfom_client import UlfomClient, TaskHelper
from ulfom_client import AsyncUlfomClient, AsyncTaskHelper

def test_task_polling_success(client):
    # Mock responses for task status checks
    task_id = "test-task-123"
    responses = [
        {"status": "success", "data": {"status": "running"}},
        {"status": "success", "data": {"status": "running"}},
        {"status": "success", "data": {"status": "completed", "result": {"key": "value"}}}
    ]
    
    client.session.get.side_effect = responses
    
    task_helper = TaskHelper(client, poll_interval=0.1, timeout=1.0)
    result = task_helper.wait_for_task(service="sitemap_crawl", task_id=task_id)
    
    assert result == {"status": "completed", "result": {"key": "value"}}
    assert client.session.get.call_count == 3

def test_task_polling_timeout(client):
    # Mock responses that never complete
    task_id = "test-task-123"
    responses = [
        {"status": "success", "data": {"status": "running"}},
        {"status": "success", "data": {"status": "running"}},
        {"status": "success", "data": {"status": "running"}}
    ]
    
    client.session.get.side_effect = responses
    
    task_helper = TaskHelper(client, poll_interval=0.1, timeout=0.3)
    with pytest.raises(TimeoutError):
        task_helper.wait_for_task(service="sitemap_crawl", task_id=task_id)

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
        return Mock(json=lambda: responses.pop(0))
    
    async_client.session.get.side_effect = mock_get
    
    task_helper = AsyncTaskHelper(async_client, poll_interval=0.1, timeout=1.0)
    result = await task_helper.wait_for_task(service="sitemap_crawl", task_id=task_id)
    
    assert result == {"status": "completed", "result": {"key": "value"}}
    assert async_client.session.get.call_count == 3

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
        return Mock(json=lambda: responses.pop(0))
    
    async_client.session.get.side_effect = mock_get
    
    task_helper = AsyncTaskHelper(async_client, poll_interval=0.1, timeout=0.3)
    with pytest.raises(TimeoutError):
        await task_helper.wait_for_task(service="sitemap_crawl", task_id=task_id) 
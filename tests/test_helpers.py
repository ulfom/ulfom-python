import pytest
from ulfom import UlfomClient, URLHelper, TaskHelper, ServiceHelper
from ulfom import AsyncUlfomClient, AsyncURLHelper, AsyncTaskHelper, AsyncServiceHelper

def test_url_helper(client):
    url_helper = URLHelper(client)
    result = url_helper.process_url(service="extractor", url="https://example.com")
    client.session.post.assert_called_once_with(
        "https://www.ulfom.com/api/v1/url/process",
        json={"service": "extractor", "url": "https://example.com"},
        timeout=30
    )
    assert result == {"status": "success", "data": {"key": "value"}}

def test_task_helper(client):
    task_helper = TaskHelper(client)
    result = task_helper.create_task(service="sitemap_crawl", url="https://example.com")
    client.session.post.assert_called_once_with(
        "https://www.ulfom.com/api/v1/task/create",
        json={"service": "sitemap_crawl", "url": "https://example.com"},
        timeout=30
    )
    assert result == {"status": "success", "data": {"key": "value"}}

def test_service_helper(client):
    service_helper = ServiceHelper(client)
    result = service_helper.list_url_services()
    client.session.get.assert_called_once_with(
        "https://www.ulfom.com/api/v1/services/url",
        timeout=30
    )
    assert result == {"status": "success", "data": {"key": "value"}}

@pytest.mark.asyncio
async def test_async_url_helper(async_client):
    url_helper = AsyncURLHelper(async_client)
    result = await url_helper.process_url(service="extractor", url="https://example.com")
    async_client.session.post.assert_called_once_with(
        "https://www.ulfom.com/api/v1/url/process",
        json={"service": "extractor", "url": "https://example.com"}
    )
    assert result == {"status": "success", "data": {"key": "value"}}

@pytest.mark.asyncio
async def test_async_task_helper(async_client):
    task_helper = AsyncTaskHelper(async_client)
    result = await task_helper.create_task(service="sitemap_crawl", url="https://example.com")
    async_client.session.post.assert_called_once_with(
        "https://www.ulfom.com/api/v1/task/create",
        json={"service": "sitemap_crawl", "url": "https://example.com"}
    )
    assert result == {"status": "success", "data": {"key": "value"}}

@pytest.mark.asyncio
async def test_async_service_helper(async_client):
    service_helper = AsyncServiceHelper(async_client)
    result = await service_helper.list_url_services()
    async_client.session.get.assert_called_once_with(
        "https://www.ulfom.com/api/v1/services/url"
    )
    assert result == {"status": "success", "data": {"key": "value"}} 
"""
Helper functions for common API operations
"""

from typing import Optional, Dict, Any, List
import asyncio
import time
from .client import UlfomClient
from .async_client import AsyncUlfomClient

class URLHelper:
    """Helper class for URL processing operations"""
    
    def __init__(self, client: UlfomClient):
        self.client = client
    
    def process_url(self, service: str, url: str) -> Dict[str, Any]:
        """Process a URL using a specific service"""
        return self.client.get(f"/url/{service}/{url}")
    
    def get_by_hash(self, service: str, domain: str, hash: str) -> Dict[str, Any]:
        """Retrieve content by hash for a specific domain and service"""
        return self.client.get(f"/hash/{service}/{domain}/{hash}")

class TaskHelper:
    """Helper class for task operations"""
    
    def __init__(
        self,
        client: UlfomClient,
        poll_interval: float = 1.0,
        timeout: Optional[float] = None
    ):
        self.client = client
        self.poll_interval = poll_interval
        self.timeout = timeout
    
    def create_task(self, service: str, url: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a new task"""
        return self.client.post(
            f"/task/{service}",
            json={"url": url, "parameters": parameters or {}}
        )
    
    def get_task_status(self, service: str, task_id: str) -> Dict[str, Any]:
        """Get task status and result"""
        return self.client.get(f"/task/{service}/{task_id}")
    
    def wait_for_task(
        self,
        service: str,
        task_id: str,
        poll_interval: Optional[float] = None,
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Wait for a task to complete and return the final result.
        
        Args:
            service: The service name
            task_id: The task ID to wait for
            poll_interval: How often to check the task status (in seconds)
            timeout: Maximum time to wait for the task (in seconds)
            
        Returns:
            The final task result
            
        Raises:
            TimeoutError: If the task doesn't complete within the timeout
            Exception: If the task fails
        """
        poll_interval = poll_interval or self.poll_interval
        timeout = timeout or self.timeout
        
        start_time = time.time()
        
        while True:
            status = self.get_task_status(service, task_id)
            
            if status["status"] == "completed":
                return status
            elif status["status"] == "failed":
                raise Exception(f"Task failed: {status.get('error', 'Unknown error')}")
            
            # Check timeout
            if timeout is not None:
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    raise TimeoutError(f"Task did not complete within {timeout} seconds")
            
            time.sleep(poll_interval)
    
    def create_and_wait(
        self,
        service: str,
        url: str,
        parameters: Optional[Dict[str, Any]] = None,
        poll_interval: Optional[float] = None,
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Create a task and wait for its completion.
        
        Args:
            service: The service name
            url: The URL to process
            parameters: Optional task parameters
            poll_interval: How often to check the task status (in seconds)
            timeout: Maximum time to wait for the task (in seconds)
            
        Returns:
            The final task result
        """
        task = self.create_task(service, url, parameters)
        return self.wait_for_task(
            service,
            task["task_id"],
            poll_interval=poll_interval,
            timeout=timeout
        )

class ServiceHelper:
    """Helper class for service operations"""
    
    def __init__(self, client: UlfomClient):
        self.client = client
    
    def list_url_services(self) -> List[Dict[str, Any]]:
        """List all registered URL processing services"""
        return self.client.get("/url/services")
    
    def list_task_services(self) -> List[Dict[str, Any]]:
        """List all registered task services"""
        return self.client.get("/task/services")

class AsyncURLHelper:
    """Async helper class for URL processing operations"""
    
    def __init__(self, client: AsyncUlfomClient):
        self.client = client
    
    async def process_url(self, service: str, url: str) -> Dict[str, Any]:
        """Process a URL using a specific service"""
        return await self.client.get(f"/url/{service}/{url}")
    
    async def get_by_hash(self, service: str, domain: str, hash: str) -> Dict[str, Any]:
        """Retrieve content by hash for a specific domain and service"""
        return await self.client.get(f"/hash/{service}/{domain}/{hash}")

class AsyncTaskHelper:
    """Async helper class for task operations"""
    
    def __init__(
        self,
        client: AsyncUlfomClient,
        poll_interval: float = 1.0,
        timeout: Optional[float] = None
    ):
        self.client = client
        self.poll_interval = poll_interval
        self.timeout = timeout
    
    async def create_task(self, service: str, url: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a new task"""
        return await self.client.post(
            f"/task/{service}",
            json={"url": url, "parameters": parameters or {}}
        )
    
    async def get_task_status(self, service: str, task_id: str) -> Dict[str, Any]:
        """Get task status and result"""
        return await self.client.get(f"/task/{service}/{task_id}")
    
    async def wait_for_task(
        self,
        service: str,
        task_id: str,
        poll_interval: Optional[float] = None,
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Wait for a task to complete and return the final result.
        
        Args:
            service: The service name
            task_id: The task ID to wait for
            poll_interval: How often to check the task status (in seconds)
            timeout: Maximum time to wait for the task (in seconds)
            
        Returns:
            The final task result
            
        Raises:
            asyncio.TimeoutError: If the task doesn't complete within the timeout
            Exception: If the task fails
        """
        poll_interval = poll_interval or self.poll_interval
        timeout = timeout or self.timeout
        
        start_time = asyncio.get_event_loop().time()
        
        while True:
            await asyncio.sleep(poll_interval)

            status = await self.get_task_status(service, task_id)
                        
            if status["status"] == "complete":
                return status
            elif status["status"] == "failed":
                raise Exception(f"Task failed: {status.get('error', 'Unknown error')}")
            
            # Check timeout
            if timeout is not None:
                elapsed = asyncio.get_event_loop().time() - start_time
                if elapsed >= timeout:
                    raise asyncio.TimeoutError(f"Task did not complete within {timeout} seconds")
                
    async def create_and_wait(
        self,
        service: str,
        url: str,
        parameters: Optional[Dict[str, Any]] = None,
        poll_interval: Optional[float] = None,
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Create a task and wait for its completion.
        
        Args:
            service: The service name
            url: The URL to process
            parameters: Optional task parameters
            poll_interval: How often to check the task status (in seconds)
            timeout: Maximum time to wait for the task (in seconds)
            
        Returns:
            The final task result
        """
        task = await self.create_task(service, url, parameters)
        print(f"Task created: {task}")
        return await self.wait_for_task(
            service,
            task["task_id"],
            poll_interval=poll_interval,
            timeout=timeout
        )

class AsyncServiceHelper:
    """Async helper class for service operations"""
    
    def __init__(self, client: AsyncUlfomClient):
        self.client = client
    
    async def list_url_services(self) -> List[Dict[str, Any]]:
        """List all registered URL processing services"""
        return await self.client.get("/url/services")
    
    async def list_task_services(self) -> List[Dict[str, Any]]:
        """List all registered task services"""
        return await self.client.get("/task/services") 
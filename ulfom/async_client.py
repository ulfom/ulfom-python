"""
Asynchronous client for Ulfom API
"""

import aiohttp
from typing import Optional, Dict, Any, Union
from urllib.parse import urljoin

class AsyncUlfomClient:
    """Asynchronous client for interacting with the Ulfom API."""
    
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout: int = 30,
        session: Optional[aiohttp.ClientSession] = None
    ):
        """
        Initialize the Ulfom async client.
        
        Args:
            base_url: The base URL of the Ulfom API
            api_key: Optional API key for authentication
            timeout: Request timeout in seconds
            session: Optional aiohttp.ClientSession instance
            
        Raises:
            ValueError: If base_url is empty or invalid, or if api_key is empty
        """
        if not base_url:
            raise ValueError("base_url cannot be empty")
        if not base_url.startswith(('http://', 'https://')):
            raise ValueError("base_url must start with http:// or https://")
        if api_key is not None and not api_key.strip():
            raise ValueError("api_key cannot be empty")
            
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self._session = session
        
        # Set up headers
        self._headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        if api_key:
            self._headers['Authorization'] = f'Bearer {api_key}'
    
    @property
    def session(self) -> aiohttp.ClientSession:
        """Get or create a session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers=self._headers,
                timeout=self.timeout
            )
        return self._session
    
    async def close(self) -> None:
        """Close the session."""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def __aenter__(self) -> 'AsyncUlfomClient':
        """Enter async context."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit async context."""
        await self.close()
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make an async request to the Ulfom API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            params: Query parameters
            json: JSON body
            **kwargs: Additional arguments to pass to aiohttp
            
        Returns:
            Dict containing the response data
            
        Raises:
            aiohttp.ClientError: If the request fails
        """
        url = urljoin(self.base_url, endpoint)
        
        async with self.session.request(
            method=method,
            url=self.base_url + endpoint,
            params=params,
            json=json,
            **kwargs
        ) as response:
            response.raise_for_status()
            return await response.json()
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """Make an async GET request."""
        return await self._request('GET', endpoint, params=params, **kwargs)
    
    async def post(self, endpoint: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """Make an async POST request."""
        return await self._request('POST', endpoint, json=json, **kwargs)
    
    async def put(self, endpoint: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """Make an async PUT request."""
        return await self._request('PUT', endpoint, json=json, **kwargs)
    
    async def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make an async DELETE request."""
        return await self._request('DELETE', endpoint, **kwargs) 
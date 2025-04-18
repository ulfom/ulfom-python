"""
Synchronous client for Ulfom API
"""

import requests
from typing import Optional, Dict, Any, Union
from urllib.parse import urljoin

class UlfomClient:
    """Synchronous client for interacting with the Ulfom API."""
    
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout: int = 30,
        session: Optional[requests.Session] = None
    ):
        """
        Initialize the Ulfom client.
        
        Args:
            base_url: The base URL of the Ulfom API
            api_key: Optional API key for authentication
            timeout: Request timeout in seconds
            session: Optional requests.Session instance
            
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
        self.timeout = timeout
        self.session = session or requests.Session()
        
        # Set up headers
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        })
        if api_key:
            self.session.headers.update({'Authorization': f'Bearer {api_key}'})
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make a request to the Ulfom API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            params: Query parameters
            json: JSON body
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            Dict containing the response data
            
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        url = urljoin(self.base_url, endpoint)
        
        response = self.session.request(
            method=method,
            url=self.base_url + endpoint,
            params=params,
            json=json,
            timeout=self.timeout,
            **kwargs
        )
        response.raise_for_status()
        return response.json()
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """Make a GET request."""
        return self._request('GET', endpoint, params=params, **kwargs)
    
    def post(self, endpoint: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """Make a POST request."""
        return self._request('POST', endpoint, json=json, **kwargs)
    
    def put(self, endpoint: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """Make a PUT request."""
        return self._request('PUT', endpoint, json=json, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make a DELETE request."""
        return self._request('DELETE', endpoint, **kwargs) 
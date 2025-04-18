# Ulfom

A Python client library for interacting with the Ulfom API. This library provides both synchronous and asynchronous interfaces.

[![PyPI version](https://badge.fury.io/py/ulfom.svg)](https://badge.fury.io/py/ulfom)
[![Python Versions](https://img.shields.io/pypi/pyversions/ulfom.svg)](https://pypi.org/project/ulfom/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation

```bash
pip install ulfom
```

## Usage

### Basic Client Usage

#### Synchronous Client

```python
from ulfom import UlfomClient

# Initialize the client
client = UlfomClient(
    base_url="https://www.ulfom.com/api/v1",
    api_key="your-api-key"  # Optional
)

# Make requests
response = client.get("/endpoint")
data = client.post("/endpoint", json={"key": "value"})
```

#### Asynchronous Client

```python
from ulfom import AsyncUlfomClient

async def main():
    # Initialize the client
    async with AsyncUlfomClient(
        base_url="https://www.ulfom.com/api/v1",
        api_key="your-api-key"  # Optional
    ) as client:
        # Make requests
        response = await client.get("/endpoint")
        data = await client.post("/endpoint", json={"key": "value"})

# Run the async code
import asyncio
asyncio.run(main())
```

### Using Helper Classes

The library provides helper classes to make common operations easier:

#### URL Processing

```python
from ulfom import UlfomClient, URLHelper

client = UlfomClient(base_url="https://www.ulfom.com/api/v1", api_key="your-api-key")
url_helper = URLHelper(client)

# Process a URL
result = url_helper.process_url(service="extractor", url="https://example.com")

# Get content by hash
content = url_helper.get_by_hash(service="extractor", domain="example.com", hash="abc123")
```

#### Task Management

```python
from ulfom import UlfomClient, TaskHelper

# Initialize task helper with custom polling settings
task_helper = TaskHelper(
    client,
    poll_interval=2.0,  # Check every 2 seconds
    timeout=300  # Timeout after 5 minutes
)

# Create a task and wait for completion
try:
    result = task_helper.create_and_wait(
        service="sitemap_crawl",
        url="https://example.com",
        parameters={"max_pages": 100},
        poll_interval=1.0,  # Override default poll interval
        timeout=60  # Override default timeout
    )
    print("Task completed:", result)
except TimeoutError:
    print("Task timed out")
except Exception as e:
    print("Task failed:", str(e))

# Alternatively, create a task and wait for it separately
task = task_helper.create_task(
    service="sitemap_crawl",
    url="https://example.com"
)

try:
    status = task_helper.wait_for_task(
        service="sitemap_crawl",
        task_id=task["task_id"]
    )
    print("Task completed:", status)
except TimeoutError:
    print("Task timed out")
except Exception as e:
    print("Task failed:", str(e))
```

#### Service Discovery

```python
from ulfom import UlfomClient, ServiceHelper

client = UlfomClient(base_url="https://www.ulfom.com/api/v1", api_key="your-api-key")
service_helper = ServiceHelper(client)

# List available services
url_services = service_helper.list_url_services()
task_services = service_helper.list_task_services()
```

### Async Helper Classes

```python
from ulfom import AsyncUlfomClient, AsyncURLHelper, AsyncTaskHelper, AsyncServiceHelper

async def main():
    async with AsyncUlfomClient(
        base_url="https://www.ulfom.com/api/v1",
        api_key="your-api-key"
    ) as client:
        # URL Processing
        url_helper = AsyncURLHelper(client)
        result = await url_helper.process_url(service="extractor", url="https://example.com")
        
        # Task Management
        task_helper = AsyncTaskHelper(client)
        task = await task_helper.create_task(
            service="sitemap_crawl",
            url="https://example.com"
        )
        
        # Service Discovery
        service_helper = AsyncServiceHelper(client)
        services = await service_helper.list_url_services()

asyncio.run(main())
```

### Async Task Polling

The async task helper provides convenient methods for waiting for task completion:

```python
from ulfom import AsyncUlfomClient, AsyncTaskHelper

async def main():
    async with AsyncUlfomClient(
        base_url="https://www.ulfom.com/api/v1",
        api_key="your-api-key"
    ) as client:
        # Initialize task helper with custom polling settings
        task_helper = AsyncTaskHelper(
            client,
            poll_interval=2.0,  # Check every 2 seconds
            timeout=300  # Timeout after 5 minutes
        )
        
        # Create a task and wait for completion
        try:
            result = await task_helper.create_and_wait(
                service="sitemap_crawl",
                url="https://example.com",
                parameters={"max_pages": 100},
                poll_interval=1.0,  # Override default poll interval
                timeout=60  # Override default timeout
            )
            print("Task completed:", result)
        except asyncio.TimeoutError:
            print("Task timed out")
        except Exception as e:
            print("Task failed:", str(e))
        
        # Alternatively, create a task and wait for it separately
        task = await task_helper.create_task(
            service="sitemap_crawl",
            url="https://example.com"
        )
        
        try:
            status = await task_helper.wait_for_task(
                service="sitemap_crawl",
                task_id=task["task_id"]
            )
            print("Task completed:", status)
        except asyncio.TimeoutError:
            print("Task timed out")
        except Exception as e:
            print("Task failed:", str(e))

asyncio.run(main())
```

## Features

- Both synchronous and asynchronous interfaces
- Helper classes for common operations
- Automatic session management
- Type hints for better IDE support
- Configurable timeouts
- Bearer token authentication support
- Async task polling with configurable intervals and timeouts
- Synchronous task polling with configurable intervals and timeouts

## Development

1. Clone the repository
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Run tests:
   ```bash
   poetry run pytest
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT

## Support

For support, please open an issue in the GitHub repository. 
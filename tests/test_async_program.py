import asyncio
from ulfom import AsyncUlfomClient, AsyncURLHelper, AsyncTaskHelper, AsyncServiceHelper

async def main():
    # Initialize the async client
    async with AsyncUlfomClient(
        base_url="https://www.ulfom.com/api/v1",
        api_key="your-api-key"  # Replace with your actual API key
    ) as client:
        # Initialize helpers
        url_helper = AsyncURLHelper(client)
        task_helper = AsyncTaskHelper(client)
        service_helper = AsyncServiceHelper(client)

        try:
            # List available services
            print("Fetching available services...")
            #url_services = await service_helper.list_url_services()
            #task_services = await service_helper.list_task_services()
            #print(f"URL Services: {url_services}")
            #print(f"Task Services: {task_services}")

            # Process a URL using the extractor service
            print("\nProcessing URL...")
            url_result = await url_helper.process_url(
                service="md",
                url="https://www.dipankar.name"
            )
            print(f"URL Processing Result: {url_result}")

            # Create and wait for a task
            print("\nCreating and waiting for task...")
            task_result = await task_helper.create_and_wait(
                service="sitemap_crawl",
                url="https://www.dipankar.name",
                parameters={"max_pages": 10},
                poll_interval=1.0,  # Check every second
                timeout=60  # Timeout after 60 seconds
            )
            print(f"Task Result: {task_result}")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 
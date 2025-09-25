import asyncio
from fetcher.fetch import AsyncHTTPFetcher
from fetcher.dataclass import HTTPRequest


async def http_fetcher_example():
    requests = [
        HTTPRequest("https://httpbin.org/delay/1"),
        HTTPRequest("https://httpbin.org/status/200"),
        HTTPRequest("https://httpbin.org/json"),
        HTTPRequest("https://httpbin.org/status/404"),  # Will fail
        HTTPRequest("https://httpbin.org/status/500"),  # Will retry
    ]

    async with AsyncHTTPFetcher(max_concurrent=3) as fetcher:
        try:
            results = await fetcher.fetch_all(requests)
            print(f"\nSuccessful responses: {len(results)}")
            for result in results:
                print(
                    f"- {result.url}: {result.status_code} ({result.response_time:.2f}s)"
                )

            print(f"\nStats: {fetcher.get_stats()}")

        except Exception as e:
            print(f"Fetcher failed: {e}")


if __name__ == "__main__":
    asyncio.run(http_fetcher_example())

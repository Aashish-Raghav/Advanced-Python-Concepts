import asyncio
import aiohttp


async def fetch_single(
    url: str, session: aiohttp.ClientSession, timeout: float = 5, max_retries: int = 1
):
    """
    Fetch a single URL with retries, proper exception handling, and timeout.
    """
    for attempt in range(1, max_retries + 2):  # +1 for first try
        try:
            async with session.get(
                url, timeout=aiohttp.ClientTimeout(total=timeout)
            ) as response:
                # Raise for HTTP 4xx or 5xx
                response.raise_for_status()

                # Parse JSON if content type is JSON, else fallback to text
                if "application/json" in response.content_type:
                    data = await response.json()
                else:
                    data = await response.text()

                print(f"Success: {url} -> {data}")
                return data

        except asyncio.TimeoutError:
            print(f"Timeout while fetching {url}")
        except aiohttp.ClientConnectionError as e:
            print(f"Connection error while fetching {url}: {e}")
        except aiohttp.ClientResponseError as e:
            if 500 <= e.status < 600:
                print(f"Server error {e.status} for {url}")
            else:
                print(f"Client error {e.status} for {url} (no retry)")
                raise
        except aiohttp.ClientError as e:
            print(f"HTTP client error while fetching {url}: {e}")
        except Exception as e:
            print(f"Unexpected error while fetching {url}: {e}")
            raise

        # Retry logic
        if attempt <= max_retries:
            delay = min(2 ** (attempt - 1), 30)
            print(f"Retrying {url} in {delay}s (attempt {attempt})")
            await asyncio.sleep(delay)
        else:
            print(f"Failed {url} after {attempt} attempts")
            raise aiohttp.ClientError(f"Failed to fetch {url}")


# Example usage
async def main():
    urls = [
        "https://httpbin.org/json",  # valid
        "https://httpbin.org/status/500",  # server error
        "https://httpbin.org/status/404",  # client error
        "https://httpbin.org/delay/5",  # may timeout
    ]
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(fetch_single(url, session)) for url in urls]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        for i, resp in enumerate(responses, 1):
            if isinstance(resp, Exception):
                print(f"Request {i} failed: {resp}")
            else:
                print(f"Request {i} succeeded: {resp}")


if __name__ == "__main__":
    asyncio.run(main())

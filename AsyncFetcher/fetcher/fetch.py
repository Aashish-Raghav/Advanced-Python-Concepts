import asyncio
import time
from typing import Optional
import aiohttp
from .logging import logger
from .dataclass import HTTPRequest, HTTPResponse


class AsyncHTTPFetcher:

    def __init__(self, max_concurrent: int = 10, default_timeout: float = 10.09):
        self.max_concurrent = max_concurrent
        self.default_timeout = default_timeout
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.session: Optional[aiohttp.ClientSession] = None
        self.stats: dict[str, int] = {
            "request_made": 0,
            "request_failed": 0,
            "request_succeeded": 0,
            "total_retries": 0,
        }

    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.default_timeout),
            connector=aiohttp.TCPConnector(limit=100),
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()

        # Wait a bit for underlying connections to close
        await asyncio.sleep(0.1)

    async def fetch_single(self, request: HTTPRequest) -> HTTPResponse:
        """Fetch a single HTTP request with retries and timeout."""
        async with self.semaphore:
            for attempt in range(request.max_retries + 1):
                start = time.time()
                try:
                    self.stats["request_made"] += 1
                    async with self.session.request(
                        method=request.method,
                        url=request.url,
                        headers=request.headers,
                        json=request.data if request.method != "GET" else None,
                        timeout=aiohttp.ClientTimeout(total=request.timeout),
                    ) as response:
                        try:
                            if "application/json" in response.content_type:
                                data = await response.json()
                            else:
                                data = await response.text()
                        except Exception as e:
                            data = f"Error reading data {e}"

                    response_time = time.time() - start

                    result = HTTPResponse(
                        url=request.url,
                        status_code=response.status,
                        headers=dict(response.headers),
                        body=data,
                        response_time=response_time,
                        attempt=attempt + 1,
                    )

                    if response.status >= 400:
                        raise aiohttp.ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status,
                            message=f"HTTP Error {response.status}",
                            headers=response.headers,
                        )
                    self.stats["request_succeeded"] += 1
                    logger.info(
                        f"Success {request.url} - {response.status} ({response_time:.2f}s)"
                    )
                    return result

                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    response_time = time.time() - start

                    if attempt == request.max_retries:
                        self.stats["request_failed"] += 1
                        logger.error(
                            f"Failed {request.url} after {attempt+1} attempts: {e}"
                        )
                        raise

                    delay = min(2**attempt, 30)
                    self.stats["total_retries"] += 1
                    logger.warning(
                        f"Warning {request.url} - Attempt {attempt + 1} failed ({e}), "
                        f"retrying in {delay}s"
                    )

                    await asyncio.sleep(delay)

                except Exception as e:
                    logger.exception(f"Unexpected error for {request.url}: {e}")
                    raise

    async def fetch_all(self, requests: list[HTTPRequest]) -> list[HTTPResponse]:
        """Fetch multiple HTTP requests concurrently."""
        tasks = [asyncio.create_task(self.fetch_single(req)) for req in requests]
        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            succeed = []
            failed = []

            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    failed.append((requests[i], result))
                else:
                    succeed.append(result)

            if failed:
                logger.warning(f"Failed to fetch {len(failed)} URLs")

            return succeed
        except Exception as e:
            for task in tasks:
                if not task.done():
                    task.cancel()

            await asyncio.gather(*tasks, return_exceptions=True)
            raise

    def get_stats(self) -> dict[str, int]:
        """Get current statistics."""
        return self.stats.copy()

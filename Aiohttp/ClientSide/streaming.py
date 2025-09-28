import asyncio
import aiohttp
import aiofiles
import time


class APIClient:
    def __init__(self):
        self.session = None

    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=None)  # remove total timeout for testing
        connector = aiohttp.TCPConnector(limit=10, limit_per_host=5)
        self.session = aiohttp.ClientSession(timeout=timeout, connector=connector)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def streaming_blocking(self, url: str, file_suffix: int):
        try:
            async with self.session.get(url) as response:
                response.raise_for_status()
                with open(f"blocking_{file_suffix}.bin", "wb") as f:
                    async for chunk in response.content.iter_chunked(8192):
                        f.write(chunk)  # blocking
            print(f"[Blocking] Downloaded {url}")
        except Exception as e:
            print(f"[Blocking] Failed {url}: {e}")

    async def streaming_non_blocking(self, url: str, file_suffix: int):
        try:
            async with self.session.get(url) as response:
                response.raise_for_status()
                async with aiofiles.open(f"non_blocking_{file_suffix}.bin", "wb") as f:
                    async for chunk in response.content.iter_chunked(8192):
                        await f.write(chunk)
            print(f"[Non-blocking] Downloaded {url}")
        except Exception as e:
            print(f"[Non-blocking] Failed {url}: {e}")


async def main():
    urls = [
        "https://httpbin.org/bytes/1024",
        "https://httpbin.org/bytes/9000",
        "https://httpbin.org/bytes/19000",
    ]

    async with APIClient() as client:
        # Blocking
        # start = time.time()
        # tasks = [asyncio.create_task(client.streaming_blocking(url, i)) for i, url in enumerate(urls)]
        # await asyncio.gather(*tasks)
        # print(f"Blocking total time: {time.time() - start:.2f}s\n")

        # Non-blocking
        start = time.time()
        tasks = [
            asyncio.create_task(client.streaming_non_blocking(url, i))
            for i, url in enumerate(urls)
        ]
        await asyncio.gather(*tasks)
        print(f"Non-blocking total time: {time.time() - start:.2f}s\n")


if __name__ == "__main__":
    asyncio.run(main())
"""
[Blocking] Downloaded https://httpbin.org/bytes/9000
[Blocking] Downloaded https://httpbin.org/bytes/19000
[Blocking] Downloaded https://httpbin.org/bytes/1024
Blocking total time: 178.80s

[Non-blocking] Downloaded https://httpbin.org/bytes/1024
[Non-blocking] Downloaded https://httpbin.org/bytes/9000
[Non-blocking] Downloaded https://httpbin.org/bytes/19000
Non-blocking total time: 114.86s

"""

import asyncio
import aiohttp


async def bad_example():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://httpbin.org/get") as response:
            return await response.json()


class APIClient:
    def __init__(self):
        self.session = None

    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=30)
        connector = aiohttp.TCPConnector(
            limit=100,
            limit_per_host=30,
            keepalive_timeout=60,
            enable_cleanup_closed=True,
        )

        self.session = aiohttp.ClientSession(timeout=timeout, connector=connector)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def fetch_get(self, url: str):
        async with self.session.get(url) as resp:
            return await resp.json()

    async def fetch_post(self, url: str, payload: dict):
        async with self.session.post(url, json=payload) as resp:
            return await resp.json()


async def main():
    async with APIClient() as client:

        tasks = [
            client.fetch_get("https://httpbin.org/get"),
            client.fetch_get("https://httpbin.org/user-agent"),
            client.fetch_post("https://httpbin.org/post", {"data": "test"}),
        ]

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        for i, resp in enumerate(responses, 1):
            if isinstance(resp, Exception):
                print(f"Request {i} failed: {resp}")
            else:
                print(f"Request {i} succeeded: {resp}")


if __name__ == "__main__":
    asyncio.run(main())

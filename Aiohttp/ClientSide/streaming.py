import asyncio
import os
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

    async def file_sender(self, file_path):
        async with aiofiles.open(file_path, "rb") as f:
            chunk = await f.read(8192)
            while chunk:
                yield chunk
                chunk = await f.read(8192)

    async def upload_non_blocking(self, file_path, url, no):
        try:
            file_size = os.path.getsize(file_path)
            uploaded = 0

            async def non_blocking():
                nonlocal uploaded
                async for chunk in self.file_sender(file_path):
                    uploaded += len(chunk)
                    progress = (uploaded / file_size) * 100
                    # print(f"Non Blocking Upload progress for task {no}: {progress:.1f}%")
                    yield chunk

            async with self.session.post(
                url, data=non_blocking(), chunked=True
            ) as response:
                return await response.json()

        except Exception as e:
            print(f"[Non Blocking Upload] Failed {file_path}: {e}")

    async def upload_blocking(self, file_path, url, no):
        try:
            file_size = os.path.getsize(file_path)
            uploaded = 0

            async def blocking_sender():
                nonlocal uploaded
                with open(file_path, "rb") as f:
                    chunk = f.read(8192)  # blocking read
                    while chunk:
                        yield chunk
                        uploaded += len(chunk)
                        progress = (uploaded / file_size) * 100
                        # print(f"Blocking Upload progress for task {no}: {progress:.1f}%")
                        chunk = f.read(8192)

            async with self.session.post(
                url, data=blocking_sender(), chunked=True
            ) as response:
                return await response.json()
        except Exception as e:
            print(f"[Blocking Upload] Failed {file_path}: {e}")


async def main():
    urls = [
        "https://httpbin.org/bytes/1024",
        "https://httpbin.org/bytes/9000",
        "https://httpbin.org/bytes/19000",
    ]

    async with APIClient() as client:
        # Blocking
        start = time.time()
        tasks = [
            asyncio.create_task(client.streaming_blocking(url, i))
            for i, url in enumerate(urls)
        ]
        await asyncio.gather(*tasks)
        print(f"Blocking total time: {time.time() - start:.2f}s\n")

        # Non-blocking
        start = time.time()
        tasks = [
            asyncio.create_task(client.streaming_non_blocking(url, i))
            for i, url in enumerate(urls)
        ]
        await asyncio.gather(*tasks)
        print(f"Non-blocking total time: {time.time() - start:.2f}s\n")

    # ===========
    # Uploading
    # ===========
    upload_file = "E:\\Advanced Python Concepts\\Aiohttp\\ClientSide\\test_file_05MB.bin"  # 0.5 MB file
    async with APIClient() as client:
        # Non-blocking upload
        start = time.time()
        tasks = [
            asyncio.create_task(
                client.upload_non_blocking(
                    upload_file, "http://localhost:8080/upload", i
                )
            )
            for i in range(100)
        ]
        await asyncio.gather(*tasks)
        print(f"Non-blocking upload total time: {time.time() - start:.2f}s\n")

    async with APIClient() as client:
        # Blocking upload
        start = time.time()
        tasks = [
            asyncio.create_task(
                client.upload_blocking(upload_file, "http://localhost:8080/upload", i)
            )
            for i in range(100)
        ]
        await asyncio.gather(*tasks)
        print(f"Blocking upload total time: {time.time() - start:.2f}s\n")


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


# Simulate upload with 100 users , each with 50 KB data,
network latency of 0.001 sec (1 ms) for each chunk

Non-blocking upload total time: 13.13s
Blocking upload total time: 18.37s

"""

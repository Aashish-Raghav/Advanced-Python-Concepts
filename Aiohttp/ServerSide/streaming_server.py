# server.py
import asyncio
from aiohttp import web
import os


async def handle_download(request):
    size = int(request.query.get("size", 1024))

    async def file_gen():
        sent = 0
        chunk_size = 8192
        while sent < size:
            remaining = size - sent
            yield os.urandom(min(chunk_size, remaining))
            sent += chunk_size
            await asyncio.sleep(0.001)  # Simulate real world

    return web.Response(body=file_gen())


async def handle_upload(request):
    uploaded = 0
    reader = request.content
    async for chunk in reader.iter_chunked(8192):
        uploaded += len(chunk)
        await asyncio.sleep(0.001)
        # optionally write to disk here
    return web.json_response({"received_bytes": uploaded})


# async def handle_upload(request):
#     uploaded = await request.read()
#     await asyncio.sleep(0.1) # simulate traffic
#     return web.json_response({"received_bytes": len(uploaded)})

app = web.Application()
app.add_routes(
    [web.get("/download", handle_download), web.post("/upload", handle_upload)]
)

if __name__ == "__main__":
    web.run_app(app, port=8080)

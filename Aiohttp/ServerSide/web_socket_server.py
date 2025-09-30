import asyncio
from aiohttp import web

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            print(f"Server received: {msg.data}")
            await ws.send_str(f"Echo: {msg.data}")
        elif msg.type == web.WSMsgType.ERROR:
            print(f"WebSocket connection closed with exception {ws.exception()}")

    print("WebSocket connection closed")
    return ws

app = web.Application()
app.router.add_get("/ws", websocket_handler)

if __name__ == "__main__":
    web.run_app(app, port=8080)

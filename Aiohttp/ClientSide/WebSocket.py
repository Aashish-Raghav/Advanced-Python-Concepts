import json
import aiohttp
import asyncio


class WebSocketClient:
    def __init__(self, url: str, max_reconnect_attempts: int = 5):
        self.url = url
        self.session = None
        self.ws = None
        self.reconnect_attempts = 0
        self.max_reconnet_attempts = max_reconnect_attempts

    async def connect(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()

        try:
            self.ws = await self.session.ws_connect(self.url)
            self.reconnect_attempts = 0
            print("WebSocket connected")
            return True
        except aiohttp.ClientConnectorError as e:
            print(f"Connection failed: {e}")
        except aiohttp.WSServerHandshakeError as e:
            print(f"Handshake failed: {e}")
        except asyncio.TimeoutError:
            print("Connection timed out")
        except aiohttp.ClientError as e:
            print(f"Generic aiohttp client error: {e}")
        except Exception as e:
            # fallback – log unexpected stuff
            print(f"⚠️ Unexpected error: {e}")

        return False

    async def send_message(self, message):
        if self.ws and not self.ws.closed:
            await self.ws.send_str(json.dumps(message))

    async def reconnect(self):
        if self.reconnect_attempts >= self.max_reconnet_attempts:
            print("Max connection attempts reached.")
            return False

        self.reconnect_attempts += 1
        wait_time = (2**self.reconnect_attempts, 60)
        print(f"Reconnecting in {wait_time}.....")
        await asyncio.sleep(wait_time)

        return self.connect()

    async def listen(self):
        while True:
            if not self.ws or self.ws.closed:
                if not await self.reconnect():
                    break

            try:
                async for msg in self.ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        print(f"msg from server: {msg}")
                        yield str(msg.data)
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        print(f"Web Socket Error: {self.ws.exception()}")
                        break
                    elif msg.type == aiohttp.WSMsgType.CLOSED:
                        print("WebSocket Closed")
                        break

            except Exception as e:
                print(f"Error in listen loop : {e}")
                await asyncio.sleep(1)

    async def close(self):
        if self.ws:
            await self.ws.close()
        if self.session:
            await self.session.close()


async def run_client():
    url = "http://localhost:8080/ws"
    client = WebSocketClient(url)
    connected = await client.connect()

    if not connected:
        return

    # send text message
    await client.send_message({"type" : "Hello", "data" : "World"})

    # Listen to response:
    async for msg in client.listen():
        print("Client got : ", msg)


if __name__ == "__main__":
    asyncio.run(run_client())

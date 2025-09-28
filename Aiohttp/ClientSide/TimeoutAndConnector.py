from sqlite3 import Time
import aiohttp
from aiohttp import ClientTimeout, TCPConnector
import asyncio


async def timeout_examples():
    # Comprehensive timeout configuration
    timeout = ClientTimeout(
        total=30,  # Total timeout for the operation
        connect=5,  # Timeout for connection establishment
        sock_read=10,  # Timeout for reading from socket
        sock_connect=5,  # Timeout for socket connection
    )

    # Advanced connector configuration
    connector = TCPConnector(
        limit=100,  # Total connection pool size
        limit_per_host=30,  # Max connections per host
        keepalive_timeout=60,  # Keep connections alive for 60s
        enable_cleanup_closed=True,  # Clean up closed connections
        use_dns_cache=True,  # Cache DNS lookups
        ttl_dns_cache=300,  # DNS cache TTL in seconds
        family=0,  # 0 for both IPv4/IPv6
        ssl=False,  # SSL context or False
        local_addr=None,  # Local address to bind
        resolver=None,  # Custom resolver
    )

    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
        try:
            async with session.get("https://httpbin.org/status/404") as resp:
                resp.raise_for_status()  # Raises ClientResponseError
        except aiohttp.ClientResponseError as e:
            print(f"HTTP Error: {e.status}")


asyncio.run(timeout_examples())

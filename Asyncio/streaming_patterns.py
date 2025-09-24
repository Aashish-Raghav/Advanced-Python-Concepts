import asyncio
import random
import time
from typing import Any, AsyncGenerator


class StreamingPatterns:

    async def async_iterator(self):
        """
        | Feature                  | Async Iterator                       | `asyncio.as_completed`                          |
        | ------------------------ | ------------------------------------ | ----------------------------------------------- |
        | Order                    | Preserves sequence                   | Completion order (may be different)             |
        | Lazy generation          | ✅ Each next item generated on demand | ❌ All awaitables start immediately              |
        | Stateful / complex logic | ✅ Can maintain state inside iterator | ❌ Must pre-create all awaitables                |
        | Suitable for             | Streaming, lazy data                 | Parallel tasks, handling results as they finish |

        """

        class AsyncRange:
            def __init__(self, start: int, stop: int, delay: float = 0.2):
                self.start = start
                self.stop = stop
                self.delay = delay

            def __aiter__(self):
                return self

            async def __anext__(self):
                if self.start >= self.stop:
                    raise StopAsyncIteration

                await asyncio.sleep(self.delay)
                current = self.start
                self.start += 1
                return current

        async for i in AsyncRange(1, 5, 1):
            print(f"Got Value {i}")

    async def async_generator(self):

        async def fetch_data_stream(count: int) -> AsyncGenerator[dict[str, Any], None]:
            for i in range(count):
                await asyncio.sleep(0.2)  # simulate network delay
                data = {
                    "id": i,
                    "timestamp": time.time(),
                    "value": random.randint(1, 100),
                }
                yield data

        # Two ways to consume the async generator
        count = 2

        # 1. Using async for
        async for data in fetch_data_stream(count):
            print(f"Fetched : {data }")

        # 2. Using __anext__()
        g = fetch_data_stream(count)
        for _ in range(count):
            data = await g.__anext__()
            print(f"Fetched : {data }")

        # 3. using g.asend()
        g = fetch_data_stream(count)
        for _ in range(count):
            data = await g.asend(None)
            print(f"Fetched : {data }")

        # 4. with comprehension
        g = fetch_data_stream(count)
        data = [item async for item in g]
        print(f"Fetched : {data }")


if __name__ == "__main__":
    # asyncio.run(StreamingPatterns().async_iterator())
    asyncio.run(StreamingPatterns().async_generator())

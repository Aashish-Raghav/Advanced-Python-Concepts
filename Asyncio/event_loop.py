import asyncio


async def simple_coroutine():
    """A simple coroutine that simulates an I/O-bound task."""
    print("Coroutine started")
    await asyncio.sleep(1)  # Simulate an I/O operation with sleep
    print("Coroutine finished")
    return "Result from coroutine"


async def demo_event_loop():
    """Demonstrates different ways to run the asyncio event loop."""
    print("Running coroutine directly")
    result = await simple_coroutine()
    print(f"Result : {result}")

    print("\nRunning with asyncio.create_task()")
    task = asyncio.create_task(simple_coroutine())
    result = await task
    print(f"Task Result : {result}")

    print("\nRunning multiple task simultaneously")
    tasks = [asyncio.create_task(simple_coroutine()) for _ in range(3)]
    results = await asyncio.gather(*tasks)
    print(f"Results : {results}")


if __name__ == "__main__":
    asyncio.run(demo_event_loop())

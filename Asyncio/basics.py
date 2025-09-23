import asyncio

# Coroutine
async def couroutine_example():
    print("Coroutine started")
    await asyncio.sleep(1)
    print("Coroutine ended")


# Task
async def task_example():
    print("Task Created")
    task = asyncio.create_task(couroutine_example())
    await task
    print("Task ended")

# Future
async def future_example():
    loop = asyncio.get_running_loop()
    future = loop.create_future()

    def set_future():
        future.set_result("Future Result Set")

    loop.call_later(1, set_future)
    print("Waiting for future...")
    result = await future
    print(result)

async def main():
    await couroutine_example()
    await task_example()
    await future_example()

if __name__ == "__main__":
    asyncio.run(main())
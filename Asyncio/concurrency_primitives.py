import asyncio


class ConcurrencyPrimitive:
    """
    Queue: message passing
    Lock: ensure mutual exclusion
    Event: signal/wait
    Semaphore: limit concurrency
    """

    async def queue_demo(self):
        """Demonstrates the use of asyncio.Queue for producer-consumer pattern."""
        queue = asyncio.Queue(maxsize=3)

        async def producer(name: str, queue: asyncio.Queue):
            for i in range(5):
                item = f"item-{i}"
                await queue.put(item)
                print(f"Producer {name} put : {item}")
                await asyncio.sleep(0.1)  # Simulate time taken to produce an item

        async def consumer(name: str, queue: asyncio.Queue):
            while True:
                try:
                    item = await asyncio.wait_for(queue.get(), timeout=1.0)
                    print(f"Consumer {name} got : {item}")
                    queue.task_done()
                    await asyncio.sleep(0.2)  # Simulate time taken to process an item
                except asyncio.TimeoutError:
                    print(f"Consumer {name} timed out.")
                    break

        tasks = [
            asyncio.create_task(consumer("C1", queue)),
            asyncio.create_task(consumer("C2", queue)),
            asyncio.create_task(producer("P1", queue)),
        ]

        await asyncio.gather(*tasks, return_exceptions=True)

    async def lock_demo(self):
        """Demostrates asyncio.Lock for mutual exclusion."""
        shared_resource = 0
        lock = asyncio.Lock()

        async def Worker(name: str, lock: asyncio.Lock):
            nonlocal shared_resource
            for _ in range(5):
                async with lock:
                    current_value = shared_resource
                    await asyncio.sleep(0.1)  # Simulate some processing time
                    shared_resource = current_value + 1
                    print(
                        f"Worker {name} incremented shared_resource to {shared_resource}"
                    )

        tasks = [asyncio.create_task(Worker(f"W{i}", lock)) for i in range(4)]
        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"Final value of shared_resource: {shared_resource}")

    async def event_demo(self):
        """
        | Scenario                                      | Behavior                                                                    |
        | --------------------------------------------- | --------------------------------------------------------------------------- |
        | Multiple waiters, one setter                  | All waiters unblock at once                                                 |
        | Multiple setters                              | First `.set()` releases everyone; later `.set()` calls have no extra effect |
        | Waiter starts **after** event was already set | Waiter continues immediately (no wait)                                      |
        | To make waiters block again                   | You must call `.clear()`                                                    |

        Demonstrates asyncio.Event for signaling between coroutines.
        """
        event = asyncio.Event()

        async def waiter(name: str, event: asyncio.Event):
            print(f"Waiter {name} waiting for event.")
            await event.wait()
            print(f"Waiter {name} recieved event signal.")

        async def setter(name: str, event: asyncio.Event):
            print(f"Setter {name} setting event after 1 second.")
            await asyncio.sleep(1)
            event.set()
            print(f"Setter {name} set the event.")

        tasks = [
            asyncio.create_task(waiter("W1", event)),
            asyncio.create_task(waiter("W2", event)),
            asyncio.create_task(setter("S1", event)),
        ]

        await asyncio.gather(*tasks, return_exceptions=True)

    async def semaphore_demo(self):
        """Demonstrates asyncio.Semaphore to limit concurrency."""
        semaphore = asyncio.Semaphore(5)

        async def Worker(name: str, semaphore: asyncio.Semaphore):
            async with semaphore:
                print(f"Worker {name} acquired semaphore.")
                await asyncio.sleep(1)  # Simulate some processing time
                print(f"Worker {name} releasing semaphore.")

        tasks = [asyncio.create_task(Worker(f"W{i}", semaphore)) for i in range(10)]

        await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    # asyncio.run(ConcurrencyPrimitive().queue_demo())
    # asyncio.run(ConcurrencyPrimitive().lock_demo())
    # asyncio.run(ConcurrencyPrimitive().event_demo())
    asyncio.run(ConcurrencyPrimitive().semaphore_demo())

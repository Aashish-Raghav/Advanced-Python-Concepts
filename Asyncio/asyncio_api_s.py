import asyncio
import enum
import re
from unittest import async_case


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


class CoordinationPatterns:
    """
    1. as_completed
    2. gather
    3. wait, wait_for
    4. shield
    5. timeout
    """

    async def slow_task(self, name: str, delay : float):
        await asyncio.sleep(delay)
        return f"Task {name} completer after {delay}"

    
    
    async def demo_as_completed(self):
        """Demonstrates asyncio.as_completed to process tasks as they complete."""
        tasks = [
            asyncio.create_task(self.slow_task(f"T{i}", delay))
            for i, delay in enumerate([3, 1, 2, 5])
        ]

        for completed_task in asyncio.as_completed(tasks):
            print(f"Waiting for next completed task {completed_task}...")
            result = await completed_task
            # Note: completed_task is a coroutine, not a finished Task object.
            # You cannot use .result() directly here.
            # Always use 'await' to retrieve the result:
            # - If the task is already done, 'await' returns immediately.
            # - If the task is pending, 'await' suspends until completion.
            print(f"Completed: {result}")
    
    async def demo_gather(self):
        """Demonstrates asyncio.gather to run tasks concurrently and collect results."""
        tasks = [
            asyncio.create_task(self.slow_task(f"T{i}", delay))
            for i, delay in enumerate([3, 1, 2, 5])
        ]

        results = await asyncio.gather(*tasks)
        print("All tasks completed. Results:")
        for result in results:
            print(result)

    async def demo_wait(self):
        """Demonstrates asyncio.wait to wait for tasks with different conditions"""
        tasks = [
            asyncio.create_task(self.slow_task(f"T{i}", delay))
            for i, delay in enumerate([3, 1, 2, 5])
        ]

        # Wait until the first task completes
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        print(f"First completed : {len(done)} tasks")
        print(f"Still pending : {len(pending)} tasks")

        # max timeout after first task is 2 seconds
        try:
            result = await asyncio.wait_for(self.slow_task("T0", 3), timeout=2)
            print(f"Completed within timeout: {result}")
        except asyncio.TimeoutError:
            print(f"Task Timed out")

    async def demo_shield(self):
        """
        | Operation           | Effect                                                                                  |
        | ------------------- | --------------------------------------------------------------------------------------- |
        | `shielded.cancel()` | Cancels only the shield wrapper; underlying task keeps running                          |
        | `task.cancel()`     | Cancels the underlying task, shield cannot prevent cancellation                         |

        `asyncio.shield` ensures a wrapped task is not cancelled by its parent, but direct cancellation of the task still works.
        If the shield is cancelled, you can't await its result (raises CancelledError), but the task continues in the background.

        Use case: critical tasks that must finish even if parent coroutine is cancelled, 
        e.g., saving logs, committing DB transactions, finishing long I/O tasks
        """
        async def important_task():
            print("Important task started")
            await asyncio.sleep(3)
            print("Important task completed")
            return "Important Result"
        
        try:
            task = asyncio.create_task(important_task())
            shielded = asyncio.shield(task)

            # simulate cancellation after 1 second
            await asyncio.sleep(1)
            shielded.cancel() # this will not cancel the shielded task

            result = await shielded
            print(f"Shielded task result: {result}")
        except asyncio.CancelledError:
            print("Shielded task was cancelled")

if __name__ == "__main__":
    # asyncio.run(demo_event_loop())
    # asyncio.run(ConcurrencyPrimitive().queue_demo())
    # asyncio.run(ConcurrencyPrimitive().lock_demo())
    # asyncio.run(ConcurrencyPrimitive().event_demo())
    # asyncio.run(ConcurrencyPrimitive().semaphore_demo())
    # asyncio.run(CoordinationPatterns().demo_as_completed())
    # asyncio.run(CoordinationPatterns().demo_gather())
    # asyncio.run(CoordinationPatterns().demo_wait())
    asyncio.run(CoordinationPatterns().demo_shield())
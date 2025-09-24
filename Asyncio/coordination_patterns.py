import asyncio


class CoordinationPatterns:
    """
    1. as_completed
    2. gather
    3. wait, wait_for
    4. shield
    5. timeout
    """

    async def slow_task(self, name: str, delay: float):
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
            shielded.cancel()  # this will not cancel the shielded task

            result = await shielded
            print(f"Shielded task result: {result}")
        except asyncio.CancelledError:
            print("Shielded task was cancelled")


if __name__ == "__main__":
    # asyncio.run(CoordinationPatterns().demo_as_completed())
    # asyncio.run(CoordinationPatterns().demo_gather())
    # asyncio.run(CoordinationPatterns().demo_wait())
    asyncio.run(CoordinationPatterns().demo_shield())

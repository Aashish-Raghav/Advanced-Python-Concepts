import asyncio


class CancellationAndCleanup:
    """
    Event = cooperative shutdown signal.
    task.cancel() = forced, abrupt cancellation.
    Best practice:
        Signal workers to stop using an event
        Give them time to exit gracefully
        Cancel only the stragglers

    Demostrates proper cancellation and cleanup in asyncio.
    """

    async def cancellation_basics(self):
        "Basic Cancellation Example"

        async def cancellable_task(name: str):
            try:
                print(f"Task {name} started")
                await asyncio.sleep(5)  # Simulate a long-running operation
                print(f"Task {name} completed")
                return f"Result from {name}"
            except asyncio.CancelledError:
                print(f"Task {name} was cancelled")
                await asyncio.sleep(1)  # Simulate cleanup work
                print(f"Task {name} cleanup done")
                raise  # Re-raise to propagate cancellation

        task = asyncio.create_task(cancellable_task("A"))
        await asyncio.sleep(1)  # Let the task run for a bit
        task.cancel()  # Request cancellation
        try:
            await task
        except asyncio.CancelledError:
            print("Caught task cancellation")

    async def graceful_shutdown(self):
        """Graceful Shutdown Example"""

        shutdown_event = asyncio.Event()

        async def Worker(name: str):
            try:
                while not shutdown_event.is_set():
                    print(f"Worker {name} is working...")
                    await asyncio.sleep(1)  # Simulate work
            except asyncio.CancelledError:
                print(f"Worker {name} received cancellation")
                # Graceful cleanup
                await asyncio.sleep(0.2)
                print(f"Worker {name} cleanup done")
                raise

        tasks = [asyncio.create_task(Worker(f"W{i}")) for i in range(4)]

        await asyncio.sleep(2)  # Let workers run for a bit
        shutdown_event.set()  # Signal shutdown

        # give time to shutdown gracefully
        await asyncio.sleep(1.1)

        for task in tasks:
            if not task.done():
                task.cancel()

        # wait for all task to complete or cancel
        await asyncio.gather(*tasks, return_exceptions=True)
        print("All workers have been shut down gracefully.")


if __name__ == "__main__":
    # asyncio.run(CancellationAndCleanup().cancellation_basics())
    asyncio.run(CancellationAndCleanup().graceful_shutdown())

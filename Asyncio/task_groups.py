import asyncio
from tkinter import W


async def Worker(name: str, fail: bool = False):
    print(f"Worker {name} starting")
    await asyncio.sleep(1)
    if fail:
        raise ValueError(f"Worker {name} failed")
    print(f"Worker {name} finished")
    return f"Result from {name}"


async def task_group_basic():
    try:
        async with asyncio.TaskGroup() as tg_success:
            t1 = tg_success.create_task(Worker("A"))
            t2 = tg_success.create_task(Worker("B"))
            t3 = tg_success.create_task(Worker("C"))

        print(
            "All workers completed\nResults:"
            f"{t1.result()}, {t2.result()}, {t3.result()}"
        )

        async with asyncio.TaskGroup() as tg_fail:
            t1 = tg_fail.create_task(Worker("D", fail=True))
            t2 = tg_fail.create_task(Worker("E", fail=True))
            t3 = tg_fail.create_task(Worker("F"))

        print("All workers completed\nResults:" f"{await t1}, {await t2}, {await t3}")

    except* Exception as e:
        print(f"Some workers failed: {e.exceptions}")


async def main():

    task1 = asyncio.create_task(Worker("A"))
    task2 = asyncio.create_task(Worker("B", fail=True))
    task3 = asyncio.create_task(Worker("C"))

    # **********************************************
    # return_exceptions=True allows to capture errors without cancelling all tasks
    # **********************************************

    results = await asyncio.gather(task1, task2, task3, return_exceptions=True)
    print("Results:", results)


if __name__ == "__main__":
    # asyncio.run(task_group_basic())
    asyncio.run(main())

"""
| Feature            | `asyncio.gather`                                    | `asyncio.TaskGroup`                                        |
| ------------------ | --------------------------------------------------- | ---------------------------------------------------------- |
| Introduced         | Old (Python 3.5+)                                   | New (Python 3.11+)                                         |
| Exception handling | Fail-fast OR collect (via `return_exceptions=True`) | Always fail-fast, raises **ExceptionGroup**                |
| Return values      | Directly returned as list                           | You must access `.result()` or `await` on individual tasks |
| Cancellation       | Default: cancels siblings on failure                | Always cancels siblings on failure                         |
| Structured?        | No (fire-and-forget possible)                       | Yes (tasks scoped to block, cleaned up automatically)      |
| Task creation      | Via `asyncio.create_task()` or passed coros         | Via `tg.create_task()` within `async with` block           |
"""

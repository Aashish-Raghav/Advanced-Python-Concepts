# AsyncFetcher: Asynchronous HTTP Fetching Library

**AsyncFetcher** is a Python library designed for high-performance, concurrent HTTP requests using `asyncio` and `aiohttp`. It demonstrates advanced asynchronous programming patterns, resource management, error handling, and structured logging.

---

## Features

- **Async Context Management:**  
  Uses `async with` for safe resource acquisition and cleanup of HTTP sessions.
- **Concurrency Control:**  
  Limits concurrent requests with `asyncio.Semaphore` for efficient and safe parallelism.
- **Retry and Timeout Logic:**  
  Implements robust retry strategies with exponential backoff and per-request timeouts.
- **Custom Data Models:**  
  Uses dataclasses (`HTTPRequest`, `HTTPResponse`) for clear, type-safe request/response handling.
- **Structured Logging:**  
  Logs to both console and file with detailed status, warnings, and errors.
- **Error Handling:**  
  Handles HTTP errors, timeouts, and unexpected exceptions gracefully, with statistics and reporting.
- **Batch Fetching:**  
  Fetches multiple URLs concurrently and aggregates results, separating successes and failures.

---

## Project Structure

```
AsyncFetcher/
│
├── main.py                      # Example usage script
├── fetcher/
│   ├── __init__.py
│   ├── dataclass.py             # HTTPRequest and HTTPResponse dataclasses
│   ├── fetch.py                 # AsyncHTTPFetcher core logic
│   ├── logging.py               # Logging setup
│   └── __pycache__/             # Compiled Python files
└── tests/
    ├── conftest.py              # Test configuration
    ├── test_fetch.py            # Unit tests for AsyncHTTPFetcher
    └── __pycache__/             # Compiled Python test files
```

---

## Usage Example

Here’s an example of how to use the **AsyncFetcher** library:

```python
import asyncio
from fetcher.fetch import AsyncHTTPFetcher
from fetcher.dataclass import HTTPRequest

async def http_fetcher_example():
    requests = [
        HTTPRequest("https://httpbin.org/delay/1"),
        HTTPRequest("https://httpbin.org/status/200"),
        HTTPRequest("https://httpbin.org/json"),
        HTTPRequest("https://httpbin.org/status/404"),  # Will fail
        HTTPRequest("https://httpbin.org/status/500"),  # Will retry
    ]

    async with AsyncHTTPFetcher(max_concurrent=3) as fetcher:
        results = await fetcher.fetch_all(requests)
        print(f"\nSuccessful responses: {len(results)}")
        for result in results:
            print(f"- {result.url}: {result.status_code} ({result.response_time:.2f}s)")
        print(f"\nStats: {fetcher.get_stats()}")

if __name__ == '__main__':
    asyncio.run(http_fetcher_example())
```

---

## Testing

The `tests/` folder contains a comprehensive test suite for the library. It includes:

- **Unit Tests:**  
  Tests for individual components like `fetch_single` and `fetch_all`.
- **Mocking External APIs:**  
  Uses `unittest.mock` to simulate HTTP responses for testing without making real network requests.
- **Error Handling Tests:**  
  Verifies retry logic, timeout handling, and exception propagation.

### How to Run Tests

1. Install the required dependencies:
   ```bash
   pip install pytest pytest-asyncio aiohttp
   ```

2. Run the tests:
   ```bash
   pytest -v
   ```

---

## Logging

The library uses structured logging to track activity, including:

- **Console Logging:**  
  Logs high-level information and warnings to the console.
- **File Logging:**  
  Logs detailed debug information to `fetcher.log`, including retries, errors, and performance metrics.

---

## Key Components

### `HTTPRequest` (Dataclass)
Represents an HTTP request to be made.

| Attribute     | Type               | Description                              |
|---------------|--------------------|------------------------------------------|
| `url`         | `str`              | The URL to fetch.                        |
| `method`      | `str`              | HTTP method (default: `GET`).            |
| `headers`     | `Optional[dict]`   | HTTP headers.                            |
| `data`        | `Optional[dict]`   | Request body (for POST/PUT requests).    |
| `timeout`     | `float`            | Timeout for the request (default: 10s).  |
| `max_retries` | `int`              | Maximum retry attempts (default: 3).     |

---

### `HTTPResponse` (Dataclass)
Represents an HTTP response received.

| Attribute       | Type               | Description                              |
|-----------------|--------------------|------------------------------------------|
| `url`           | `str`              | The URL that was fetched.                |
| `status_code`   | `int`              | HTTP status code.                        |
| `headers`       | `dict`             | Response headers.                        |
| `body`          | `Any`              | Response body (JSON or text).            |
| `response_time` | `float`            | Time taken for the request.              |
| `attempt`       | `int`              | Number of attempts made.                 |

---

## Summary

AsyncFetcher is a practical demonstration of advanced async programming, error handling, and logging in Python.  
It’s ideal for learning about real-world concurrency, resource management, and robust HTTP client design.

Feel free to explore, modify, and experiment with the code as you deepen your understanding of Python!

---
from dataclasses import dataclass
from typing import Any, Optional
from urllib import response


@dataclass
class HTTPRequest:
    """Represents an HTTP request to be made."""

    url: str
    method: str = "GET"
    headers: Optional[dict[str, str]] = None
    data: Optional[dict[str, Any]] = None
    timeout: float = 10.0
    max_retries: int = 3


@dataclass
class HTTPResponse:
    """Represents an HTTP response received."""

    url: str
    status_code: int
    headers: dict[str, str]
    body: Any
    response_time: float
    attempt: int

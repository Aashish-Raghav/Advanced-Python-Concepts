# test_asyncio_examples.py
"""
Comprehensive unit tests for asyncio code.

Run with:
pip install pytest pytest-asyncio aiohttp
cd "..../AsyncFetcher"
pytest -v 

"""

from unittest.mock import AsyncMock, patch
import pytest
import pytest_asyncio

from fetcher.fetch import AsyncHTTPFetcher, simple_coroutine
from fetcher.dataclass import HTTPRequest, HTTPResponse


class TestBasicAsyncOperations:

    @pytest.mark.asyncio
    async def test_simple_coroutine(self):
        result = await simple_coroutine()
        assert result == "Result from simple Coroutine"


class TestAsyncFetcher:

    @pytest_asyncio.fixture
    async def http_fetcher(self):
        async with AsyncHTTPFetcher(max_concurrent=2) as fetcher:
            yield fetcher

    @pytest.mark.asyncio
    async def test_fetch_single_success(self, http_fetcher):
        # Mock response Object
        mock_content = AsyncMock()
        mock_content.status = 200
        mock_content.content_type = "application/json"
        mock_content.json = AsyncMock(return_value={"ok": True})
        mock_content.headers = {"Content-Type": "application/json"}

        mock_response = AsyncMock()
        mock_response.__aenter__.return_value = mock_content
        mock_response.__aexit__.return_value = None

        # patch aiohttp.ClientSession.request to return mock object
        with patch.object(http_fetcher.session, "request", return_value=mock_response):
            req = HTTPRequest("http://fake.url/json")
            res = await http_fetcher.fetch_single(req)

        assert isinstance(res, HTTPResponse)
        assert res.status_code == 200
        assert res.body == {"ok": True}
        assert res.url == req.url
        assert res.attempt == 1

    @pytest.mark.asyncio
    async def test_fetch_single_failure_retries(self, http_fetcher):
        mock_content = AsyncMock()
        mock_content.status = 500
        mock_content.content_type = "application/json"
        mock_content.json = AsyncMock(return_value={"error": "server"})
        mock_content.headers = {}

        mock_response = AsyncMock()
        mock_response.__aenter__.return_value = mock_content
        mock_response.__aexit__.return_value = None

        with patch.object(http_fetcher.session, "request", return_value=mock_response):
            req = HTTPRequest("http://fake.url/fail", max_retries=2)

            with pytest.raises(Exception):  # final raise after retries
                await http_fetcher.fetch_single(req)

        stats = http_fetcher.get_stats()
        assert stats["total_retries"] >= 2
        assert stats["request_failed"] >= 1

    @pytest.mark.asyncio
    async def test_fetch_all_mixed(self, http_fetcher):
        """Test fetch_all with both success and failure."""
        # Success response
        success_content = AsyncMock()
        success_content.status = 200
        success_content.content_type = "application/json"
        success_content.json = AsyncMock(return_value={"ok": True})
        success_content.headers = {}
        success_response = AsyncMock()
        success_response.__aenter__.return_value = success_content
        success_content.__aexit__.return_value = None

        # Failure response (404)
        fail_content = AsyncMock()
        fail_content.status = 404
        fail_content.content_type = "application/json"
        fail_content.json = AsyncMock(return_value={"error": "not found"})
        fail_content.headers = {}
        fail_response = AsyncMock()
        fail_response.__aenter__.return_value = fail_content
        fail_content.__aexit__.return_value = None

        # Patch: first call success, second call fail
        with patch.object(
            http_fetcher.session,
            "request",
            side_effect=[success_response, fail_response, fail_response],
        ):
            requests = [
                HTTPRequest("http://fake.url/success"),
                HTTPRequest("http://fake.url/fail", max_retries=1),
            ]
            results = await http_fetcher.fetch_all(requests)

        # One success should be returned
        assert len(results) == 1
        assert isinstance(results[0], HTTPResponse)
        assert results[0].status_code == 200

        # check stats
        stats = http_fetcher.get_stats()
        assert stats["request_failed"] == 1
        assert stats["request_succeeded"] == 1
        assert stats["request_made"] == 3
        assert stats["total_retries"] == 1

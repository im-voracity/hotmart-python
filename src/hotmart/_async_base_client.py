from __future__ import annotations

import asyncio
import time
import uuid
from typing import Any, TypeVar

import httpx

from ._async_auth import AsyncTokenManager
from ._async_rate_limit import AsyncRateLimitTracker
from ._base_client import _build_params
from ._config import BASE_URLS, ClientConfig
from ._exceptions import make_status_error
from ._logging import HotmartLogger
from ._retry import get_retry_delay, is_retryable

T = TypeVar("T")

# Re-export for async resources to import from here or _base_client
__all__ = ["BaseAsyncClient", "_build_params"]


class BaseAsyncClient:
    def __init__(self, config: ClientConfig) -> None:
        self._config = config
        self._token_manager = AsyncTokenManager(config)
        self._rate_limiter = AsyncRateLimitTracker()
        self._logger = HotmartLogger(config.log_level)
        self._http = httpx.AsyncClient(timeout=config.timeout, verify=True)

    async def __aenter__(self) -> BaseAsyncClient:
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self._http.aclose()

    def _base_url(self, api_domain: str) -> str:
        env = "sandbox" if self._config.sandbox else "prod"
        return BASE_URLS[env][api_domain]

    async def _request(
        self,
        method: str,
        path: str,
        *,
        api_domain: str = "payments",
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        cast_to: type[T] | None = None,
    ) -> T | None:
        url = f"{self._base_url(api_domain)}{path}"
        request_id = str(uuid.uuid4())

        await self._rate_limiter.wait_if_needed()
        token = await self._token_manager.get_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        self._logger.request(method=method, url=url, request_id=request_id, params=params)

        response = await self._execute_with_retry(method, url, headers, params, json, request_id)

        if response.status_code == 401:
            await self._token_manager.invalidate()
            token = await self._token_manager.get_token()
            headers["Authorization"] = f"Bearer {token}"
            response = await self._http.request(method, url, headers=headers, params=params, json=json)
            if not response.is_success:
                raise make_status_error(response)

        await self._rate_limiter.update(response.headers)

        if not response.is_success:
            raise make_status_error(response)

        if cast_to is None:
            content = response.content
            if not content or content == b"{}":
                return None
            return response.json()  # type: ignore[return-value]

        if not response.content or response.content == b"{}":
            return cast_to.model_validate({})  # type: ignore[union-attr]

        return cast_to.model_validate(response.json())  # type: ignore[union-attr]

    async def _execute_with_retry(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        params: dict[str, Any] | None,
        json: dict[str, Any] | None,
        request_id: str,
    ) -> httpx.Response:
        response: httpx.Response | None = None

        for attempt in range(self._config.max_retries + 1):
            start = time.monotonic()
            try:
                response = await self._http.request(method, url, headers=headers, params=params, json=json)
            except httpx.TransportError:
                if attempt >= self._config.max_retries:
                    raise
                delay = get_retry_delay(attempt)
                self._logger.retry(attempt=attempt + 1, max_retries=self._config.max_retries,
                                   delay=delay, status_code=0, request_id=request_id)
                await asyncio.sleep(delay)
                continue

            duration_ms = (time.monotonic() - start) * 1000
            self._logger.response(request_id=request_id, status_code=response.status_code,
                                  duration_ms=duration_ms)

            if not is_retryable(response.status_code) or attempt >= self._config.max_retries:
                return response

            delay = get_retry_delay(attempt, response)
            self._logger.retry(attempt=attempt + 1, max_retries=self._config.max_retries,
                               delay=delay, status_code=response.status_code, request_id=request_id)
            await asyncio.sleep(delay)

        return response  # type: ignore[return-value]

    async def _get(self, path: str, *, api_domain: str = "payments",
                   params: dict[str, Any] | None = None, cast_to: type[T] | None = None) -> T | None:
        return await self._request("GET", path, api_domain=api_domain, params=params, cast_to=cast_to)

    async def _post(self, path: str, *, api_domain: str = "payments",
                    json: dict[str, Any] | None = None, cast_to: type[T] | None = None) -> T | None:
        return await self._request("POST", path, api_domain=api_domain, json=json, cast_to=cast_to)

    async def _put(self, path: str, *, api_domain: str = "payments",
                   json: dict[str, Any] | None = None, cast_to: type[T] | None = None) -> T | None:
        return await self._request("PUT", path, api_domain=api_domain, json=json, cast_to=cast_to)

    async def _patch(self, path: str, *, api_domain: str = "payments",
                     json: dict[str, Any] | None = None, cast_to: type[T] | None = None) -> T | None:
        return await self._request("PATCH", path, api_domain=api_domain, json=json, cast_to=cast_to)

    async def _delete(self, path: str, *, api_domain: str = "payments",
                      cast_to: type[T] | None = None) -> T | None:
        return await self._request("DELETE", path, api_domain=api_domain, cast_to=cast_to)

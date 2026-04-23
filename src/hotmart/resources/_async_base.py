from __future__ import annotations

from typing import Any, TypeVar

from .._async_base_client import BaseAsyncClient

T = TypeVar("T")


class AsyncAPIResource:
    def __init__(self, client: BaseAsyncClient) -> None:
        self._client = client

    async def _get(self, path: str, *, api_domain: str = "payments",
                   params: dict[str, Any] | None = None, cast_to: type[T] | None = None) -> T | None:
        return await self._client._get(path, api_domain=api_domain, params=params, cast_to=cast_to)

    async def _post(self, path: str, *, api_domain: str = "payments",
                    json: dict[str, Any] | None = None, cast_to: type[T] | None = None) -> T | None:
        return await self._client._post(path, api_domain=api_domain, json=json, cast_to=cast_to)

    async def _put(self, path: str, *, api_domain: str = "payments",
                   json: dict[str, Any] | None = None, cast_to: type[T] | None = None) -> T | None:
        return await self._client._put(path, api_domain=api_domain, json=json, cast_to=cast_to)

    async def _patch(self, path: str, *, api_domain: str = "payments",
                     json: dict[str, Any] | None = None, cast_to: type[T] | None = None) -> T | None:
        return await self._client._patch(path, api_domain=api_domain, json=json, cast_to=cast_to)

    async def _delete(self, path: str, *, api_domain: str = "payments",
                      cast_to: type[T] | None = None) -> T | None:
        return await self._client._delete(path, api_domain=api_domain, cast_to=cast_to)

from __future__ import annotations
from typing import Any, TypeVar
from .._base_client import BaseSyncClient

T = TypeVar("T")


class APIResource:
    def __init__(self, client: BaseSyncClient) -> None:
        self._client = client

    def _get(self, path: str, *, api_domain: str = "payments",
             params: dict[str, Any] | None = None, cast_to: type[T] | None = None) -> T | None:
        return self._client._get(path, api_domain=api_domain, params=params, cast_to=cast_to)

    def _post(self, path: str, *, api_domain: str = "payments",
              json: dict[str, Any] | None = None, cast_to: type[T] | None = None) -> T | None:
        return self._client._post(path, api_domain=api_domain, json=json, cast_to=cast_to)

    def _put(self, path: str, *, api_domain: str = "payments",
             json: dict[str, Any] | None = None, cast_to: type[T] | None = None) -> T | None:
        return self._client._put(path, api_domain=api_domain, json=json, cast_to=cast_to)

    def _patch(self, path: str, *, api_domain: str = "payments",
               json: dict[str, Any] | None = None, cast_to: type[T] | None = None) -> T | None:
        return self._client._patch(path, api_domain=api_domain, json=json, cast_to=cast_to)

    def _delete(self, path: str, *, api_domain: str = "payments",
                cast_to: type[T] | None = None) -> T | None:
        return self._client._delete(path, api_domain=api_domain, cast_to=cast_to)

from __future__ import annotations

import time
import uuid
from typing import Any, TypeVar

import httpx

from ._auth import TokenManager
from ._config import BASE_URLS, ClientConfig
from ._exceptions import make_status_error
from ._logging import HotmartLogger
from ._rate_limit import RateLimitTracker
from ._retry import get_retry_delay, is_retryable

T = TypeVar("T")


def _build_params(local_vars: dict[str, Any]) -> dict[str, Any]:
    """Build request params from locals(), dropping None, 'self', and 'kwargs' key.

    Constrói parâmetros de requisição a partir de locals(), removendo None, 'self' e a chave 'kwargs'.
    """
    exclude = {"self", "kwargs"}
    params = {k: v for k, v in local_vars.items() if v is not None and k not in exclude}
    if "kwargs" in local_vars:
        params.update(local_vars["kwargs"])
    return params


class BaseSyncClient:
    def __init__(self, config: ClientConfig) -> None:
        self._config = config
        self._token_manager = TokenManager(config)
        self._rate_limiter = RateLimitTracker()
        self._logger = HotmartLogger(config.log_level)
        self._http = httpx.Client(timeout=config.timeout, verify=True)

    def __enter__(self) -> BaseSyncClient:
        return self

    def __exit__(self, *_: Any) -> None:
        self._http.close()

    def _base_url(self, api_domain: str) -> str:
        env = "sandbox" if self._config.sandbox else "prod"
        return BASE_URLS[env][api_domain]

    def _request(
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

        self._rate_limiter.wait_if_needed()
        token = self._token_manager.get_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        self._logger.request(method=method, url=url, request_id=request_id, params=params)

        response = self._execute_with_retry(method, url, headers, params, json, request_id)

        if response.status_code == 401:
            self._token_manager.invalidate()
            token = self._token_manager.get_token()
            headers["Authorization"] = f"Bearer {token}"
            response = self._http.request(method, url, headers=headers, params=params, json=json)
            if not response.is_success:
                raise make_status_error(response)

        self._rate_limiter.update(response.headers)

        if not response.is_success:
            raise make_status_error(response)

        if cast_to is None:
            content = response.content
            if not content or content == b"{}":
                return None
            return response.json()  # type: ignore[return-value]

        if not response.content or response.content == b"{}":
            # Hotmart bug: some endpoints (e.g. /coupon/product/{id}) return HTTP 200
            # with empty body instead of {"items": []}. Fall back to empty model.
            # Bug Hotmart: alguns endpoints retornam HTTP 200 com body vazio em vez de {"items": []}.
            return cast_to.model_validate({})  # type: ignore[union-attr]

        return cast_to.model_validate(response.json())  # type: ignore[union-attr]

    def _execute_with_retry(
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
                response = self._http.request(method, url, headers=headers, params=params, json=json)
            except httpx.TransportError:
                if attempt >= self._config.max_retries:
                    raise
                delay = get_retry_delay(attempt)
                self._logger.retry(attempt=attempt + 1, max_retries=self._config.max_retries,
                                   delay=delay, status_code=0, request_id=request_id)
                time.sleep(delay)
                continue

            duration_ms = (time.monotonic() - start) * 1000
            self._logger.response(request_id=request_id, status_code=response.status_code,
                                  duration_ms=duration_ms)

            if not is_retryable(response.status_code) or attempt >= self._config.max_retries:
                return response

            delay = get_retry_delay(attempt, response)
            self._logger.retry(attempt=attempt + 1, max_retries=self._config.max_retries,
                               delay=delay, status_code=response.status_code, request_id=request_id)
            time.sleep(delay)

        return response  # type: ignore[return-value]

    def _get(self, path: str, *, api_domain: str = "payments",
             params: dict[str, Any] | None = None, cast_to: type[T] | None = None) -> T | None:
        return self._request("GET", path, api_domain=api_domain, params=params, cast_to=cast_to)

    def _post(self, path: str, *, api_domain: str = "payments",
              json: dict[str, Any] | None = None, cast_to: type[T] | None = None) -> T | None:
        return self._request("POST", path, api_domain=api_domain, json=json, cast_to=cast_to)

    def _put(self, path: str, *, api_domain: str = "payments",
             json: dict[str, Any] | None = None, cast_to: type[T] | None = None) -> T | None:
        return self._request("PUT", path, api_domain=api_domain, json=json, cast_to=cast_to)

    def _patch(self, path: str, *, api_domain: str = "payments",
               json: dict[str, Any] | None = None, cast_to: type[T] | None = None) -> T | None:
        return self._request("PATCH", path, api_domain=api_domain, json=json, cast_to=cast_to)

    def _delete(self, path: str, *, api_domain: str = "payments",
                cast_to: type[T] | None = None) -> T | None:
        return self._request("DELETE", path, api_domain=api_domain, cast_to=cast_to)

from __future__ import annotations

import threading
import time

import httpx

from ._config import AUTH_URL, ClientConfig

_REFRESH_BUFFER = 300  # refresh 5 min before expiry


class TokenManager:
    def __init__(self, config: ClientConfig) -> None:
        self._config = config
        self._token: str | None = None
        self._expires_at: float = 0.0
        self._lock = threading.Lock()

    def get_token(self) -> str:
        if self._is_valid():
            return self._token  # type: ignore[return-value]

        with self._lock:
            if self._is_valid():
                return self._token  # type: ignore[return-value]
            return self._refresh()

    def invalidate(self) -> None:
        with self._lock:
            self._token = None
            self._expires_at = 0.0

    def _is_valid(self) -> bool:
        return self._token is not None and time.time() < self._expires_at - _REFRESH_BUFFER

    def _refresh(self) -> str:
        response = httpx.post(
            AUTH_URL,
            headers={"Authorization": self._config.basic},
            params={
                "grant_type": "client_credentials",
                "client_id": self._config.client_id,
                "client_secret": self._config.client_secret,
            },
        )
        response.raise_for_status()
        data = response.json()
        self._token = data["access_token"]
        self._expires_at = time.time() + data["expires_in"]
        return self._token  # type: ignore[return-value]

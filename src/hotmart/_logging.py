from __future__ import annotations
import logging
from typing import Any

SENSITIVE_KEYS = frozenset({"authorization", "basic", "client_secret", "access_token", "token"})


def _mask(value: str) -> str:
    if len(value) <= 8:
        return "***"
    return value[:4] + "***"


def mask_sensitive(data: dict[str, Any]) -> dict[str, Any]:
    return {
        k: _mask(str(v)) if k.lower() in SENSITIVE_KEYS else v
        for k, v in data.items()
    }


class HotmartLogger:
    def __init__(self, log_level: int = logging.WARNING) -> None:
        self._log = logging.getLogger("hotmart")
        self._log.setLevel(log_level)

    def request(self, *, method: str, url: str, request_id: str, params: dict[str, Any] | None = None) -> None:
        self._log.info("[%s] %s %s", request_id, method, url)
        if params:
            self._log.debug("[%s] params=%s", request_id, mask_sensitive(params))

    def response(self, *, request_id: str, status_code: int, duration_ms: float) -> None:
        self._log.info("[%s] %s (%.0fms)", request_id, status_code, duration_ms)

    def retry(self, *, attempt: int, max_retries: int, delay: float, status_code: int, request_id: str) -> None:
        self._log.warning(
            "[%s] retry %d/%d after %.1fs (status=%s)",
            request_id, attempt, max_retries, delay, status_code,
        )

    def auth_refresh(self, *, cached: bool) -> None:
        self._log.debug("auth: %s", "from cache" if cached else "refreshed")

    def rate_limit(self, *, remaining: int, reset_at: float) -> None:
        self._log.warning("rate limit: remaining=%d reset_in=%.0fs", remaining, reset_at)

    def error(self, *, status_code: int, error_type: str, request_id: str, message: str) -> None:
        self._log.error("[%s] %s (%s): %s", request_id, error_type, status_code, message)

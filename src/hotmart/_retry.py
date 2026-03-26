from __future__ import annotations
import random
import httpx

RETRYABLE_STATUS_CODES = frozenset({429, 500, 502, 503})
_MAX_DELAY = 30.0
_BASE_DELAY = 0.5


def is_retryable(status_code: int) -> bool:
    return status_code in RETRYABLE_STATUS_CODES


def get_retry_delay(attempt: int, response: httpx.Response | None = None) -> float:
    if response is not None and response.status_code == 429:
        reset = response.headers.get("RateLimit-Reset")
        if reset:
            return min(float(reset), _MAX_DELAY)

    jitter = random.uniform(0.0, 0.5)
    return min(_BASE_DELAY * (2 ** attempt) + jitter, _MAX_DELAY)

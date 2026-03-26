from __future__ import annotations

import threading
import time

import httpx


class RateLimitTracker:
    def __init__(self) -> None:
        self._remaining: int = 500
        self._reset_at: float = 0.0
        self._lock = threading.Lock()

    def update(self, headers: httpx.Headers) -> None:
        remaining = headers.get("RateLimit-Remaining")
        reset = headers.get("RateLimit-Reset")

        with self._lock:
            if remaining is not None:
                self._remaining = int(remaining)
            if reset is not None:
                self._reset_at = time.time() + float(reset)

    def wait_if_needed(self) -> None:
        with self._lock:
            if self._remaining > 0:
                return
            sleep_for = max(0.0, self._reset_at - time.time())

        if sleep_for > 0:
            time.sleep(sleep_for)

from __future__ import annotations

import asyncio
import time

import httpx


class AsyncRateLimitTracker:
    def __init__(self) -> None:
        self._remaining: int = 500
        self._reset_at: float = 0.0
        self._lock = asyncio.Lock()

    async def update(self, headers: httpx.Headers) -> None:
        remaining = headers.get("RateLimit-Remaining")
        reset = headers.get("RateLimit-Reset")

        async with self._lock:
            if remaining is not None:
                self._remaining = int(remaining)
            if reset is not None:
                self._reset_at = time.time() + float(reset)

    async def wait_if_needed(self) -> None:
        async with self._lock:
            if self._remaining > 0:
                return
            sleep_for = max(0.0, self._reset_at - time.time())

        if sleep_for > 0:
            await asyncio.sleep(sleep_for)

import time

import httpx

from hotmart._async_rate_limit import AsyncRateLimitTracker


async def test_update_reads_remaining_header():
    tracker = AsyncRateLimitTracker()
    await tracker.update(httpx.Headers({"RateLimit-Remaining": "42", "RateLimit-Reset": "60"}))
    assert tracker._remaining == 42


async def test_wait_if_needed_does_not_sleep_when_remaining_positive():
    tracker = AsyncRateLimitTracker()
    tracker._remaining = 10
    start = time.monotonic()
    await tracker.wait_if_needed()
    assert time.monotonic() - start < 0.1


async def test_wait_if_needed_sleeps_when_remaining_zero(monkeypatch):
    slept: list[float] = []
    async def fake_sleep(s: float) -> None:
        slept.append(s)
    monkeypatch.setattr("hotmart._async_rate_limit.asyncio.sleep", fake_sleep)
    tracker = AsyncRateLimitTracker()
    tracker._remaining = 0
    tracker._reset_at = time.time() + 2.0
    await tracker.wait_if_needed()
    assert slept and slept[0] > 0


async def test_update_ignores_missing_headers():
    tracker = AsyncRateLimitTracker()
    await tracker.update(httpx.Headers({}))
    assert tracker._remaining == 500  # default unchanged

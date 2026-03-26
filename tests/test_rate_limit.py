import time

import httpx

from hotmart._rate_limit import RateLimitTracker


def test_update_reads_remaining_header():
    tracker = RateLimitTracker()
    tracker.update(httpx.Headers({"RateLimit-Remaining": "42", "RateLimit-Reset": "60"}))
    assert tracker._remaining == 42


def test_wait_if_needed_does_not_sleep_when_remaining_positive():
    tracker = RateLimitTracker()
    tracker._remaining = 10
    start = time.monotonic()
    tracker.wait_if_needed()
    assert time.monotonic() - start < 0.1


def test_wait_if_needed_sleeps_when_remaining_zero(monkeypatch):
    slept: list[float] = []
    monkeypatch.setattr("time.sleep", lambda s: slept.append(s))
    tracker = RateLimitTracker()
    tracker._remaining = 0
    tracker._reset_at = time.time() + 2.0
    tracker.wait_if_needed()
    assert slept and slept[0] > 0


def test_update_ignores_missing_headers():
    tracker = RateLimitTracker()
    tracker.update(httpx.Headers({}))
    assert tracker._remaining == 500  # default unchanged

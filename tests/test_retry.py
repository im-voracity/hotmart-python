import httpx
from hotmart._retry import get_retry_delay, is_retryable


def test_is_retryable_for_429():
    assert is_retryable(429) is True


def test_is_retryable_for_500():
    assert is_retryable(500) is True


def test_is_not_retryable_for_400():
    assert is_retryable(400) is False


def test_is_not_retryable_for_401():
    assert is_retryable(401) is False


def test_is_not_retryable_for_403():
    assert is_retryable(403) is False


def test_delay_increases_with_attempt():
    d0 = get_retry_delay(0)
    d1 = get_retry_delay(1)
    d2 = get_retry_delay(2)
    assert d1 > d0
    assert d2 > d1


def test_delay_capped_at_30s():
    assert get_retry_delay(100) <= 30.0


def test_delay_uses_rate_limit_reset_header_for_429():
    resp = httpx.Response(429, headers={"RateLimit-Reset": "5"})
    delay = get_retry_delay(0, response=resp)
    assert delay == 5.0


def test_delay_caps_rate_limit_reset_at_30():
    resp = httpx.Response(429, headers={"RateLimit-Reset": "999"})
    assert get_retry_delay(0, response=resp) == 30.0

import httpx

from hotmart._exceptions import (
    APIStatusError,
    AuthenticationError,
    BadRequestError,
    HotmartError,
    InternalServerError,
    NotFoundError,
    RateLimitError,
    make_status_error,
)


def _resp(status: int, body: str = "{}", headers: dict | None = None) -> httpx.Response:
    return httpx.Response(status, text=body, headers=headers or {})


def test_401_raises_authentication_error():
    err = make_status_error(_resp(401))
    assert isinstance(err, AuthenticationError)


def test_403_raises_authentication_error():
    err = make_status_error(_resp(403))
    assert isinstance(err, AuthenticationError)


def test_400_raises_bad_request():
    assert isinstance(make_status_error(_resp(400)), BadRequestError)


def test_404_raises_not_found():
    assert isinstance(make_status_error(_resp(404)), NotFoundError)


def test_429_raises_rate_limit_with_retry_after():
    err = make_status_error(_resp(429, headers={"RateLimit-Reset": "10"}))
    assert isinstance(err, RateLimitError)
    assert err.retry_after == 10.0


def test_500_raises_internal_server_error():
    assert isinstance(make_status_error(_resp(500)), InternalServerError)


def test_502_raises_internal_server_error():
    assert isinstance(make_status_error(_resp(502)), InternalServerError)


def test_unknown_status_raises_api_status_error():
    err = make_status_error(_resp(418))
    assert isinstance(err, APIStatusError)
    assert err.status_code == 418


def test_authentication_error_message_is_preserved():
    err = AuthenticationError("invalid credentials")
    assert "invalid credentials" in str(err)
    assert isinstance(err, HotmartError)

import time
import threading
import httpx
import respx
import pytest
from hotmart._auth import TokenManager
from hotmart._config import ClientConfig

TOKEN_URL = "https://api-sec-vlc.hotmart.com/security/oauth/token"

@pytest.fixture
def config():
    return ClientConfig(client_id="cid", client_secret="csec", basic="Basic dGVzdA==")

@pytest.fixture
def manager(config):
    return TokenManager(config)


def _token_response(token: str = "tok123", expires_in: int = 86400) -> httpx.Response:
    return httpx.Response(200, json={"access_token": token, "token_type": "bearer", "expires_in": expires_in})


def test_get_token_fetches_new_token(manager, respx_mock):
    respx_mock.post(TOKEN_URL).mock(return_value=_token_response("tok123"))
    assert manager.get_token() == "tok123"


def test_get_token_caches_on_second_call(manager, respx_mock):
    respx_mock.post(TOKEN_URL).mock(return_value=_token_response("tok123"))
    manager.get_token()
    manager.get_token()
    assert respx_mock.calls.call_count == 1


def test_get_token_refreshes_expired_token(manager, respx_mock):
    respx_mock.post(TOKEN_URL).mock(return_value=_token_response("new_tok"))
    manager._token = "old_tok"
    manager._expires_at = time.time() - 1  # already expired
    assert manager.get_token() == "new_tok"


def test_get_token_refreshes_near_expiry(manager, respx_mock):
    respx_mock.post(TOKEN_URL).mock(return_value=_token_response("fresh"))
    manager._token = "about_to_expire"
    manager._expires_at = time.time() + 100  # within 300s buffer
    assert manager.get_token() == "fresh"


def test_invalidate_forces_refresh(manager, respx_mock):
    respx_mock.post(TOKEN_URL).mock(return_value=_token_response("tok123"))
    manager.get_token()
    manager.invalidate()
    respx_mock.post(TOKEN_URL).mock(return_value=_token_response("tok456"))
    assert manager.get_token() == "tok456"


def test_token_value_not_in_request_headers(manager, respx_mock):
    """Auth request must use basic, not the token itself."""
    captured: list[httpx.Request] = []
    def capture(req: httpx.Request) -> httpx.Response:
        captured.append(req)
        return _token_response()
    respx_mock.post(TOKEN_URL).mock(side_effect=capture)
    manager.get_token()
    assert captured[0].headers["authorization"] == "Basic dGVzdA=="


def test_concurrent_calls_fetch_token_once(manager, respx_mock):
    respx_mock.post(TOKEN_URL).mock(return_value=_token_response())
    tokens = []
    def fetch():
        tokens.append(manager.get_token())
    threads = [threading.Thread(target=fetch) for _ in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()
    assert respx_mock.calls.call_count == 1
    assert all(tok == tokens[0] for tok in tokens)

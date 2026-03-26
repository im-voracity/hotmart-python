import httpx
import respx
import pytest
from hotmart._base_client import BaseSyncClient, _build_params
from hotmart._config import ClientConfig
from hotmart._exceptions import AuthenticationError, RateLimitError, InternalServerError

TOKEN_URL = "https://api-sec-vlc.hotmart.com/security/oauth/token"
BASE = "https://developers.hotmart.com/payments/api/v1"

@pytest.fixture(autouse=True)
def mock_token(respx_mock):
    respx_mock.post(TOKEN_URL).mock(return_value=httpx.Response(200, json={
        "access_token": "test_token", "token_type": "bearer", "expires_in": 86400,
    }))

@pytest.fixture
def client():
    config = ClientConfig(client_id="cid", client_secret="csec", basic="Basic dGVzdA==", max_retries=0)
    return BaseSyncClient(config)


def test_build_params_drops_none():
    result = _build_params({"self": None, "a": 1, "b": None, "c": "x"})
    assert result == {"a": 1, "c": "x"}

def test_build_params_merges_kwargs():
    result = _build_params({"self": None, "a": 1, "kwargs": {"extra": "val"}})
    assert result == {"a": 1, "extra": "val"}

def test_get_returns_deserialized_model(client, respx_mock):
    from pydantic import BaseModel
    class MyModel(BaseModel):
        foo: str

    respx_mock.get(f"{BASE}/test").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
    result = client._get("/test", cast_to=MyModel)
    assert result.foo == "bar"

def test_get_returns_none_for_empty_response(client, respx_mock):
    respx_mock.get(f"{BASE}/test").mock(return_value=httpx.Response(200, text="{}"))
    result = client._get("/test")
    assert result is None

def test_raises_authentication_error_on_403(client, respx_mock):
    respx_mock.get(f"{BASE}/test").mock(return_value=httpx.Response(403))
    with pytest.raises(AuthenticationError):
        client._get("/test")

def test_raises_rate_limit_on_429(client, respx_mock):
    respx_mock.get(f"{BASE}/test").mock(return_value=httpx.Response(429, headers={"RateLimit-Reset": "1"}))
    with pytest.raises(RateLimitError):
        client._get("/test")

def test_raises_internal_server_error_on_500(client, respx_mock):
    respx_mock.get(f"{BASE}/test").mock(return_value=httpx.Response(500))
    with pytest.raises(InternalServerError):
        client._get("/test")

def test_retries_on_500_then_succeeds(respx_mock):
    from pydantic import BaseModel
    class M(BaseModel):
        ok: bool
    config = ClientConfig(client_id="cid", client_secret="csec", basic="Basic x", max_retries=2)
    client = BaseSyncClient(config)
    respx_mock.get(f"{BASE}/test").mock(side_effect=[
        httpx.Response(500),
        httpx.Response(200, json={"ok": True}),
    ])
    result = client._get("/test", cast_to=M)
    assert result.ok is True

def test_401_triggers_token_refresh_and_retries(client, respx_mock):
    from pydantic import BaseModel
    class M(BaseModel):
        val: int
    respx_mock.get(f"{BASE}/test").mock(side_effect=[
        httpx.Response(401),
        httpx.Response(200, json={"val": 42}),
    ])
    result = client._get("/test", cast_to=M)
    assert result.val == 42

def test_context_manager_closes_client():
    config = ClientConfig(client_id="cid", client_secret="csec", basic="Basic x")
    with BaseSyncClient(config) as c:
        assert not c._http.is_closed
    assert c._http.is_closed

def test_uses_sandbox_url(respx_mock):
    from pydantic import BaseModel
    class M(BaseModel):
        x: int
    respx_mock.get("https://sandbox.hotmart.com/payments/api/v1/test").mock(
        return_value=httpx.Response(200, json={"x": 1})
    )
    config = ClientConfig(client_id="cid", client_secret="csec", basic="Basic x", sandbox=True, max_retries=0)
    c = BaseSyncClient(config)
    result = c._get("/test", cast_to=M)
    assert result.x == 1

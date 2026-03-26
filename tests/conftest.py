import httpx
import pytest
from hotmart import Hotmart

TOKEN_URL = "https://api-sec-vlc.hotmart.com/security/oauth/token"

@pytest.fixture
def client(respx_mock):
    respx_mock.post(TOKEN_URL).mock(return_value=httpx.Response(200, json={
        "access_token": "test_token", "token_type": "bearer", "expires_in": 86400,
    }))
    return Hotmart(client_id="test_id", client_secret="test_secret", basic="Basic dGVzdA==", max_retries=0)

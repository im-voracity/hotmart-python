import httpx
import pytest

from hotmart._base_client import BaseSyncClient
from hotmart._config import ClientConfig
from hotmart.resources.negotiation import Negotiation

TOKEN_URL = "https://api-sec-vlc.hotmart.com/security/oauth/token"
BASE = "https://developers.hotmart.com/payments/api/v1"

@pytest.fixture(autouse=True)
def mock_token(respx_mock):
    respx_mock.post(TOKEN_URL).mock(return_value=httpx.Response(200, json={
        "access_token": "tok", "token_type": "bearer", "expires_in": 86400,
    }))

@pytest.fixture
def negotiation():
    config = ClientConfig(client_id="cid", client_secret="csec", basic="Basic x", max_retries=0)
    return Negotiation(BaseSyncClient(config))


def test_create_posts_subscriber_code(negotiation, respx_mock):
    captured: list[httpx.Request] = []
    def capture(req: httpx.Request) -> httpx.Response:
        captured.append(req)
        return httpx.Response(200, json={"offer_url": "https://hotmart.com/offer"})
    respx_mock.post(f"{BASE}/negotiation").mock(side_effect=capture)
    negotiation.create("ABC1")
    import json
    body = json.loads(captured[0].content)
    assert body["subscriber_code"] == "ABC1"

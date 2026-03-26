import httpx
import pytest

from hotmart._base_client import BaseSyncClient
from hotmart._config import ClientConfig
from hotmart.resources.events import Events

TOKEN_URL = "https://api-sec-vlc.hotmart.com/security/oauth/token"
BASE = "https://developers.hotmart.com/payments/api/v1"

@pytest.fixture(autouse=True)
def mock_token(respx_mock):
    respx_mock.post(TOKEN_URL).mock(return_value=httpx.Response(200, json={
        "access_token": "tok", "token_type": "bearer", "expires_in": 86400,
    }))

@pytest.fixture
def events():
    config = ClientConfig(client_id="cid", client_secret="csec", basic="Basic x", max_retries=0)
    return Events(BaseSyncClient(config))


def test_get_event_calls_correct_path(events, respx_mock):
    respx_mock.get(f"{BASE}/events/EVT1").mock(return_value=httpx.Response(200, json={"id": "EVT1"}))
    result = events.get("EVT1")
    assert result is not None


def test_tickets_returns_paginated(events, respx_mock):
    data = {"items": [{"ticket_id": "T1"}], "page_info": {}}
    respx_mock.get(f"{BASE}/tickets").mock(return_value=httpx.Response(200, json=data))
    result = events.tickets(product_id=123)
    assert len(result.items) == 1

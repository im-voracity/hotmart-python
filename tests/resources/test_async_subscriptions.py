import httpx
import pytest

from hotmart._async_base_client import BaseAsyncClient
from hotmart._config import ClientConfig
from hotmart.resources.async_subscriptions import AsyncSubscriptions

TOKEN_URL = "https://api-sec-vlc.hotmart.com/security/oauth/token"
BASE = "https://developers.hotmart.com/payments/api/v1"

SUB_ITEM = {"subscriber_code": "ABC1", "status": "ACTIVE", "product": {"id": 1}}
LIST_RESPONSE = {"items": [SUB_ITEM], "page_info": {"results_per_page": 10}}

@pytest.fixture(autouse=True)
def mock_token(respx_mock):
    respx_mock.post(TOKEN_URL).mock(return_value=httpx.Response(200, json={
        "access_token": "tok", "token_type": "bearer", "expires_in": 86400,
    }))

@pytest.fixture
def subs():
    config = ClientConfig(client_id="cid", client_secret="csec", basic="Basic x", max_retries=0)
    return AsyncSubscriptions(BaseAsyncClient(config))


async def test_list_returns_paginated(subs, respx_mock):
    respx_mock.get(f"{BASE}/subscriptions").mock(return_value=httpx.Response(200, json=LIST_RESPONSE))
    result = await subs.list()
    assert result.items[0].subscriber_code == "ABC1"


async def test_purchases_returns_list(subs, respx_mock):
    data = [{"transaction": "HP1", "status": "APPROVED"}]
    respx_mock.get(f"{BASE}/subscriptions/ABC1/purchases").mock(return_value=httpx.Response(200, json=data))
    result = await subs.purchases("ABC1")
    assert result[0].transaction == "HP1"


async def test_cancel_calls_post_with_body(subs, respx_mock):
    resp = {"success_subscriptions": [{"subscriber_code": "ABC1", "status": "INACTIVE"}], "fail_subscriptions": []}
    respx_mock.post(f"{BASE}/subscriptions/cancel").mock(return_value=httpx.Response(200, json=resp))
    result = await subs.cancel(["ABC1"])
    assert result.success_subscriptions[0].subscriber_code == "ABC1"


async def test_change_due_day_calls_patch(subs, respx_mock):
    respx_mock.patch(f"{BASE}/subscriptions/ABC1").mock(return_value=httpx.Response(200, text="{}"))
    await subs.change_due_day("ABC1", 15)  # no error = success


async def test_reactivate_single_calls_post(subs, respx_mock):
    resp = {"subscriber_code": "ABC1", "status": "INACTIVE"}
    respx_mock.post(f"{BASE}/subscriptions/ABC1/reactivate").mock(return_value=httpx.Response(200, json=resp))
    result = await subs.reactivate_single("ABC1", charge=True)
    assert result.subscriber_code == "ABC1"

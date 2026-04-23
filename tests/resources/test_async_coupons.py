import httpx
import pytest

from hotmart._async_base_client import BaseAsyncClient
from hotmart._config import ClientConfig
from hotmart.resources.async_coupons import AsyncCoupons

TOKEN_URL = "https://api-sec-vlc.hotmart.com/security/oauth/token"
BASE = "https://developers.hotmart.com/payments/api/v1"

@pytest.fixture(autouse=True)
def mock_token(respx_mock):
    respx_mock.post(TOKEN_URL).mock(return_value=httpx.Response(200, json={
        "access_token": "tok", "token_type": "bearer", "expires_in": 86400,
    }))

@pytest.fixture
def coupons():
    config = ClientConfig(client_id="cid", client_secret="csec", basic="Basic x", max_retries=0)
    return AsyncCoupons(BaseAsyncClient(config))


async def test_create_posts_to_correct_url(coupons, respx_mock):
    respx_mock.post(f"{BASE}/product/P123/coupon").mock(return_value=httpx.Response(200, text="{}"))
    await coupons.create("P123", "SAVE20", 0.20)  # no error = success


async def test_list_returns_paginated(coupons, respx_mock):
    data = {"items": [{"code": "SAVE20", "discount": 0.20}], "page_info": {}}
    respx_mock.get(f"{BASE}/coupon/product/P123").mock(return_value=httpx.Response(200, json=data))
    result = await coupons.list("P123")
    assert result.items[0].code == "SAVE20"


async def test_delete_calls_delete_method(coupons, respx_mock):
    respx_mock.delete(f"{BASE}/coupon/CPN1").mock(return_value=httpx.Response(200, text="{}"))
    await coupons.delete("CPN1")  # no error = success

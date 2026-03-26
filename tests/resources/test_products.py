import httpx
import pytest

from hotmart._base_client import BaseSyncClient
from hotmart._config import ClientConfig
from hotmart.resources.products import Products

TOKEN_URL = "https://api-sec-vlc.hotmart.com/security/oauth/token"
PROD_BASE = "https://developers.hotmart.com/products/api/v1"

PRODUCT_RESPONSE = {
    "items": [{"id": 123, "name": "Course A", "ucode": "abc-123", "status": "ACTIVE", "format": "ONLINE_COURSE"}],
    "page_info": {"results_per_page": 10},
}

@pytest.fixture(autouse=True)
def mock_token(respx_mock):
    respx_mock.post(TOKEN_URL).mock(return_value=httpx.Response(200, json={
        "access_token": "tok", "token_type": "bearer", "expires_in": 86400,
    }))

@pytest.fixture
def products():
    config = ClientConfig(client_id="cid", client_secret="csec", basic="Basic x", max_retries=0)
    return Products(BaseSyncClient(config))


def test_list_returns_products(products, respx_mock):
    respx_mock.get(f"{PROD_BASE}/products").mock(return_value=httpx.Response(200, json=PRODUCT_RESPONSE))
    result = products.list()
    assert result.items[0].name == "Course A"


def test_offers_uses_ucode_path(products, respx_mock):
    respx_mock.get(f"{PROD_BASE}/products/abc-123/offers").mock(
        return_value=httpx.Response(200, json={"items": [{"code": "offer1"}], "page_info": {}})
    )
    result = products.offers("abc-123")
    assert result.items[0].code == "offer1"


def test_plans_uses_ucode_path(products, respx_mock):
    respx_mock.get(f"{PROD_BASE}/products/abc-123/plans").mock(
        return_value=httpx.Response(200, json={"items": [{"code": "plan1", "periodicity": "MONTHLY"}], "page_info": {}})
    )
    result = products.plans("abc-123")
    assert result.items[0].periodicity == "MONTHLY"

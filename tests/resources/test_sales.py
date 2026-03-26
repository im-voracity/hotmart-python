import httpx
import respx
import pytest
from hotmart._base_client import BaseSyncClient
from hotmart._config import ClientConfig
from hotmart.resources.sales import Sales
from hotmart.models.pagination import PaginatedResponse
from hotmart.models.sales import SaleHistoryItem, SaleSummaryItem

TOKEN_URL = "https://api-sec-vlc.hotmart.com/security/oauth/token"
BASE = "https://developers.hotmart.com/payments/api/v1"

HISTORY_RESPONSE = {
    "items": [{"purchase": {"transaction": "HP123", "status": "APPROVED"}, "buyer": {"name": "Paula"}}],
    "page_info": {"total_results": 1, "results_per_page": 10},
}

@pytest.fixture(autouse=True)
def mock_token(respx_mock):
    respx_mock.post(TOKEN_URL).mock(return_value=httpx.Response(200, json={
        "access_token": "tok", "token_type": "bearer", "expires_in": 86400,
    }))

@pytest.fixture
def sales():
    config = ClientConfig(client_id="cid", client_secret="csec", basic="Basic x", max_retries=0)
    return Sales(BaseSyncClient(config))


def test_history_returns_paginated_response(sales, respx_mock):
    respx_mock.get(f"{BASE}/sales/history").mock(return_value=httpx.Response(200, json=HISTORY_RESPONSE))
    result = sales.history()
    assert isinstance(result, PaginatedResponse)
    assert result.items[0].purchase.transaction == "HP123"


def test_history_passes_params(sales, respx_mock):
    captured: list[httpx.Request] = []
    def capture(req: httpx.Request) -> httpx.Response:
        captured.append(req)
        return httpx.Response(200, json=HISTORY_RESPONSE)
    respx_mock.get(f"{BASE}/sales/history").mock(side_effect=capture)
    sales.history(buyer_name="Paula", transaction_status="APPROVED")
    assert "buyer_name=Paula" in str(captured[0].url)
    assert "transaction_status=APPROVED" in str(captured[0].url)


def test_history_passes_kwargs(sales, respx_mock):
    captured: list[httpx.Request] = []
    def capture(req: httpx.Request) -> httpx.Response:
        captured.append(req)
        return httpx.Response(200, json=HISTORY_RESPONSE)
    respx_mock.get(f"{BASE}/sales/history").mock(side_effect=capture)
    sales.history(custom_param="val")
    assert "custom_param=val" in str(captured[0].url)


def test_history_autopaginate_follows_next_page_token(sales, respx_mock):
    page1 = {"items": [{"purchase": {"transaction": "HP1"}}], "page_info": {"next_page_token": "tok2"}}
    page2 = {"items": [{"purchase": {"transaction": "HP2"}}], "page_info": {}}
    respx_mock.get(f"{BASE}/sales/history").mock(side_effect=[
        httpx.Response(200, json=page1),
        httpx.Response(200, json=page2),
    ])
    items = list(sales.history_autopaginate())
    assert len(items) == 2


def test_refund_calls_put(sales, respx_mock):
    respx_mock.put(f"{BASE}/sales/HP123/refund").mock(return_value=httpx.Response(200, text="{}"))
    sales.refund("HP123")  # no error = success

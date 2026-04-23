"""
Testes de integração assíncronos contra a API real da Hotmart.

Executar:
    uv run pytest tests/test_async_integration.py -v

Requer variáveis de ambiente (ou arquivo .env lido manualmente):
    HOTMART_CLIENT_ID
    HOTMART_CLIENT_SECRET
    HOTMART_BASIC

Os testes são automaticamente pulados se as variáveis não estiverem definidas.
Respostas vazias (sem dados) são aceitas — o que importa é a estrutura retornada.
"""
import os

import pytest

from hotmart import AsyncHotmart
from hotmart._exceptions import HotmartError
from hotmart.models.pagination import PaginatedResponse

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _creds() -> tuple[str, str, str] | None:
    cid = os.getenv("HOTMART_CLIENT_ID")
    secret = os.getenv("HOTMART_CLIENT_SECRET")
    basic = os.getenv("HOTMART_BASIC")
    if not (cid and secret and basic):
        return None
    return cid, secret, basic


def _skip_if_no_creds():
    if _creds() is None:
        pytest.skip("Credenciais não configuradas (HOTMART_CLIENT_ID / HOTMART_CLIENT_SECRET / HOTMART_BASIC)")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
async def live_client():
    _skip_if_no_creds()
    cid, secret, basic = _creds()  # type: ignore[misc]
    async with AsyncHotmart(client_id=cid, client_secret=secret, basic=basic) as client:
        yield client


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

class TestAuth:
    async def test_obtém_token(self, live_client):
        token = await live_client._token_manager.get_token()
        assert isinstance(token, str)
        assert len(token) > 10

    async def test_token_é_cacheado(self, live_client):
        t1 = await live_client._token_manager.get_token()
        t2 = await live_client._token_manager.get_token()
        assert t1 == t2


# ---------------------------------------------------------------------------
# Sales
# ---------------------------------------------------------------------------

class TestSales:
    async def test_history_retorna_paginado(self, live_client):
        result = await live_client.sales.history()
        assert isinstance(result, PaginatedResponse)

    async def test_history_items_têm_campos_esperados(self, live_client):
        result = await live_client.sales.history()
        for item in result.items:
            assert hasattr(item, "transaction")
            assert hasattr(item, "purchase")

    async def test_summary_retorna_paginado(self, live_client):
        result = await live_client.sales.summary()
        assert isinstance(result, PaginatedResponse)

    async def test_participants_retorna_paginado(self, live_client):
        result = await live_client.sales.participants()
        assert isinstance(result, PaginatedResponse)

    async def test_commissions_retorna_paginado(self, live_client):
        result = await live_client.sales.commissions()
        assert isinstance(result, PaginatedResponse)

    async def test_price_details_retorna_paginado(self, live_client):
        result = await live_client.sales.price_details()
        assert isinstance(result, PaginatedResponse)

    async def test_history_com_max_results(self, live_client):
        result = await live_client.sales.history(max_results=5)
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) <= 5

    async def test_history_page_info_presente_se_há_dados(self, live_client):
        result = await live_client.sales.history()
        if result.items:
            assert result.page_info is not None


# ---------------------------------------------------------------------------
# Subscriptions
# ---------------------------------------------------------------------------

class TestSubscriptions:
    async def test_list_retorna_paginado(self, live_client):
        result = await live_client.subscriptions.list()
        assert isinstance(result, PaginatedResponse)

    async def test_list_items_têm_campos_esperados(self, live_client):
        result = await live_client.subscriptions.list()
        for item in result.items:
            assert hasattr(item, "subscriber_code")
            assert hasattr(item, "status")

    async def test_summary_retorna_paginado(self, live_client):
        result = await live_client.subscriptions.summary()
        assert isinstance(result, PaginatedResponse)

    async def test_list_filtra_por_status(self, live_client):
        result = await live_client.subscriptions.list(status="ACTIVE")
        assert isinstance(result, PaginatedResponse)
        for item in result.items:
            assert item.status == "ACTIVE"

    async def test_purchases_requer_subscriber_code(self, live_client):
        result = await live_client.subscriptions.list()
        if not result.items:
            pytest.skip("Sem assinaturas para testar purchases")
        code = result.items[0].subscriber_code
        purchases = await live_client.subscriptions.purchases(subscriber_code=code)
        assert isinstance(purchases, PaginatedResponse)

    async def test_transactions_requer_subscriber_code(self, live_client):
        result = await live_client.subscriptions.list()
        if not result.items:
            pytest.skip("Sem assinaturas para testar transactions")
        code = result.items[0].subscriber_code
        txs = await live_client.subscriptions.transactions(subscriber_code=code)
        assert isinstance(txs, PaginatedResponse)


# ---------------------------------------------------------------------------
# Products
# ---------------------------------------------------------------------------

class TestProducts:
    async def test_list_retorna_paginado(self, live_client):
        result = await live_client.products.list()
        assert isinstance(result, PaginatedResponse)

    async def test_list_items_têm_campos_esperados(self, live_client):
        result = await live_client.products.list()
        for item in result.items:
            assert hasattr(item, "ucode")
            assert hasattr(item, "name")

    async def test_offers_requer_ucode(self, live_client):
        result = await live_client.products.list()
        if not result.items:
            pytest.skip("Sem produtos para testar offers")
        ucode = result.items[0].ucode
        offers = await live_client.products.offers(ucode=ucode)
        assert isinstance(offers, PaginatedResponse)

    async def test_plans_requer_ucode(self, live_client):
        result = await live_client.products.list()
        if not result.items:
            pytest.skip("Sem produtos para testar plans")
        ucode = result.items[0].ucode
        from hotmart._exceptions import BadRequestError
        try:
            plans = await live_client.products.plans(ucode=ucode)
            assert isinstance(plans, PaginatedResponse)
        except BadRequestError:
            pytest.xfail("Hotmart bug: /products/{ucode}/plans retorna 400 para produtos sem planos")


# ---------------------------------------------------------------------------
# Coupons
# ---------------------------------------------------------------------------

class TestCoupons:
    async def test_list_retorna_paginado(self, live_client):
        products = await live_client.products.list()
        if not products.items:
            pytest.skip("Sem produtos para testar coupons")
        ucode = products.items[0].ucode
        result = await live_client.coupons.list(product_id=ucode)
        assert isinstance(result, PaginatedResponse)


# ---------------------------------------------------------------------------
# Smoke — todos os endpoints retornam sem exceção
# ---------------------------------------------------------------------------

class TestSmoke:
    """Garante que nenhum endpoint assíncrono lança exceção inesperada."""

    @pytest.mark.parametrize("call", [
        lambda c: c.sales.history(),
        lambda c: c.sales.summary(),
        lambda c: c.sales.participants(),
        lambda c: c.sales.commissions(),
        lambda c: c.sales.price_details(),
        lambda c: c.subscriptions.list(),
        lambda c: c.subscriptions.summary(),
        lambda c: c.products.list(),
    ])
    async def test_endpoint_não_lança_exceção(self, live_client, call):
        try:
            await call(live_client)
        except HotmartError as e:
            pytest.fail(f"HotmartError inesperado: {e}")

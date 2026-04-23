from __future__ import annotations

import logging

from ._async_base_client import BaseAsyncClient
from ._config import ClientConfig
from .resources.async_club import AsyncClub
from .resources.async_coupons import AsyncCoupons
from .resources.async_events import AsyncEvents
from .resources.async_negotiation import AsyncNegotiation
from .resources.async_products import AsyncProducts
from .resources.async_sales import AsyncSales
from .resources.async_subscriptions import AsyncSubscriptions


class AsyncHotmart(BaseAsyncClient):
    """
    Async client for the Hotmart API.

    Cliente assíncrono para a API da Hotmart.

    Usage / Uso::

        async with AsyncHotmart(client_id="...", client_secret="...", basic="Basic ...") as client:
            sales = await client.sales.history(buyer_name="Paula")
    """

    sales: AsyncSales
    subscriptions: AsyncSubscriptions
    products: AsyncProducts
    coupons: AsyncCoupons
    club: AsyncClub
    events: AsyncEvents
    negotiation: AsyncNegotiation

    def __init__(
        self,
        *,
        client_id: str,
        client_secret: str,
        basic: str,
        sandbox: bool = False,
        max_retries: int = 3,
        timeout: float = 30.0,
        log_level: int = logging.WARNING,
    ) -> None:
        config = ClientConfig(
            client_id=client_id,
            client_secret=client_secret,
            basic=basic,
            sandbox=sandbox,
            max_retries=max_retries,
            timeout=timeout,
            log_level=log_level,
        )
        super().__init__(config)
        self.sales = AsyncSales(self)
        self.subscriptions = AsyncSubscriptions(self)
        self.products = AsyncProducts(self)
        self.coupons = AsyncCoupons(self)
        self.club = AsyncClub(self)
        self.events = AsyncEvents(self)
        self.negotiation = AsyncNegotiation(self)

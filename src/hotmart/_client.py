from __future__ import annotations

import logging

from ._base_client import BaseSyncClient
from ._config import ClientConfig
from .resources.club import Club
from .resources.coupons import Coupons
from .resources.events import Events
from .resources.negotiation import Negotiation
from .resources.products import Products
from .resources.sales import Sales
from .resources.subscriptions import Subscriptions


class Hotmart(BaseSyncClient):
    """
    Main client for the Hotmart API.

    Usage:
        client = Hotmart(client_id="...", client_secret="...", basic="Basic ...")
        sales = client.sales.history(buyer_name="Paula")
    """

    sales: Sales
    subscriptions: Subscriptions
    products: Products
    coupons: Coupons
    club: Club
    events: Events
    negotiation: Negotiation

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
        self.sales = Sales(self)
        self.subscriptions = Subscriptions(self)
        self.products = Products(self)
        self.coupons = Coupons(self)
        self.club = Club(self)
        self.events = Events(self)
        self.negotiation = Negotiation(self)

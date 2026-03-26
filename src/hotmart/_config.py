from __future__ import annotations

import logging
from dataclasses import dataclass

AUTH_URL = "https://api-sec-vlc.hotmart.com/security/oauth/token"

BASE_URLS: dict[str, dict[str, str]] = {
    "prod": {
        "payments": "https://developers.hotmart.com/payments/api/v1",
        "club": "https://developers.hotmart.com/club/api/v1",
        "products": "https://developers.hotmart.com/products/api/v1",
    },
    "sandbox": {
        "payments": "https://sandbox.hotmart.com/payments/api/v1",
        "club": "https://sandbox.hotmart.com/club/api/v1",
        "products": "https://sandbox.hotmart.com/products/api/v1",
    },
}


@dataclass
class ClientConfig:
    client_id: str
    client_secret: str
    basic: str
    sandbox: bool = False
    max_retries: int = 3
    timeout: float = 30.0
    log_level: int = logging.WARNING

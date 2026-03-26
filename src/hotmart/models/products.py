from __future__ import annotations
from ._common import _Base, Price
from ._enums import ProductStatus, ProductFormat


class ProductItem(_Base):
    id: int | None = None
    name: str | None = None
    ucode: str | None = None
    status: ProductStatus | str | None = None
    created_at: int | None = None
    format: ProductFormat | str | None = None
    is_subscription: bool | None = None
    warranty_period: int | None = None


class OfferItem(_Base):
    code: str | None = None
    name: str | None = None
    description: str | None = None
    price: Price | None = None
    payment_mode: str | None = None
    is_currency_conversion_enabled: bool | None = None
    is_main_offer: bool | None = None
    is_smart_recovery_enabled: bool | None = None


class PlanItem(_Base):
    code: str | None = None
    name: str | None = None
    description: str | None = None
    price: Price | None = None
    payment_mode: str | None = None
    periodicity: str | None = None
    max_installments: int | None = None
    trial_period: int | None = None
    is_subscription_recovery_enabled: bool | None = None
    is_switch_plan_enabled: bool | None = None

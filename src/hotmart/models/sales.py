from __future__ import annotations
from ._common import _Base, Price
from ._enums import PurchaseStatus, PaymentType, CommissionSource


class SaleProduct(_Base):
    id: int | None = None
    name: str | None = None


class SaleBuyer(_Base):
    name: str | None = None
    email: str | None = None
    ucode: str | None = None


class SaleProducer(_Base):
    name: str | None = None
    ucode: str | None = None


class SalePayment(_Base):
    method: str | None = None
    installments_number: int | None = None
    type: PaymentType | str | None = None


class SaleTracking(_Base):
    source: str | None = None
    source_sck: str | None = None
    external_code: str | None = None


class SaleOffer(_Base):
    code: str | None = None
    payment_mode: str | None = None


class SaleHotmartFee(_Base):
    total: float | None = None
    fixed: float | None = None
    base: float | None = None
    percentage: float | None = None
    currency_code: str | None = None


class SalePurchase(_Base):
    transaction: str | None = None
    order_date: int | None = None
    approved_date: int | None = None
    status: PurchaseStatus | str | None = None
    recurrency_number: int | None = None
    is_subscription: bool | None = None
    commission_as: CommissionSource | str | None = None
    price: Price | None = None
    payment: SalePayment | None = None
    tracking: SaleTracking | None = None
    offer: SaleOffer | None = None
    hotmart_fee: SaleHotmartFee | None = None
    warranty_expire_date: int | None = None


class SaleHistoryItem(_Base):
    product: SaleProduct | None = None
    buyer: SaleBuyer | None = None
    producer: SaleProducer | None = None
    purchase: SalePurchase | None = None


class SaleSummaryItem(_Base):
    total_items: int | None = None
    total_value: Price | None = None


class UserDocument(_Base):
    value: str | None = None
    type: str | None = None


class UserAddress(_Base):
    city: str | None = None
    state: str | None = None
    country: str | None = None
    zip_code: str | None = None
    address: str | None = None
    complement: str | None = None
    neighborhood: str | None = None
    number: str | None = None


class SaleUser(_Base):
    ucode: str | None = None
    locale: str | None = None
    name: str | None = None
    trade_name: str | None = None
    cellphone: str | None = None
    phone: str | None = None
    email: str | None = None
    documents: list[UserDocument] = []
    address: UserAddress | None = None


class SaleParticipant(_Base):
    role: CommissionSource | str | None = None
    user: SaleUser | None = None


class SaleParticipantsItem(_Base):
    transaction: str | None = None
    product: SaleProduct | None = None
    users: list[SaleParticipant] = []


class CommissionAmount(_Base):
    value: float | None = None
    currency_value: str | None = None


class SaleCommission(_Base):
    commission: CommissionAmount | None = None
    user: _Base | None = None
    source: CommissionSource | str | None = None


class SaleCommissionsItem(_Base):
    transaction: str | None = None
    product: SaleProduct | None = None
    exchange_rate_currency_payout: float | None = None
    commissions: list[SaleCommission] = []


class SaleCoupon(_Base):
    code: str | None = None
    value: float | None = None


class SalePriceDetailsItem(_Base):
    transaction: str | None = None
    product: SaleProduct | None = None
    base: Price | None = None
    total: Price | None = None
    vat: Price | None = None
    fee: Price | None = None
    coupon: SaleCoupon | None = None
    real_conversion_rate: float | None = None

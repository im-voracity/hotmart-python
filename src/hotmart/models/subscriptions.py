from __future__ import annotations
from ._common import _Base, Price
from ._enums import SubscriptionStatus, PaymentType


class SubPlan(_Base):
    name: str | None = None
    id: int | None = None
    recurrency_period: int | None = None
    max_charge_cycles: int | None = None


class SubProduct(_Base):
    id: int | None = None
    name: str | None = None
    ucode: str | None = None


class SubSubscriber(_Base):
    name: str | None = None
    email: str | None = None
    ucode: str | None = None
    id: int | None = None


class SubscriptionItem(_Base):
    subscriber_code: str | None = None
    subscription_id: int | None = None
    status: SubscriptionStatus | str | None = None
    accession_date: int | None = None
    end_accession_date: int | None = None
    request_date: int | None = None
    date_next_charge: int | None = None
    trial: bool | None = None
    transaction: str | None = None
    plan: SubPlan | None = None
    product: SubProduct | None = None
    price: Price | None = None
    subscriber: SubSubscriber | None = None


class LastRecurrency(_Base):
    number: int | None = None
    request_date: int | None = None
    status: str | None = None
    transaction_number: int | None = None
    billing_type: str | None = None


class SubscriptionSummaryItem(_Base):
    subscriber_code: str | None = None
    subscription_id: int | None = None
    status: SubscriptionStatus | str | None = None
    lifetime: int | None = None
    accession_date: int | None = None
    end_accession_date: int | None = None
    trial: bool | None = None
    plan: _Base | None = None
    product: _Base | None = None
    offer: _Base | None = None
    last_recurrency: LastRecurrency | None = None
    unpaid_recurrencies: list[_Base] = []
    subscriber: _Base | None = None


class SubscriptionPurchase(_Base):
    transaction: str | None = None
    approved_date: int | None = None
    payment_engine: str | None = None
    status: str | None = None
    price: Price | None = None
    payment_type: PaymentType | str | None = None
    payment_method: str | None = None
    recurrency_number: int | None = None
    under_warranty: bool | None = None
    purchase_subscription: bool | None = None


class SubShopper(_Base):
    email: str | None = None
    phone: str | None = None


class SubscriptionResult(_Base):
    status: str | None = None
    subscriber_code: str | None = None
    creation_date: str | None = None
    current_recurrence: int | None = None
    date_last_recurrence: str | None = None
    date_next_charge: str | None = None
    due_day: int | None = None
    trial_period: int | None = None
    interval_type_between_charges: str | None = None
    interval_between_charges: int | None = None
    max_charge_cycles: int | None = None
    activation_date: str | None = None
    error: str | None = None
    shopper: SubShopper | None = None


class SubscriptionBulkResponse(_Base):
    success_subscriptions: list[SubscriptionResult] = []
    fail_subscriptions: list[SubscriptionResult] = []

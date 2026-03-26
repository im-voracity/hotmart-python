from __future__ import annotations
from collections.abc import Iterator
from typing import Any
from ._base import APIResource
from .._base_client import _build_params
from ..models.pagination import PaginatedResponse
from ..models.sales import (
    SaleHistoryItem, SaleSummaryItem, SaleParticipantsItem,
    SaleCommissionsItem, SalePriceDetailsItem,
)
from ..models._enums import PurchaseStatus, PaymentType, CommissionSource


class Sales(APIResource):

    def history(
        self,
        *,
        product_id: int | None = None,
        start_date: int | None = None,
        end_date: int | None = None,
        sales_source: str | None = None,
        transaction: str | None = None,
        buyer_name: str | None = None,
        buyer_email: str | None = None,
        transaction_status: PurchaseStatus | str | None = None,
        payment_type: PaymentType | str | None = None,
        offer_code: str | None = None,
        commission_as: CommissionSource | str | None = None,
        max_results: int | None = None,
        page_token: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse[SaleHistoryItem]:
        params = _build_params(locals())
        return self._get("/sales/history", params=params, cast_to=PaginatedResponse[SaleHistoryItem])  # type: ignore[return-value]

    def history_autopaginate(self, **kwargs: Any) -> Iterator[SaleHistoryItem]:
        page_token: str | None = None
        while True:
            page = self.history(page_token=page_token, **kwargs)
            yield from page.items
            if not page.page_info or not page.page_info.next_page_token:
                break
            page_token = page.page_info.next_page_token

    def summary(
        self,
        *,
        product_id: int | None = None,
        start_date: int | None = None,
        end_date: int | None = None,
        sales_source: str | None = None,
        affiliate_name: str | None = None,
        payment_type: PaymentType | str | None = None,
        offer_code: str | None = None,
        transaction: str | None = None,
        transaction_status: PurchaseStatus | str | None = None,
        max_results: int | None = None,
        page_token: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse[SaleSummaryItem]:
        params = _build_params(locals())
        return self._get("/sales/summary", params=params, cast_to=PaginatedResponse[SaleSummaryItem])  # type: ignore[return-value]

    def summary_autopaginate(self, **kwargs: Any) -> Iterator[SaleSummaryItem]:
        page_token: str | None = None
        while True:
            page = self.summary(page_token=page_token, **kwargs)
            yield from page.items
            if not page.page_info or not page.page_info.next_page_token:
                break
            page_token = page.page_info.next_page_token

    def participants(
        self,
        *,
        product_id: int | None = None,
        start_date: int | None = None,
        end_date: int | None = None,
        buyer_email: str | None = None,
        buyer_name: str | None = None,
        sales_source: str | None = None,
        transaction: str | None = None,
        affiliate_name: str | None = None,
        commission_as: CommissionSource | str | None = None,
        transaction_status: PurchaseStatus | str | None = None,
        max_results: int | None = None,
        page_token: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse[SaleParticipantsItem]:
        params = _build_params(locals())
        return self._get("/sales/users", params=params, cast_to=PaginatedResponse[SaleParticipantsItem])  # type: ignore[return-value]

    def participants_autopaginate(self, **kwargs: Any) -> Iterator[SaleParticipantsItem]:
        page_token: str | None = None
        while True:
            page = self.participants(page_token=page_token, **kwargs)
            yield from page.items
            if not page.page_info or not page.page_info.next_page_token:
                break
            page_token = page.page_info.next_page_token

    def commissions(
        self,
        *,
        product_id: int | None = None,
        start_date: int | None = None,
        end_date: int | None = None,
        transaction: str | None = None,
        commission_as: CommissionSource | str | None = None,
        transaction_status: PurchaseStatus | str | None = None,
        max_results: int | None = None,
        page_token: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse[SaleCommissionsItem]:
        params = _build_params(locals())
        return self._get("/sales/commissions", params=params, cast_to=PaginatedResponse[SaleCommissionsItem])  # type: ignore[return-value]

    def commissions_autopaginate(self, **kwargs: Any) -> Iterator[SaleCommissionsItem]:
        page_token: str | None = None
        while True:
            page = self.commissions(page_token=page_token, **kwargs)
            yield from page.items
            if not page.page_info or not page.page_info.next_page_token:
                break
            page_token = page.page_info.next_page_token

    def price_details(
        self,
        *,
        product_id: int | None = None,
        start_date: int | None = None,
        end_date: int | None = None,
        transaction: str | None = None,
        transaction_status: PurchaseStatus | str | None = None,
        payment_type: PaymentType | str | None = None,
        max_results: int | None = None,
        page_token: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse[SalePriceDetailsItem]:
        params = _build_params(locals())
        return self._get("/sales/price/details", params=params, cast_to=PaginatedResponse[SalePriceDetailsItem])  # type: ignore[return-value]

    def price_details_autopaginate(self, **kwargs: Any) -> Iterator[SalePriceDetailsItem]:
        page_token: str | None = None
        while True:
            page = self.price_details(page_token=page_token, **kwargs)
            yield from page.items
            if not page.page_info or not page.page_info.next_page_token:
                break
            page_token = page.page_info.next_page_token

    def refund(self, transaction_code: str) -> None:
        # NOTE: spec table lists this as POST /sales/refund but the API reference
        # confirms PUT /payments/api/v1/sales/:transaction_code/refund — API wins.
        self._put(f"/sales/{transaction_code}/refund")

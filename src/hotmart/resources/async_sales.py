from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

from .._base_client import _build_params
from ..models._enums import CommissionSource, PaymentType, PurchaseStatus
from ..models.pagination import PaginatedResponse
from ..models.sales import (
    SaleCommissionsItem,
    SaleHistoryItem,
    SaleParticipantsItem,
    SalePriceDetailsItem,
    SaleSummaryItem,
)
from ._async_base import AsyncAPIResource


class AsyncSales(AsyncAPIResource):

    async def history(
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
        return await self._get("/sales/history", params=params, cast_to=PaginatedResponse[SaleHistoryItem])  # type: ignore[return-value]

    async def history_autopaginate(self, **kwargs: Any) -> AsyncIterator[SaleHistoryItem]:
        page_token: str | None = None
        while True:
            page = await self.history(page_token=page_token, **kwargs)
            for item in page.items:
                yield item
            if not page.page_info or not page.page_info.next_page_token:
                break
            page_token = page.page_info.next_page_token

    async def summary(
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
        return await self._get("/sales/summary", params=params, cast_to=PaginatedResponse[SaleSummaryItem])  # type: ignore[return-value]

    async def summary_autopaginate(self, **kwargs: Any) -> AsyncIterator[SaleSummaryItem]:
        page_token: str | None = None
        while True:
            page = await self.summary(page_token=page_token, **kwargs)
            for item in page.items:
                yield item
            if not page.page_info or not page.page_info.next_page_token:
                break
            page_token = page.page_info.next_page_token

    async def participants(
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
        return await self._get("/sales/users", params=params, cast_to=PaginatedResponse[SaleParticipantsItem])  # type: ignore[return-value]

    async def participants_autopaginate(self, **kwargs: Any) -> AsyncIterator[SaleParticipantsItem]:
        page_token: str | None = None
        while True:
            page = await self.participants(page_token=page_token, **kwargs)
            for item in page.items:
                yield item
            if not page.page_info or not page.page_info.next_page_token:
                break
            page_token = page.page_info.next_page_token

    async def commissions(
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
        return await self._get("/sales/commissions", params=params, cast_to=PaginatedResponse[SaleCommissionsItem])  # type: ignore[return-value]

    async def commissions_autopaginate(self, **kwargs: Any) -> AsyncIterator[SaleCommissionsItem]:
        page_token: str | None = None
        while True:
            page = await self.commissions(page_token=page_token, **kwargs)
            for item in page.items:
                yield item
            if not page.page_info or not page.page_info.next_page_token:
                break
            page_token = page.page_info.next_page_token

    async def price_details(
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
        return await self._get("/sales/price/details", params=params, cast_to=PaginatedResponse[SalePriceDetailsItem])  # type: ignore[return-value]

    async def price_details_autopaginate(self, **kwargs: Any) -> AsyncIterator[SalePriceDetailsItem]:
        page_token: str | None = None
        while True:
            page = await self.price_details(page_token=page_token, **kwargs)
            for item in page.items:
                yield item
            if not page.page_info or not page.page_info.next_page_token:
                break
            page_token = page.page_info.next_page_token

    async def refund(self, transaction_code: str) -> None:
        await self._put(f"/sales/{transaction_code}/refund")

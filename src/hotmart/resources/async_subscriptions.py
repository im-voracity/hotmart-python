from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

from .._base_client import _build_params
from ..models._enums import SubscriptionStatus
from ..models.pagination import PaginatedResponse
from ..models.subscriptions import (
    SubscriptionBulkResponse,
    SubscriptionItem,
    SubscriptionPurchase,
    SubscriptionResult,
    SubscriptionSummaryItem,
)
from ._async_base import AsyncAPIResource


class AsyncSubscriptions(AsyncAPIResource):

    async def list(
        self,
        *,
        product_id: int | None = None,
        plan: list[str] | None = None,
        plan_id: int | None = None,
        accession_date: int | None = None,
        end_accession_date: int | None = None,
        status: SubscriptionStatus | str | None = None,
        subscriber_code: str | None = None,
        subscriber_email: str | None = None,
        transaction: str | None = None,
        trial: bool | None = None,
        cancelation_date: int | None = None,
        end_cancelation_date: int | None = None,
        date_next_charge: int | None = None,
        end_date_next_charge: int | None = None,
        max_results: int | None = None,
        page_token: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse[SubscriptionItem]:
        params = _build_params(locals())
        return await self._get("/subscriptions", params=params, cast_to=PaginatedResponse[SubscriptionItem])  # type: ignore[return-value]

    async def list_autopaginate(self, **kwargs: Any) -> AsyncIterator[SubscriptionItem]:
        page_token: str | None = None
        while True:
            page = await self.list(page_token=page_token, **kwargs)
            for item in page.items:
                yield item
            if not page.page_info or not page.page_info.next_page_token:
                break
            page_token = page.page_info.next_page_token

    async def summary(
        self,
        *,
        product_id: int | None = None,
        subscriber_code: str | None = None,
        accession_date: int | None = None,
        end_accession_date: int | None = None,
        date_next_charge: int | None = None,
        max_results: int | None = None,
        page_token: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse[SubscriptionSummaryItem]:
        params = _build_params(locals())
        return await self._get(  # type: ignore[return-value]
            "/subscriptions/summary", params=params, cast_to=PaginatedResponse[SubscriptionSummaryItem]
        )

    async def summary_autopaginate(self, **kwargs: Any) -> AsyncIterator[SubscriptionSummaryItem]:
        page_token: str | None = None
        while True:
            page = await self.summary(page_token=page_token, **kwargs)
            for item in page.items:
                yield item
            if not page.page_info or not page.page_info.next_page_token:
                break
            page_token = page.page_info.next_page_token

    async def purchases(self, subscriber_code: str, **kwargs: Any) -> list[SubscriptionPurchase]:
        data: Any = await self._get(f"/subscriptions/{subscriber_code}/purchases")
        if not data:
            return []
        return [SubscriptionPurchase.model_validate(item) for item in data]

    async def transactions(self, subscriber_code: str, **kwargs: Any) -> list[Any]:
        data: Any = await self._get(f"/subscriptions/{subscriber_code}/transactions")
        return data if data else []

    async def cancel(self, subscriber_code: list[str], *, send_mail: bool = True) -> SubscriptionBulkResponse | None:
        body = {"subscriber_code": subscriber_code, "send_mail": send_mail}
        return await self._post("/subscriptions/cancel", json=body, cast_to=SubscriptionBulkResponse)

    async def reactivate(self, subscriber_code: list[str], *, charge: bool = False) -> SubscriptionBulkResponse | None:
        body = {"subscriber_code": subscriber_code, "charge": charge}
        return await self._post("/subscriptions/reactivate", json=body, cast_to=SubscriptionBulkResponse)

    async def reactivate_single(self, subscriber_code: str, *, charge: bool = False) -> SubscriptionResult | None:
        return await self._post(
            f"/subscriptions/{subscriber_code}/reactivate",
            json={"charge": charge},
            cast_to=SubscriptionResult,
        )

    async def change_due_day(self, subscriber_code: str, due_day: int) -> None:
        await self._patch(f"/subscriptions/{subscriber_code}", json={"due_day": due_day})

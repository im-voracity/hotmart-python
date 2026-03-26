from __future__ import annotations

from collections.abc import Iterator
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
from ._base import APIResource


class Subscriptions(APIResource):

    def list(
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
        return self._get("/subscriptions", params=params, cast_to=PaginatedResponse[SubscriptionItem])  # type: ignore[return-value]

    def list_autopaginate(self, **kwargs: Any) -> Iterator[SubscriptionItem]:
        page_token: str | None = None
        while True:
            page = self.list(page_token=page_token, **kwargs)
            yield from page.items
            if not page.page_info or not page.page_info.next_page_token:
                break
            page_token = page.page_info.next_page_token

    def summary(
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
        return self._get("/subscriptions/summary", params=params, cast_to=PaginatedResponse[SubscriptionSummaryItem])  # type: ignore[return-value]

    def summary_autopaginate(self, **kwargs: Any) -> Iterator[SubscriptionSummaryItem]:
        page_token: str | None = None
        while True:
            page = self.summary(page_token=page_token, **kwargs)
            yield from page.items
            if not page.page_info or not page.page_info.next_page_token:
                break
            page_token = page.page_info.next_page_token

    def purchases(self, subscriber_code: str, **kwargs: Any) -> list[SubscriptionPurchase]:
        data = self._get(f"/subscriptions/{subscriber_code}/purchases")
        if not data:
            return []
        return [SubscriptionPurchase.model_validate(item) for item in data]

    def transactions(self, subscriber_code: str, **kwargs: Any) -> list[Any]:
        data = self._get(f"/subscriptions/{subscriber_code}/transactions")
        return data if data else []

    def cancel(self, subscriber_code: list[str], *, send_mail: bool = True) -> SubscriptionBulkResponse | None:
        body = {"subscriber_code": subscriber_code, "send_mail": send_mail}
        return self._post("/subscriptions/cancel", json=body, cast_to=SubscriptionBulkResponse)

    def reactivate(self, subscriber_code: list[str], *, charge: bool = False) -> SubscriptionBulkResponse | None:
        body = {"subscriber_code": subscriber_code, "charge": charge}
        return self._post("/subscriptions/reactivate", json=body, cast_to=SubscriptionBulkResponse)

    def reactivate_single(self, subscriber_code: str, *, charge: bool = False) -> SubscriptionResult | None:
        return self._post(
            f"/subscriptions/{subscriber_code}/reactivate",
            json={"charge": charge},
            cast_to=SubscriptionResult,
        )

    def change_due_day(self, subscriber_code: str, due_day: int) -> None:
        self._patch(f"/subscriptions/{subscriber_code}", json={"due_day": due_day})

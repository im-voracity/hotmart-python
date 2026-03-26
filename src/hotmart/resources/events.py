from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from .._base_client import _build_params
from ..models.events import EventItem, TicketItem
from ..models.pagination import PaginatedResponse
from ._base import APIResource


class Events(APIResource):

    def get(self, event_id: str, **kwargs: Any) -> EventItem | None:
        # NOTE: spec table shows GET /events (no path param) but the API reference
        # confirms GET /payments/api/v1/events/:event_id — path param is correct.
        return self._get(f"/events/{event_id}", cast_to=EventItem)

    def tickets(
        self,
        *,
        product_id: int,
        max_results: int | None = None,
        page_token: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse[TicketItem]:
        params = _build_params(locals())
        return self._get("/tickets", params=params, cast_to=PaginatedResponse[TicketItem])  # type: ignore[return-value]

    def tickets_autopaginate(self, *, product_id: int, **kwargs: Any) -> Iterator[TicketItem]:
        page_token: str | None = None
        while True:
            page = self.tickets(product_id=product_id, page_token=page_token, **kwargs)
            yield from page.items
            if not page.page_info or not page.page_info.next_page_token:
                break
            page_token = page.page_info.next_page_token

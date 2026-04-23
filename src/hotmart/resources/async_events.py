from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

from .._base_client import _build_params
from ..models.events import EventItem, TicketItem
from ..models.pagination import PaginatedResponse
from ._async_base import AsyncAPIResource


class AsyncEvents(AsyncAPIResource):

    async def get(self, event_id: str, **kwargs: Any) -> EventItem | None:
        return await self._get(f"/events/{event_id}", cast_to=EventItem)

    async def tickets(
        self,
        *,
        product_id: int,
        max_results: int | None = None,
        page_token: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse[TicketItem]:
        params = _build_params(locals())
        return await self._get("/tickets", params=params, cast_to=PaginatedResponse[TicketItem])  # type: ignore[return-value]

    async def tickets_autopaginate(self, *, product_id: int, **kwargs: Any) -> AsyncIterator[TicketItem]:
        page_token: str | None = None
        while True:
            page = await self.tickets(product_id=product_id, page_token=page_token, **kwargs)
            for item in page.items:
                yield item
            if not page.page_info or not page.page_info.next_page_token:
                break
            page_token = page.page_info.next_page_token

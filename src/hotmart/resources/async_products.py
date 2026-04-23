from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

from .._base_client import _build_params
from ..models._enums import ProductFormat, ProductStatus
from ..models.pagination import PaginatedResponse
from ..models.products import OfferItem, PlanItem, ProductItem
from ._async_base import AsyncAPIResource


class AsyncProducts(AsyncAPIResource):

    async def list(
        self,
        *,
        id: int | None = None,
        status: ProductStatus | str | None = None,
        format: ProductFormat | str | None = None,
        max_results: int | None = None,
        page_token: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse[ProductItem]:
        params = _build_params(locals())
        return await self._get(  # type: ignore[return-value]
            "/products", api_domain="products", params=params, cast_to=PaginatedResponse[ProductItem]
        )

    async def list_autopaginate(self, **kwargs: Any) -> AsyncIterator[ProductItem]:
        page_token: str | None = None
        while True:
            page = await self.list(page_token=page_token, **kwargs)
            for item in page.items:
                yield item
            if not page.page_info or not page.page_info.next_page_token:
                break
            page_token = page.page_info.next_page_token

    async def offers(
        self,
        ucode: str,
        *,
        max_results: int | None = None,
        page_token: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse[OfferItem]:
        params = _build_params(locals())
        params.pop("ucode", None)
        return await self._get(  # type: ignore[return-value]
            f"/products/{ucode}/offers", api_domain="products", params=params, cast_to=PaginatedResponse[OfferItem]
        )

    async def offers_autopaginate(self, ucode: str, **kwargs: Any) -> AsyncIterator[OfferItem]:
        page_token: str | None = None
        while True:
            page = await self.offers(ucode, page_token=page_token, **kwargs)
            for item in page.items:
                yield item
            if not page.page_info or not page.page_info.next_page_token:
                break
            page_token = page.page_info.next_page_token

    async def plans(
        self,
        ucode: str,
        *,
        max_results: int | None = None,
        page_token: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse[PlanItem]:
        params = _build_params(locals())
        params.pop("ucode", None)
        return await self._get(  # type: ignore[return-value]
            f"/products/{ucode}/plans", api_domain="products", params=params, cast_to=PaginatedResponse[PlanItem]
        )

    async def plans_autopaginate(self, ucode: str, **kwargs: Any) -> AsyncIterator[PlanItem]:
        page_token: str | None = None
        while True:
            page = await self.plans(ucode, page_token=page_token, **kwargs)
            for item in page.items:
                yield item
            if not page.page_info or not page.page_info.next_page_token:
                break
            page_token = page.page_info.next_page_token

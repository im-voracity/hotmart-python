from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from .._base_client import _build_params
from ..models._enums import ProductFormat, ProductStatus
from ..models.pagination import PaginatedResponse
from ..models.products import OfferItem, PlanItem, ProductItem
from ._base import APIResource


class Products(APIResource):

    def list(
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
        return self._get("/products", api_domain="products", params=params, cast_to=PaginatedResponse[ProductItem])  # type: ignore[return-value]

    def list_autopaginate(self, **kwargs: Any) -> Iterator[ProductItem]:
        page_token: str | None = None
        while True:
            page = self.list(page_token=page_token, **kwargs)
            yield from page.items
            if not page.page_info or not page.page_info.next_page_token:
                break
            page_token = page.page_info.next_page_token

    def offers(
        self,
        ucode: str,
        *,
        max_results: int | None = None,
        page_token: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse[OfferItem]:
        params = _build_params(locals())
        params.pop("ucode", None)
        return self._get(  # type: ignore[return-value]
            f"/products/{ucode}/offers", api_domain="products", params=params, cast_to=PaginatedResponse[OfferItem]
        )

    def offers_autopaginate(self, ucode: str, **kwargs: Any) -> Iterator[OfferItem]:
        page_token: str | None = None
        while True:
            page = self.offers(ucode, page_token=page_token, **kwargs)
            yield from page.items
            if not page.page_info or not page.page_info.next_page_token:
                break
            page_token = page.page_info.next_page_token

    def plans(
        self,
        ucode: str,
        *,
        max_results: int | None = None,
        page_token: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse[PlanItem]:
        params = _build_params(locals())
        params.pop("ucode", None)
        return self._get(  # type: ignore[return-value]
            f"/products/{ucode}/plans", api_domain="products", params=params, cast_to=PaginatedResponse[PlanItem]
        )

    def plans_autopaginate(self, ucode: str, **kwargs: Any) -> Iterator[PlanItem]:
        page_token: str | None = None
        while True:
            page = self.plans(ucode, page_token=page_token, **kwargs)
            yield from page.items
            if not page.page_info or not page.page_info.next_page_token:
                break
            page_token = page.page_info.next_page_token

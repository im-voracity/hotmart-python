from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

from ..models.coupons import CouponItem
from ..models.pagination import PaginatedResponse
from ._async_base import AsyncAPIResource


class AsyncCoupons(AsyncAPIResource):

    async def create(self, product_id: str, coupon_code: str, discount: float) -> None:
        await self._post(f"/product/{product_id}/coupon", json={"code": coupon_code, "discount": discount})

    async def list(
        self,
        product_id: str,
        *,
        code: str | None = None,
        page_token: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse[CouponItem]:
        params: dict[str, Any] = {}
        if code is not None:
            params["code"] = code
        if page_token is not None:
            params["page_token"] = page_token
        params.update(kwargs)
        return await self._get(f"/coupon/product/{product_id}", params=params, cast_to=PaginatedResponse[CouponItem])  # type: ignore[return-value]

    async def list_autopaginate(self, product_id: str, **kwargs: Any) -> AsyncIterator[CouponItem]:
        page_token: str | None = None
        while True:
            page = await self.list(product_id, page_token=page_token, **kwargs)
            for item in page.items:
                yield item
            if not page.page_info or not page.page_info.next_page_token:
                break
            page_token = page.page_info.next_page_token

    async def delete(self, coupon_id: str) -> None:
        await self._delete(f"/coupon/{coupon_id}")

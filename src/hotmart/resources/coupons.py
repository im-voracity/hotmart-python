from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from ..models.coupons import CouponItem
from ..models.pagination import PaginatedResponse
from ._base import APIResource


class Coupons(APIResource):

    def create(self, product_id: str, coupon_code: str, discount: float) -> None:
        self._post(f"/product/{product_id}/coupon", json={"code": coupon_code, "discount": discount})

    def list(
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
        return self._get(f"/coupon/product/{product_id}", params=params, cast_to=PaginatedResponse[CouponItem])  # type: ignore[return-value]

    def list_autopaginate(self, product_id: str, **kwargs: Any) -> Iterator[CouponItem]:
        page_token: str | None = None
        while True:
            page = self.list(product_id, page_token=page_token, **kwargs)
            yield from page.items
            if not page.page_info or not page.page_info.next_page_token:
                break
            page_token = page.page_info.next_page_token

    def delete(self, coupon_id: str) -> None:
        self._delete(f"/coupon/{coupon_id}")

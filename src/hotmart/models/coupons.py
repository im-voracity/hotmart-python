from __future__ import annotations
from ._common import _Base


class CouponItem(_Base):
    id: str | None = None
    code: str | None = None
    discount: float | None = None
    product_id: str | None = None

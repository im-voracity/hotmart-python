from __future__ import annotations
from pydantic import BaseModel, ConfigDict


class _Base(BaseModel):
    model_config = ConfigDict(extra="allow")


class Price(_Base):
    value: float | None = None
    currency_code: str | None = None


class PageInfo(_Base):
    total_results: int | None = None
    next_page_token: str | None = None
    prev_page_token: str | None = None
    results_per_page: int | None = None

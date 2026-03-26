from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

from ._common import PageInfo

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(extra="allow")
    items: list[T] = []
    page_info: PageInfo | None = None

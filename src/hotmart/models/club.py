from __future__ import annotations

from ._common import _Base


class ModuleItem(_Base):
    module_id: str | None = None
    name: str | None = None
    sequence: int | None = None
    is_extra: bool | None = None
    is_extra_paid: bool | None = None
    is_public: bool | None = None
    classes: list[str] = []
    total_pages: int | None = None


class PageItem(_Base):
    """Members Area lesson/page. Fields vary — extra="allow" captures all."""


class StudentItem(_Base):
    """Members Area student. Fields vary — extra="allow" captures all."""


class StudentProgress(_Base):
    """Student progress data. Fields vary — extra="allow" captures all."""

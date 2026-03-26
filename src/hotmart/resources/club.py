from __future__ import annotations
from typing import Any
from ._base import APIResource
from ..models.club import ModuleItem, PageItem, StudentItem, StudentProgress


class Club(APIResource):

    def modules(self, subdomain: str, *, is_extra: bool | None = None, **kwargs: Any) -> list[ModuleItem]:
        """Return list of modules for the given subdomain.

        Retorna lista de módulos para o subdomínio informado.
        """
        params: dict[str, Any] = {"subdomain": subdomain}
        if is_extra is not None:
            params["is_extra"] = is_extra
        params.update(kwargs)
        data = self._get("/modules", api_domain="club", params=params)
        if not data:
            return []
        return [ModuleItem.model_validate(item) for item in data]

    def pages(self, subdomain: str, module_id: str, **kwargs: Any) -> list[PageItem]:
        """Return list of pages for the given module.

        Retorna lista de páginas para o módulo informado.
        """
        params: dict[str, Any] = {"subdomain": subdomain, "module_id": module_id, **kwargs}
        data = self._get("/pages", api_domain="club", params=params)
        if not data:
            return []
        return [PageItem.model_validate(item) for item in data]

    def students(self, subdomain: str, **kwargs: Any) -> list[StudentItem]:
        """Return list of students for the given subdomain.

        Retorna lista de alunos para o subdomínio informado.
        """
        params: dict[str, Any] = {"subdomain": subdomain, **kwargs}
        data = self._get("/students", api_domain="club", params=params)
        if not data:
            return []
        return [StudentItem.model_validate(item) for item in data]

    def student_progress(self, subdomain: str, *, student_email: str | None = None, **kwargs: Any) -> list[StudentProgress]:
        """Return progress data for students in the given subdomain.

        Retorna dados de progresso dos alunos no subdomínio informado.
        """
        params: dict[str, Any] = {"subdomain": subdomain}
        if student_email is not None:
            params["student_email"] = student_email
        params.update(kwargs)
        data = self._get("/students/progress", api_domain="club", params=params)
        if not data:
            return []
        return [StudentProgress.model_validate(item) for item in data]

# Contributing to hotmart-python

Thank you for your interest in contributing! This guide covers everything you need: development setup, running tests, coding standards, and how to add a new Hotmart API endpoint.

**Documentacao em Portugues disponivel em [CONTRIBUTING-ptBR.md](CONTRIBUTING-ptBR.md).**

---

## Table of Contents

- [Getting Started](#getting-started)
- [Running Tests](#running-tests)
- [Linting and Formatting](#linting-and-formatting)
- [Type Checking](#type-checking)
- [Code Style](#code-style)
- [How to Add a New Endpoint](#how-to-add-a-new-endpoint)
- [API Reference](#api-reference)
- [Pull Request Checklist](#pull-request-checklist)

---

## Getting Started

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

1. Fork and clone the repository:

```bash
git clone https://github.com/im-voracity/hotmart-python.git
cd hotmart-python
```

2. Install all dependencies (including dev dependencies):

```bash
uv sync
```

That is all. `uv` creates and manages the virtual environment automatically — no manual `venv` setup needed.

---

## Running Tests

```bash
uv run pytest tests/ --ignore=tests/test_integration.py
```

For verbose output with short tracebacks:

```bash
uv run pytest tests/ --ignore=tests/test_integration.py -v --tb=short
```

All unit tests use `respx` to mock HTTP — no real API calls, no credentials required.

### Integration tests

Integration tests run against the real Hotmart API. They are skipped automatically if credentials are not present:

```bash
# Requires HOTMART_CLIENT_ID, HOTMART_CLIENT_SECRET, HOTMART_BASIC in environment
set -a && source .env && set +a
uv run pytest tests/test_integration.py -v
```

See `.env.example` for the expected environment variables.

---

## Linting and Formatting

```bash
# Check for lint errors
uv run ruff check src/ tests/

# Auto-fix what can be fixed
uv run ruff check --fix src/ tests/

# Format
uv run ruff format src/ tests/

# Check format without modifying files
uv run ruff format --check src/ tests/
```

---

## Type Checking

```bash
uv run mypy src/hotmart/
```

The project runs `mypy --strict`. All public APIs must be fully annotated.

---

## Code Style

- **No nested `if` statements.** Use early returns and guard clauses instead.
- **Early returns first.** Validate inputs and handle error cases at the top of a function before the happy path.
- **Guard clauses.** Prefer `if not x: return` over `if x: <big block>`.
- **Docstrings in EN + PT-BR.** Every public method should have a brief English description followed by a Portuguese translation. See existing resource methods for the pattern.

**Preferred:**

```python
def my_method(self, value: str | None) -> str:
    if not value:
        return ""
    if len(value) > 100:
        raise ValueError("value too long")
    return value.strip()
```

**Not:**

```python
def my_method(self, value: str | None) -> str:
    if value:
        if len(value) <= 100:
            return value.strip()
    return ""
```

---

## How to Add a New Endpoint

### Step 1 — Identify the resource

Determine which resource group the endpoint belongs to (`sales`, `subscriptions`, `products`, `coupons`, `club`, `events`, or `negotiation`). If it belongs to a new group, create a new resource file following the existing patterns.

### Step 2 — Add or update the Pydantic model

Add the response model in `src/hotmart/models/`. Keep one file per resource group. Use `extra="allow"` on all models so new fields from the API do not break existing code:

```python
# src/hotmart/models/sales.py
from pydantic import BaseModel, ConfigDict

class MyNewModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    field_one: str
    field_two: int | None = None
```

Export the new model from `src/hotmart/models/__init__.py` and from `src/hotmart/__init__.py`.

### Step 3 — Add the method to the resource class

Add the method to the appropriate file in `src/hotmart/resources/`:

```python
# src/hotmart/resources/sales.py
def my_new_method(
    self,
    *,
    some_param: str | None = None,
    **kwargs: Any,
) -> PaginatedResponse[MyNewModel]:
    """Fetch my new resource.

    Busca o novo recurso.
    """
    params = _build_params(locals())
    return self._get("/my-endpoint", params=params, cast_to=PaginatedResponse[MyNewModel])  # type: ignore[return-value]
```

If the endpoint is paginated, also add an `*_autopaginate` variant following the existing pattern.

### Step 4 — Write tests

Add tests in `tests/resources/`. Follow the existing test patterns — mock `BaseSyncClient._request` and assert the correct URL and parameters are passed:

```python
# tests/resources/test_sales.py
def test_my_new_method(client, mock_paginated_response):
    with patch.object(client, "_request", return_value=mock_paginated_response) as mock_req:
        client.sales.my_new_method(some_param="value")
    mock_req.assert_called_once()
    _, kwargs = mock_req.call_args
    assert kwargs["params"]["some_param"] == "value"
```

### Step 5 — Update docs

Update `docs/README.md` and `docs/README-ptBR.md` to document the new method in the relevant resource section.

---

## API Reference

The file [`HOTMART-API-REFERENCE.md`](HOTMART-API-REFERENCE.md) contains a complete, machine-readable reference of all Hotmart API endpoints. It exists because the official Hotmart documentation is rendered as a JavaScript SPA and is not accessible to crawlers or AI agents.

If you are implementing a new endpoint, this file is your primary reference for request parameters, response shapes, and known quirks.

---

## Pull Request Checklist

Before submitting a PR, verify:

- [ ] `uv run pytest tests/ --ignore=tests/test_integration.py` passes with no failures
- [ ] `uv run ruff check src/ tests/` reports no errors
- [ ] `uv run ruff format --check src/ tests/` reports no changes needed
- [ ] `uv run mypy src/hotmart/` reports no errors
- [ ] New endpoint is covered by at least one test
- [ ] `docs/README.md` and `docs/README-ptBR.md` are updated if applicable

---

## License

By contributing to this project, you agree that your contributions will be licensed under the Apache License 2.0.

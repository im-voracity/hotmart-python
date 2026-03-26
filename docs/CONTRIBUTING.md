# Contributing to hotmart-python

Contributions are welcome. This guide covers the development setup, how to run the test suite, and how to add a new endpoint.

---

## Development Setup

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

That is all. No virtual environment setup needed — `uv` handles it.

---

## Running Tests

```bash
uv run pytest tests/
```

For verbose output with short tracebacks:

```bash
uv run pytest tests/ -v --tb=short
```

All tests use `unittest.mock` — no real HTTP calls are made. There are no sandbox or production credentials required to run the test suite.

---

## Linting

```bash
uv run ruff check src/ tests/
```

Fix auto-fixable issues:

```bash
uv run ruff check --fix src/ tests/
```

---

## Formatting

```bash
uv run ruff format src/ tests/
```

Check without modifying:

```bash
uv run ruff format --check src/ tests/
```

---

## Type Checking

```bash
uv run mypy src/hotmart/
```

---

## Code Style

- **No nested `if` statements.** Use early returns and guard clauses instead.
- **Early returns first.** Validate inputs and handle error cases at the top of a function before the happy path.
- **Guard clauses.** Prefer `if not x: return` over `if x: <big block>`.
- **Docstrings in EN + PT-BR.** Every public method should have a brief English description followed by the Portuguese translation. See existing resource methods for the pattern.

Example of preferred style:

```python
def my_method(self, value: str | None) -> str:
    if not value:
        return ""
    if len(value) > 100:
        raise ValueError("value too long")
    return value.strip()
```

Not:

```python
def my_method(self, value: str | None) -> str:
    if value:
        if len(value) <= 100:
            return value.strip()
    return ""
```

---

## How to Add a New Endpoint

Follow these steps to add a new Hotmart API endpoint to the SDK.

### Step 1 — Identify the resource

Determine which resource group the endpoint belongs to (sales, subscriptions, products, coupons, club, events, or negotiation). If it is a new group, create a new resource file.

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

If the endpoint is paginated, also add an `*_autopaginate` variant.

### Step 4 — Write tests

Add tests in `tests/`. Follow the existing test patterns — mock `BaseSyncClient._request` and assert the correct URL and parameters are passed.

```python
# tests/test_sales.py
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

## Pull Request Checklist

Before submitting a PR, verify:

- [ ] `uv run pytest tests/` passes with no failures
- [ ] `uv run ruff check src/ tests/` reports no errors
- [ ] `uv run ruff format --check src/ tests/` reports no changes needed
- [ ] `uv run mypy src/hotmart/` reports no errors
- [ ] New endpoint is covered by at least one test
- [ ] `docs/README.md` and `docs/README-ptBR.md` are updated if applicable

---

## License

By contributing to this project, you agree that your contributions will be licensed under the Apache License 2.0.

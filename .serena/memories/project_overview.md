# Hotmart Python SDK v1 Rewrite

## Purpose
Python SDK for the Hotmart API with TDD approach.

## Tech Stack
- Python 3.10+
- httpx >= 0.27, < 1 (HTTP client)
- pydantic >= 2.0, < 3 (data validation)
- pytest (testing)
- respx (mocking HTTP)
- mypy (type checking)
- ruff (linting/formatting)

## Code Structure
- `src/hotmart/` - Main SDK code
  - `_exceptions.py` - Custom exceptions (Task 3 done)
  - `_config.py` - Configuration (Task 2 done)
  - `_logging.py` - Logging setup (Task 4 done)
  - `_retry.py` - Retry logic (Task 5 in progress)
  - `_rate_limit.py` - Rate limiting (Task 6)
  - `_auth.py` - Authentication (Task 7)
  - `_base_client.py` - Base client (Task 8)
  - `models/` - Data models
  - `resources/` - API resources
- `tests/` - Test suite
- `docs/` - Documentation

## Key Commands
- Test: `uv run pytest tests/ -v`
- Single test: `uv run pytest tests/test_file.py -v`
- Format: `ruff format src/ tests/`
- Lint: `ruff check src/ tests/ --fix`
- Type check: `mypy src/`
- All checks: `ruff format && ruff check --fix && mypy src/ && pytest tests/`

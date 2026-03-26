# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.1] - 2026-03-26

### Changed

- Moved full README to repository root for correct rendering on GitHub and PyPI
- Rewrote README with features section, design principles, and improved DX documentation
- Added CONTRIBUTING.md (EN) and CONTRIBUTING-ptBR.md (PT-BR)
- Renamed `HOTMART_API.md` to `docs/HOTMART-API-REFERENCE.md`

---

## [1.0.0] - 2026-03-26

### Added

- Resource-based API: `client.sales`, `client.subscriptions`, `client.products`, `client.coupons`, `client.club`, `client.events`, `client.negotiation`
- All 27 Hotmart API endpoints across 7 resource groups
- Pydantic v2 models with `extra="allow"` for forward compatibility with new API fields
- Automatic token refresh with double-checked locking (thread-safe)
- Exponential backoff retry on transient errors (configurable `max_retries`, default 3)
- Proactive rate limit tracking (500 calls/min window)
- Structured logging with secret masking (`log_level` parameter)
- Pagination iterators: every paginated method has a matching `*_autopaginate` variant
- Sandbox mode via `sandbox=True` constructor flag
- Context manager support (`with Hotmart(...) as client:`)
- `**kwargs` passthrough for undocumented or future API parameters
- Full typed return values using Pydantic models
- Custom exception hierarchy: `HotmartError`, `AuthenticationError`, `BadRequestError`, `NotFoundError`, `RateLimitError`, `InternalServerError`, `APIStatusError`

### Changed

- Migrated HTTP client from `requests` to `httpx`
- Migrated project tooling from `poetry` to `uv` + `hatchling`
- Resource-based API replaces flat method names on the `Hotmart` class
- Import path changed from `hotmart_python` to `hotmart`
- `cancel_subscription` now takes a list of subscriber codes (bulk operation)
- Package name on PyPI remains `hotmart-python`

### Removed

- `enhance` parameter (all methods)
- `coloredlogs` dependency
- `@paginate` decorator (replaced by `*_autopaginate` methods)
- Flat class-level method names (`get_sales_history`, `get_subscriptions`, etc.)

---

## [0.5.0] - 2024-03-24

- Changed underlying request handling to always return a list of dicts
- Added `_handle_response` for standardized response output
- Added `@paginate` decorator for pagination
- Removed old `_paginate` method
- Fixed `subscriber_code` not passed correctly in `change_due_day`
- Enhanced type hints

## [0.4.1] - 2024-03-22

- Better error handling in `_make_request`
- Removed custom exceptions
- Updated tests

## [0.4.0] - 2024-03-21

- Added Discount Coupons endpoint
- Added sandbox code examples

## [0.3.0] - 2024-03-21

- Dropped Python <3.9 support
- Added flake8 linting and GitHub Actions

## [0.2.2] - 2024-03-21

- Refactored helper methods for error handling
- Fixed pagination output to return list of dicts

## [0.2.1] - 2024-03-20

- Added subscriptions endpoint
- Renamed `get_sales_users` to `get_sales_participants`
- Migrated to Poetry

## [0.1.20] - 2024

- Initial test releases

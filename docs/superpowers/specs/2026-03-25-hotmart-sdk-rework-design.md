# hotmart-python v1.0 — SDK Rework Design Spec

**Date:** 2026-03-25
**Status:** Approved
**Scope:** v1.0 (sync only — async planned for v1.x)

---

## Context

`hotmart-python` is a public Python library on PyPI with consistent downloads since its creation two years ago. The current v0.5.0 is a monolithic single-class client (~544 lines) with no type safety, no async, no retry logic, no rate limiting, and secrets leaking into debug logs. It covers only 14 of 27 Hotmart API endpoints.

This spec describes a complete rewrite to v1.0: a modern, production-ready SDK covering all 27 endpoints, designed for the Python community with strong DX, full documentation in both English and Brazilian Portuguese, and a clean migration path from v0.x.

No backward compatibility is required at the code level. A migration guide will be provided.

---

## Goals

- Cover all 27 Hotmart API endpoints
- Resource-based API: `client.sales.history()`, `client.coupons.create()`
- Typed responses via Pydantic v2 with `extra="allow"` (resilient to API additions)
- `**kwargs` passthrough on every method for undocumented/future API params
- Built-in retry with exponential backoff
- Proactive rate limit handling
- Structured logging with complete secret masking
- Full documentation in EN + PT-BR
- Sync client in v1.0; async planned for v1.x

---

## Non-Goals

- Async support (v1.x)
- Webhook handling
- Backward compatibility with v0.x method signatures

---

## Package

- **Name:** `hotmart-python` (keep for SEO and PyPI continuity)
- **Import:** `from hotmart import Hotmart`
- **Python:** `>=3.10`
- **Build backend:** hatchling
- **Package manager:** uv

---

## Dependencies

**Runtime:**
- `httpx>=0.27,<1` — replaces `requests`; async-ready for v1.x without HTTP layer rewrite
- `pydantic>=2.0,<3` — typed models with `extra="allow"`

**Dev:**
- `pytest`, `respx`, `ruff`, `mypy`, `coverage`

**Dropped:**
- `requests`, `coloredlogs`, `flake8`, poetry

---

## Architecture

### Package Structure

```
src/
  hotmart/
    __init__.py          # exports: Hotmart, models, exceptions
    _client.py           # Hotmart class — composes all resource classes
    _base_client.py      # HTTP core: request orchestration
    _auth.py             # OAuth2 TokenManager (cache + proactive refresh)
    _config.py           # ClientConfig, URL maps (prod/sandbox, by domain)
    _exceptions.py       # HotmartError hierarchy
    _logging.py          # HotmartLogger — structured, secrets always masked
    _retry.py            # exponential backoff logic
    _rate_limit.py       # RateLimit-Remaining tracker
    resources/
      _base.py           # APIResource base class
      sales.py           # Sales (6 endpoints)
      subscriptions.py   # Subscriptions (8 endpoints)
      products.py        # Products (3 endpoints)
      coupons.py         # Coupons (3 endpoints)
      club.py            # Club (4 endpoints)
      events.py          # Events (2 endpoints)
      negotiation.py     # Negotiation (1 endpoint)
    models/
      __init__.py        # re-exports all models
      _enums.py          # StrEnum types
      _common.py         # Price, PageInfo (shared)
      pagination.py      # PaginatedResponse[T]
      sales.py
      subscriptions.py
      products.py
      coupons.py
      club.py
      events.py
      negotiation.py
tests/
  conftest.py
  test_auth.py
  test_retry.py
  test_rate_limit.py
  test_logging.py
  test_exceptions.py
  test_client.py
  resources/
    test_sales.py
    test_subscriptions.py
    test_products.py
    test_coupons.py
    test_club.py
    test_events.py
    test_negotiation.py
docs/
  README.md              # EN — complete usage guide
  README-ptBR.md         # PT-BR — complete, not a shallow translation
  MIGRATION.md           # v0.x → v1.0 side-by-side examples
  CHANGELOG.md           # Keep a Changelog format (https://keepachangelog.com)
  CONTRIBUTING.md
  SANDBOX-GUIDE.md
```

---

## Authentication

### Credentials

Hotmart provides three values in the dashboard (Tools → Developer Tools → Credentials):
- `client_id`
- `client_secret`
- `basic` — pre-encoded value in the form `"Basic <base64(client_id:client_secret)>"`, provided directly by Hotmart

The SDK accepts `basic` as-is. Callers copy it from the dashboard — no encoding step required.

### OAuth2 Flow (`_auth.py`)

```
POST https://api-sec-vlc.hotmart.com/security/oauth/token
Authorization: <basic>
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&client_id=...&client_secret=...
```

Response: `{"access_token": "...", "token_type": "bearer", "expires_in": 86400}`

Token is valid for **86400 seconds (24 hours)**. The TokenManager:
- Caches the token in memory
- Proactively refreshes **300 seconds (5 minutes) before expiry**
- Uses `threading.Lock` with **double-checked locking** to prevent thundering herd under concurrent requests
- The token value **never** appears in logs or exceptions at any level

### 401 vs 403

- **401** (`token_expired`, `invalid_token`): token issue — trigger a token refresh and retry the request **once**. If it fails again, raise `AuthenticationError`.
- **403** (`unauthorized_client`): permanent permission denial — raise `AuthenticationError` immediately, no retry.

---

## Base URLs

| Environment | Payments | Club | Products |
|-------------|----------|------|----------|
| Production  | `https://developers.hotmart.com/payments/api/v1` | `https://developers.hotmart.com/club/api/v1` | `https://developers.hotmart.com/products/api/v1` |
| Sandbox     | `https://sandbox.hotmart.com/payments/api/v1` | `https://sandbox.hotmart.com/club/api/v1` | `https://sandbox.hotmart.com/products/api/v1` |

---

## Rate Limits

Hotmart allows **500 calls per minute**. Response headers on every request:

| Header | Description |
|--------|-------------|
| `RateLimit-Limit` | Total calls per minute |
| `RateLimit-Remaining` | Remaining calls in current window |
| `RateLimit-Reset` | Seconds until quota resets |
| `X-RateLimit-Remaining-Minute` | Alternative remaining header |

`_rate_limit.py` reads `RateLimit-Remaining` and `RateLimit-Reset`. When remaining reaches 0, sleeps until reset — preventing 429s proactively.

---

## Pagination

Hotmart uses cursor-based pagination.

**Request params:** `max_results` (int), `page_token` (string)

**Response envelope:**
```json
{
  "items": [...],
  "page_info": {
    "total_results": 95,
    "next_page_token": "eyJyb3...",
    "prev_page_token": "eyJyb3...",
    "results_per_page": 50
  }
}
```

`PaginatedResponse[T]` maps this shape exactly. The `_autopaginate` suffix is the convention for all paginated endpoints — it returns an `Iterator[T]` that follows `next_page_token` until exhausted.

---

## Key Components

### `_config.py`

```python
@dataclass
class ClientConfig:
    client_id: str
    client_secret: str
    basic: str
    sandbox: bool = False
    max_retries: int = 3     # 0 = raise immediately on retryable errors
    timeout: float = 30.0
    log_level: int = logging.WARNING
```

### `_logging.py` — HotmartLogger

Masks `authorization`, `basic`, `client_secret`, `access_token` keys at every log level before writing. The fixed key list is the masking scope — caller `**kwargs` keys are not masked (by design: callers control their own params).

| Level   | Event             | Key Fields                               |
|---------|-------------------|------------------------------------------|
| INFO    | Request sent      | request_id, method, url                  |
| INFO    | Response received | request_id, status_code, duration_ms     |
| DEBUG   | Request params    | sanitized (fixed sensitive keys masked)  |
| DEBUG   | Token refresh     | cached: bool — never the value           |
| DEBUG   | Response body     | truncated snippet                        |
| WARNING | Retry attempt     | attempt, max_retries, delay, status_code |
| WARNING | Rate limit        | remaining, reset_at                      |
| ERROR   | API error         | status_code, error_type, request_id      |

User configuration via standard Python logging:
```python
logging.getLogger("hotmart").setLevel(logging.DEBUG)
# or:
client = Hotmart(..., log_level=logging.INFO)
```

### `_exceptions.py`

```
HotmartError(Exception)
├── AuthenticationError    (401/403)
├── BadRequestError        (400)
├── NotFoundError          (404)
├── RateLimitError         (429 — includes retry_after: float)
├── InternalServerError    (500/502/503)
└── APIStatusError         (generic — status_code + body)
```

All exceptions sanitize sensitive data in `__str__` and `__repr__`.

### `_retry.py`

- Retries on: 429, 500, 502, 503, connection errors, timeouts
- 401: refresh token, retry once (see auth section)
- 403: no retry
- Strategy: `0.5 × 2^attempt` + jitter, capped at 30s
- Respects `RateLimit-Reset` header when present
- `max_retries=0`: raises immediately on any retryable error (no retry loop)

### `_base_client.py` — Request Pipeline

```
generate request_id (UUID4)
→ get token (TokenManager — double-checked lock)
→ check rate limit (sleep if remaining=0)
→ httpx call (timeout always set, SSL always on)
→ log request + response
→ update rate limit state
→ on error: retry with backoff OR refresh-and-retry (401) OR raise typed exception
→ deserialize via cast_to= (Pydantic model or None)
```

**Connection pooling:** `httpx.Client` maintains a connection pool. When used as a context manager (`with Hotmart(...) as client`), the pool closes on exit. When used without a context manager, the pool is left open (valid for long-lived use). Docs will recommend the context manager for scripts and the bare client for long-lived services.

### Resources — Method Pattern

```python
class Sales(APIResource):
    def history(
        self,
        *,
        product_id: int | None = None,
        buyer_name: str | None = None,
        buyer_email: str | None = None,
        transaction_status: PurchaseStatus | str | None = None,
        start_date: int | None = None,  # Unix ms epoch
        end_date: int | None = None,
        page_token: str | None = None,
        max_results: int | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse[SaleHistoryItem]:
        params = _build_params(locals())  # drops None and "self"
        return self._get("/sales/history", params=params,
                         cast_to=PaginatedResponse[SaleHistoryItem])

    def history_autopaginate(self, **kwargs: Any) -> Iterator[SaleHistoryItem]:
        page_token = None
        while True:
            page = self.history(page_token=page_token, **kwargs)
            yield from page.items
            if not page.page_info or not page.page_info.next_page_token:
                break
            page_token = page.page_info.next_page_token
```

Rules: guard clauses + early returns, no nested ifs, type hints on all functions.

---

## All 27 Endpoints

### Sales (`/payments/api/v1/sales/...`)

| Method | HTTP | Path | Paginated | Sandbox |
|--------|------|------|-----------|---------|
| `history` | GET | `/sales/history` | yes | yes |
| `summary` | GET | `/sales/summary` | yes | yes |
| `participants` | GET | `/sales/users` | yes | yes |
| `commissions` | GET | `/sales/commissions` | yes | yes |
| `price_details` | GET | `/sales/price/details` | yes | yes |
| `refund` | POST | `/sales/refund` | no | no |

### Subscriptions (`/payments/api/v1/subscriptions/...`)

| Method | HTTP | Path | Paginated | Sandbox |
|--------|------|------|-----------|---------|
| `list` | GET | `/subscriptions` | yes | yes |
| `summary` | GET | `/subscriptions/summary` | no | no |
| `purchases` | GET | `/subscriptions/{subscriber_code}/purchases` | yes | no |
| `transactions` | GET | `/subscriptions/{subscriber_code}/transactions` | no | no |
| `cancel` | POST | `/subscriptions/cancel` | no | no |
| `reactivate` | POST | `/subscriptions/reactivate` | no | no |
| `reactivate_single` | POST | `/subscriptions/{subscriber_code}/reactivate` | no | no |
| `change_due_day` | PATCH | `/subscriptions/{subscriber_code}` | no | no |

### Products (`/products/api/v1/...`)

| Method | HTTP | Path | Paginated | Sandbox |
|--------|------|------|-----------|---------|
| `list` | GET | `/products` | yes | yes |
| `offers` | GET | `/products/{product_id}/offers` | yes | yes |
| `plans` | GET | `/products/{product_id}/plans` | yes | yes |

### Coupons (`/payments/api/v1/...`)

| Method | HTTP | Path | Paginated | Sandbox |
|--------|------|------|-----------|---------|
| `create` | POST | `/product/{product_id}/coupon` | no | no |
| `list` | GET | `/coupon/product/{product_id}` | yes | no |
| `delete` | DELETE | `/coupon/{coupon_id}` | no | no |

### Club / Members Area (`/club/api/v1/...`)

| Method | HTTP | Path | Paginated | Sandbox |
|--------|------|------|-----------|---------|
| `modules` | GET | `/modules` | no (array) | yes |
| `pages` | GET | `/modules/{module_id}/pages` | no (array) | yes |
| `students` | GET | `/students` | no (array) | yes |
| `student_progress` | GET | `/students/{student_id}/progress` | no (array) | yes |

### Events (`/payments/api/v1/...`)

| Method | HTTP | Path | Paginated | Sandbox |
|--------|------|------|-----------|---------|
| `get` | GET | `/events` | no | no |
| `tickets` | GET | `/events/{event_id}/tickets` | yes | no |

### Negotiation (`/payments/api/v1/...`)

| Method | HTTP | Path | Paginated | Sandbox |
|--------|------|------|-----------|---------|
| `create` | POST | `/installments/negotiation` | no | no |

---

## Models

```python
# All models
class SaleHistoryItem(BaseModel):
    model_config = ConfigDict(extra="allow")
    # Fields from HOTMART_API.md response shapes — all Optional with None defaults

# Shared
class Price(BaseModel):
    model_config = ConfigDict(extra="allow")
    value: float | None = None
    currency_code: str | None = None

class PageInfo(BaseModel):
    model_config = ConfigDict(extra="allow")
    total_results: int | None = None
    next_page_token: str | None = None
    prev_page_token: str | None = None
    results_per_page: int | None = None

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T] = []
    page_info: PageInfo | None = None
```

Dates are `int` (Unix ms epoch) matching the API format. Models are populated from `HOTMART_API.md` response examples for each endpoint.

---

## Enums

`StrEnum` — accepted as typed or raw string values:

```python
class PurchaseStatus(StrEnum):
    APPROVED = "APPROVED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"
    BLOCKED = "BLOCKED"
    UNDER_ANALISYS = "UNDER_ANALISYS"
    COMPLETE = "COMPLETE"
    EXPIRED = "EXPIRED"
    NO_FUNDS = "NO_FUNDS"
    OVERDUE = "OVERDUE"
    PRINTED = "PRINTED"
    STARTED = "STARTED"
    WAITING_PAYMENT = "WAITING_PAYMENT"
    PRE_ORDER = "PRE_ORDER"
    CHARGEBACK = "CHARGEBACK"

class PaymentType(StrEnum):
    BILLET = "BILLET"
    CREDIT_CARD = "CREDIT_CARD"
    PIX = "PIX"
    PAYPAL = "PAYPAL"
    DIRECT_BANK_TRANSFER = "DIRECT_BANK_TRANSFER"
    HYBRID = "HYBRID"
    WALLET = "WALLET"
    GOOGLE_PAY = "GOOGLE_PAY"
    SAMSUNG_PAY = "SAMSUNG_PAY"

class CommissionAs(StrEnum):
    PRODUCER = "PRODUCER"
    COPRODUCER = "COPRODUCER"
    AFFILIATE = "AFFILIATE"

class SubscriptionStatus(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DELAYED = "DELAYED"
    CANCELLED_BY_CUSTOMER = "CANCELLED_BY_CUSTOMER"
    CANCELLED_BY_SELLER = "CANCELLED_BY_SELLER"
    CANCELLED_BY_ADMIN = "CANCELLED_BY_ADMIN"

class ProductFormat(StrEnum):
    EBOOK = "EBOOK"
    ONLINE_COURSE = "ONLINE_COURSE"
    SERIAL_CONTENT = "SERIAL_CONTENT"
    MENTORING = "MENTORING"
    SOFTWARE = "SOFTWARE"
    COMMUNITY = "COMMUNITY"
    BUNDLE = "BUNDLE"
```

---

## Public API

```python
from hotmart import Hotmart

client = Hotmart(
    client_id="...",
    client_secret="...",
    basic="Basic ...",   # provided as-is from Hotmart dashboard
    sandbox=False,
    max_retries=3,
    timeout=30.0,
    log_level=logging.WARNING,
)

# Single page
sales = client.sales.history(buyer_name="Paula")
# → PaginatedResponse[SaleHistoryItem]

# Auto-paginate (Iterator[SaleHistoryItem])
for sale in client.sales.history_autopaginate(transaction_status="APPROVED"):
    print(sale.purchase.transaction)

# kwargs passthrough
sales = client.sales.history(buyer_name="Paula", new_param="value")

# Context manager (recommended for scripts)
with Hotmart(...) as client:
    products = client.products.list()
```

---

## Testing Strategy

- `respx` mocks `httpx` at transport level — no real server needed
- Every endpoint: happy path + 401, 403, 429, 500
- Auth: cache hit, cache miss, proactive refresh, 401-refresh-retry, thread safety
- Retry: 429 → backoff → success; max retries exceeded → `RateLimitError`; `max_retries=0` → raises immediately
- Logging: assert sensitive keys never appear in log output (any level)
- Pagination: autopaginate follows `next_page_token` until `page_info` has none

---

## Code Style

- No nested ifs — guard clauses and early returns throughout
- Type hints on all public and private functions
- Ruff for linting and formatting
- mypy for type checking

---

## Documentation

- `docs/README.md` — full EN usage guide
- `docs/README-ptBR.md` — full PT-BR guide (examples with PIX, boleto, planos de assinatura)
- `docs/MIGRATION.md` — v0.x → v1.0 side-by-side method mapping
- `docs/SANDBOX-GUIDE.md` — sandbox credentials setup + known unsupported endpoints
- `docs/CHANGELOG.md` — Keep a Changelog format

---

## Implementation Phases

Each phase ends with a **commit + push**.

| Phase | Deliverables |
|-------|-------------|
| 1 — Foundation | `pyproject.toml`, package skeleton, `_config.py`, `_exceptions.py`, `_logging.py` |
| 2 — HTTP Core | `_auth.py`, `_retry.py`, `_rate_limit.py`, `_base_client.py` + tests |
| 3 — Models | All Pydantic models + enums |
| 4 — Resources | All 7 resource files + tests (commit per resource) |
| 5 — Client + Exports | `_client.py`, `__init__.py`, `conftest.py`, remaining tests |
| 6 — Cleanup + Docs | Remove old files, write docs EN + PT-BR, MIGRATION.md |

---

## Security Checklist

- Secrets never appear in log output at any level
- Exception messages mask sensitive fields
- SSL/TLS always enabled — no option to disable
- No dangerous deserialization (pickle, unsafe yaml)
- No secrets in URL query params — all auth via headers
- httpx timeout always set — no infinite waits
- Rate limit handling prevents accidental API abuse

# hotmart-python — Python SDK for the Hotmart API

![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)
![PyPI version](https://img.shields.io/pypi/v/hotmart-python)
![License Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-green)

**hotmart-python** is a typed Python SDK for the [Hotmart API](https://developers.hotmart.com/docs/en/).
[Hotmart](https://www.hotmart.com) is a Brazilian digital products platform for selling courses, ebooks, subscriptions, and memberships — supporting payments via PIX, boleto, credit/debit card, and PayPal.

This SDK handles OAuth, token refresh, retries, rate limits, and pagination automatically. You write business logic; the SDK handles the API.

**Documentação em Português disponível em [README-ptBR.md](docs/README-ptBR.md).**

---

> **v1.0 — rewrite completo.** Após dois anos sem atualizações, a biblioteca foi redesenhada do zero: API resource-based, `httpx`, Pydantic v2, retry automático, tipagem estrita e muito mais. É um breaking change forte em relação à v0.x — veja o [guia de migração](docs/MIGRATION.md) para atualizar. Se você está começando agora, pode ignorar esse aviso.

---

## Features

- **Fully typed responses** — every API response is a Pydantic v2 model. Your IDE completes field names; no raw dicts, no guessing.
- **Autopaginate iterators** — every paginated endpoint ships a `*_autopaginate` variant that transparently walks all pages. One `for` loop, all records.
- **Automatic token management** — OAuth token is acquired, cached, and proactively refreshed 5 minutes before expiry. Thread-safe with double-checked locking.
- **Retry with exponential backoff** — transient errors (5xx, 429) are retried automatically with jitter and `RateLimit-Reset` awareness. Configurable via `max_retries`.
- **Proactive rate limit tracking** — monitors remaining requests per window and backs off before hitting the limit.
- **Clean exception hierarchy** — catch only what you care about: `AuthenticationError`, `RateLimitError`, `NotFoundError`, `BadRequestError`, and more.
- **httpx under the hood** — persistent connection pool, configurable timeouts, context manager support.
- **Forward-compatible kwargs** — extra `**kwargs` are passed directly as query params, so you can use undocumented or newly added Hotmart parameters without waiting for an SDK update.

---

## Design Principles

- **One object, all resources.** Instantiate `Hotmart` once and access every resource group as an attribute: `client.sales`, `client.subscriptions`, `client.products`, etc.
- **Fail loudly.** Errors are typed exceptions, never silently swallowed or buried in return values.
- **No boilerplate.** Authentication, pagination, retries, and connection management are invisible by default. Opt in to configuration only when you need it.
- **Strict typing.** `mypy --strict` passes. All public APIs are fully annotated. Models use `extra="allow"` so new API fields don't break your code.

---

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Authentication](#authentication)
- [Resources](#resources)
  - [Sales](#sales)
  - [Subscriptions](#subscriptions)
  - [Products](#products)
  - [Coupons](#coupons)
  - [Club (Members Area)](#club-members-area)
  - [Events](#events)
  - [Negotiation](#negotiation)
- [Pagination](#pagination)
- [Sandbox Mode](#sandbox-mode)
- [Error Handling](#error-handling)
- [Logging](#logging)
- [Context Manager](#context-manager)
- [Extra Parameters (kwargs)](#extra-parameters-kwargs)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## Installation

```bash
pip install hotmart-python
```

Or with [uv](https://github.com/astral-sh/uv):

```bash
uv add hotmart-python
```

**Requirements:** Python 3.11+

---

## Quick Start

```python
from hotmart import Hotmart

client = Hotmart(
    client_id="your_client_id",
    client_secret="your_client_secret",
    basic="Basic your_base64_credentials",
)

# Single page
page = client.sales.history(buyer_name="Paula")
for sale in page.items:
    print(sale.purchase.transaction, sale.buyer.email)

# All pages — one iterator, no manual pagination
for sale in client.sales.history_autopaginate(transaction_status="APPROVED"):
    print(sale.purchase.transaction)
```

---

## Authentication

Hotmart uses **OAuth 2.0 Client Credentials**. The SDK handles token acquisition and refresh automatically — you only need to supply three values at startup.

### Where to find your credentials

1. Log in to [Hotmart](https://app.hotmart.com).
2. Go to **Tools → Developer Tools → Credentials**.
3. Generate a new credential set. You will receive:
   - `client_id` — your application client ID
   - `client_secret` — your application client secret
   - `basic` — the Base64-encoded `client_id:client_secret` string prefixed with `Basic ` (Hotmart shows this value directly in the dashboard)

```python
from hotmart import Hotmart

client = Hotmart(
    client_id="abcdef12-1234-5678-abcd-abcdef123456",
    client_secret="your_secret_here",
    basic="Basic YWJjZGVmMTItMTIzNC01Njc4LWFiY2QtYWJjZGVmMTIzNDU2OnlvdXJfc2VjcmV0X2hlcmU=",
)
```

Tokens are valid for 24 hours. The SDK caches the token and proactively refreshes it 5 minutes before expiry using double-checked locking, so concurrent requests never race on token renewal.

---

## Resources

### Sales

```python
# Single page
page = client.sales.history(buyer_name="Paula", transaction_status="APPROVED")
page = client.sales.summary(start_date=1700000000000, end_date=1710000000000)
page = client.sales.participants(buyer_email="paula@example.com")
page = client.sales.commissions(commission_as="PRODUCER")
page = client.sales.price_details(product_id=1234567)

# Refund a transaction
client.sales.refund("HP17715690036014")

# Autopaginate — iterates all pages automatically
for sale in client.sales.history_autopaginate(buyer_name="Paula"):
    print(sale.purchase.transaction)
```

| Method | Description |
|--------|-------------|
| `history(**kwargs)` | List all sales with detailed information |
| `history_autopaginate(**kwargs)` | Iterator over all pages |
| `summary(**kwargs)` | Total commission values per currency |
| `summary_autopaginate(**kwargs)` | Iterator over all pages |
| `participants(**kwargs)` | Sales user/participant data |
| `participants_autopaginate(**kwargs)` | Iterator over all pages |
| `commissions(**kwargs)` | Commission breakdown per sale |
| `commissions_autopaginate(**kwargs)` | Iterator over all pages |
| `price_details(**kwargs)` | Price and fee details per sale |
| `price_details_autopaginate(**kwargs)` | Iterator over all pages |
| `refund(transaction_code)` | Request a refund for a transaction |

---

### Subscriptions

```python
# List subscribers
page = client.subscriptions.list(status="ACTIVE", product_id=1234567)

# Summary
page = client.subscriptions.summary()

# Purchases and transactions for a single subscriber
purchases = client.subscriptions.purchases("SUB-ABC123")
transactions = client.subscriptions.transactions("SUB-ABC123")

# Cancel one or more subscriptions
result = client.subscriptions.cancel(["SUB-ABC123", "SUB-DEF456"], send_mail=True)

# Reactivate subscriptions (bulk)
result = client.subscriptions.reactivate(["SUB-ABC123"], charge=False)

# Reactivate a single subscription
result = client.subscriptions.reactivate_single("SUB-ABC123", charge=True)

# Change billing due day
client.subscriptions.change_due_day("SUB-ABC123", due_day=15)

# Autopaginate
for sub in client.subscriptions.list_autopaginate(status="ACTIVE"):
    print(sub.subscriber_code)
```

| Method | Description |
|--------|-------------|
| `list(**kwargs)` | List subscriptions with filters |
| `list_autopaginate(**kwargs)` | Iterator over all pages |
| `summary(**kwargs)` | Subscription summary |
| `summary_autopaginate(**kwargs)` | Iterator over all pages |
| `purchases(subscriber_code)` | Purchase history for a subscriber |
| `transactions(subscriber_code)` | Transactions for a subscriber |
| `cancel(subscriber_code, send_mail)` | Cancel one or more subscriptions |
| `reactivate(subscriber_code, charge)` | Reactivate subscriptions (bulk) |
| `reactivate_single(subscriber_code, charge)` | Reactivate a single subscription |
| `change_due_day(subscriber_code, due_day)` | Change the billing due day |

---

### Products

```python
# List products
page = client.products.list(status="ACTIVE")

# Offers for a product
page = client.products.offers("product-ucode-here")

# Plans for a product
page = client.products.plans("product-ucode-here")

# Autopaginate
for product in client.products.list_autopaginate():
    print(product.name)
```

| Method | Description |
|--------|-------------|
| `list(**kwargs)` | List all products |
| `list_autopaginate(**kwargs)` | Iterator over all pages |
| `offers(ucode, **kwargs)` | Offers for a product |
| `offers_autopaginate(ucode, **kwargs)` | Iterator over all pages |
| `plans(ucode, **kwargs)` | Plans for a product |
| `plans_autopaginate(ucode, **kwargs)` | Iterator over all pages |

---

### Coupons

```python
# Create a coupon (10% off) for product 1234567
client.coupons.create("1234567", "SUMMER10", discount=10.0)

# List coupons for a product
page = client.coupons.list("1234567")

# Delete a coupon by ID
client.coupons.delete("coupon-id-here")

# Autopaginate
for coupon in client.coupons.list_autopaginate("1234567"):
    print(coupon.code)
```

| Method | Description |
|--------|-------------|
| `create(product_id, coupon_code, discount)` | Create a discount coupon |
| `list(product_id, **kwargs)` | List coupons for a product |
| `list_autopaginate(product_id, **kwargs)` | Iterator over all pages |
| `delete(coupon_id)` | Delete a coupon |

---

### Club (Members Area)

The Club resource requires a `subdomain` argument — the subdomain of your Members Area.

```python
# Modules in the members area
modules = client.club.modules("my-course-subdomain")

# Pages within a module
pages = client.club.pages("my-course-subdomain", module_id="module-uuid")

# Students enrolled
students = client.club.students("my-course-subdomain")

# Student progress
progress = client.club.student_progress(
    "my-course-subdomain",
    student_email="student@example.com",
)
```

| Method | Description |
|--------|-------------|
| `modules(subdomain, **kwargs)` | List modules in the members area |
| `pages(subdomain, module_id, **kwargs)` | List pages in a module |
| `students(subdomain, **kwargs)` | List enrolled students |
| `student_progress(subdomain, **kwargs)` | Student progress data |

---

### Events

```python
# Get event details
event = client.events.get("event-id-here")

# List tickets for a product
page = client.events.tickets(product_id=1234567)

# Autopaginate
for ticket in client.events.tickets_autopaginate(product_id=1234567):
    print(ticket.name)
```

| Method | Description |
|--------|-------------|
| `get(event_id)` | Get event details |
| `tickets(product_id, **kwargs)` | List tickets for a product |
| `tickets_autopaginate(product_id, **kwargs)` | Iterator over all pages |

---

### Negotiation

```python
# Create an installment negotiation for a subscriber
result = client.negotiation.create("SUB-ABC123")
```

| Method | Description |
|--------|-------------|
| `create(subscriber_code)` | Create an installment negotiation |

---

## Pagination

The Hotmart API uses cursor-based pagination. Each paginated response contains a `page_info` object with `next_page_token`.

### Single-page call

Returns a `PaginatedResponse[T]` with `.items` and `.page_info`:

```python
page = client.sales.history(max_results=50)
print(f"Got {len(page.items)} items")
print(f"Next token: {page.page_info.next_page_token}")

# Manually fetch next page
next_page = client.sales.history(page_token=page.page_info.next_page_token)
```

### Autopaginate (recommended)

Every paginated method has a matching `*_autopaginate` variant that handles all page-fetching transparently:

```python
for sale in client.sales.history_autopaginate(buyer_name="Paula"):
    print(sale.purchase.transaction)
```

The iterator stops when there are no more pages — no token management, no loop conditions.

---

## Sandbox Mode

Use `sandbox=True` to point all requests at Hotmart's sandbox environment. Sandbox and production credentials are not interchangeable — generate sandbox credentials in the Hotmart dashboard under the same Developer Credentials section, selecting "Sandbox" as the environment.

```python
from hotmart import Hotmart

client = Hotmart(
    client_id="your_sandbox_client_id",
    client_secret="your_sandbox_client_secret",
    basic="Basic your_sandbox_base64_credentials",
    sandbox=True,
)
```

> **Note:** Some endpoints behave differently or are not fully supported in the sandbox. See [SANDBOX-GUIDE.md](docs/SANDBOX-GUIDE.md) and [HOTMART-API-BUGS.md](docs/HOTMART-API-BUGS.md) for known issues.

---

## Error Handling

All SDK errors inherit from `HotmartError`. Import and catch only the exceptions you need:

```python
from hotmart import (
    Hotmart,
    HotmartError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    BadRequestError,
    InternalServerError,
)

try:
    page = client.sales.history()
except AuthenticationError:
    print("Check your credentials.")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds.")
except NotFoundError:
    print("Resource not found.")
except HotmartError as e:
    print(f"API error: {e}")
```

Exception hierarchy:

| Exception | HTTP status | Meaning |
|-----------|------------|---------|
| `AuthenticationError` | 401, 403 | Invalid or missing credentials |
| `BadRequestError` | 400 | Invalid parameters |
| `NotFoundError` | 404 | Resource not found |
| `RateLimitError` | 429 | Rate limit exceeded (500 req/min) |
| `InternalServerError` | 500, 502, 503 | Hotmart server error |
| `APIStatusError` | other | Unexpected HTTP status |
| `HotmartError` | — | Base class for all SDK errors |

The SDK retries automatically on transient errors (5xx, 429) with exponential backoff (`0.5 × 2^attempt + jitter`, cap 30s). Configure via `max_retries`:

```python
client = Hotmart(..., max_retries=5)
```

---

## Logging

Logging is disabled by default. Enable it by passing `log_level` at construction time:

```python
import logging
from hotmart import Hotmart

client = Hotmart(
    client_id="...",
    client_secret="...",
    basic="Basic ...",
    log_level=logging.INFO,
)
```

| Level | What is logged |
|-------|---------------|
| `logging.DEBUG` | Request URLs, parameters — **contains sensitive data, avoid in production** |
| `logging.INFO` | High-level operation summaries |
| `logging.WARNING` | Warnings and unexpected conditions |
| `logging.ERROR` | Errors during API interactions |
| `logging.CRITICAL` | Critical failures |

Tokens and credentials are masked in all log output.

---

## Context Manager

`Hotmart` supports the context manager protocol for automatic cleanup of the underlying HTTP connection pool:

```python
from hotmart import Hotmart

with Hotmart(
    client_id="...",
    client_secret="...",
    basic="Basic ...",
) as client:
    for sale in client.sales.history_autopaginate():
        print(sale.purchase.transaction)
```

---

## Extra Parameters (kwargs)

All resource methods accept `**kwargs` and forward them directly to the API as query parameters. This lets you use undocumented or recently added Hotmart parameters without waiting for an SDK update:

```python
# Pass any query parameter Hotmart supports, even if not in the method signature
page = client.sales.history(some_new_param="value")
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [README-ptBR.md](docs/README-ptBR.md) | Esta documentação em Português |
| [MIGRATION.md](docs/MIGRATION.md) | Upgrading from v0.x to v1.0 — breaking changes and method mapping |
| [CHANGELOG.md](docs/CHANGELOG.md) | Full version history |
| [CONTRIBUTING.md](docs/CONTRIBUTING.md) | Development setup, code style, how to add endpoints |
| [SANDBOX-GUIDE.md](docs/SANDBOX-GUIDE.md) | Sandbox environment usage and known limitations |
| [HOTMART-API-BUGS.md](docs/HOTMART-API-BUGS.md) | Known Hotmart API bugs found during integration testing |
| [HOTMART-API-REFERENCE.md](docs/HOTMART-API-REFERENCE.md) | Complete API reference (agent/LLM-friendly — official docs are a JS SPA) |

---

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for setup, coding style, how to add a new endpoint, and the PR checklist.

---

## License

Apache License 2.0 — see [LICENSE.txt](LICENSE.txt) for details.

This package is not affiliated with or officially supported by Hotmart.

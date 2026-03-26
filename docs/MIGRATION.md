# Migration Guide: v0.x to v1.0

This guide covers the breaking changes introduced in v1.0 and shows how to update your code.

---

## Overview of Changes

v1.0 introduces a **resource-based API** that replaces the flat method names on the `Hotmart` class. All methods are now grouped under resource objects (`client.sales`, `client.subscriptions`, etc.).

The underlying HTTP client was also migrated from `requests` to `httpx`, and the project now uses `uv` + `hatchling` instead of `poetry`.

---

## Breaking Changes

### 1. Import path changed

```python
# v0.x
from hotmart_python import Hotmart

# v1.0
from hotmart import Hotmart
```

### 2. Resource-based method access

All methods moved from flat names on `Hotmart` to resource sub-objects:

```python
# v0.x
hotmart = Hotmart(client_id=..., client_secret=..., basic=...)
result = hotmart.get_sales_history()

# v1.0
client = Hotmart(client_id=..., client_secret=..., basic=...)
page = client.sales.history()
```

### 3. Return types are now typed Pydantic models

```python
# v0.x — returned a raw dict or list of dicts
result = hotmart.get_sales_history()
# result["items"][0]["buyer"]["name"]

# v1.0 — returns PaginatedResponse[SaleHistoryItem]
page = client.sales.history()
# page.items[0].buyer.name  (typed attribute access)
```

### 4. Pagination API changed

```python
# v0.x — used a @paginate decorator
from hotmart_python.decorators import paginate

@paginate
def get_sales_history(*args, **kwargs):
    return hotmart.get_sales_history(*args, **kwargs)

results = get_sales_history()

# v1.0 — use *_autopaginate methods directly
for sale in client.sales.history_autopaginate():
    print(sale.purchase.transaction)
```

### 5. `enhance` parameter removed

The `enhance` parameter that some methods accepted in v0.x has been removed. There is no replacement — the typed models handle field normalization directly.

### 6. `coloredlogs` dependency removed

If your project depended on `coloredlogs` being installed as a transitive dependency, you will need to add it directly to your own dependencies.

---

## Method Name Mapping

| v0.x method | v1.0 equivalent |
|-------------|-----------------|
| `hotmart.get_sales_history(**kw)` | `client.sales.history(**kw)` |
| `hotmart.get_sales_summary(**kw)` | `client.sales.summary(**kw)` |
| `hotmart.get_sales_participants(**kw)` | `client.sales.participants(**kw)` |
| `hotmart.get_sales_commissions(**kw)` | `client.sales.commissions(**kw)` |
| `hotmart.get_sales_price_details(**kw)` | `client.sales.price_details(**kw)` |
| `hotmart.get_subscriptions(**kw)` | `client.subscriptions.list(**kw)` |
| `hotmart.get_subscription_summary(**kw)` | `client.subscriptions.summary(**kw)` |
| `hotmart.get_subscription_purchases(code, **kw)` | `client.subscriptions.purchases(code, **kw)` |
| `hotmart.cancel_subscription(code)` | `client.subscriptions.cancel([code])` |
| `hotmart.reactivate_and_charge_subscription(code)` | `client.subscriptions.reactivate_single(code, charge=True)` |
| `hotmart.change_due_day(code, day)` | `client.subscriptions.change_due_day(code, day)` |
| `hotmart.create_coupon(pid, code, disc)` | `client.coupons.create(pid, code, disc)` |
| `hotmart.get_coupon(pid)` | `client.coupons.list(pid)` |
| `hotmart.delete_coupon(cid)` | `client.coupons.delete(cid)` |

---

## New in v1.0 (no v0.x equivalent)

These resources and methods are new in v1.0:

- `client.products.list()` / `offers()` / `plans()`
- `client.club.modules()` / `pages()` / `students()` / `student_progress()`
- `client.events.get()` / `tickets()`
- `client.negotiation.create()`
- `client.subscriptions.transactions(subscriber_code)`
- `client.subscriptions.reactivate(subscriber_codes)` (bulk)

---

## Before and After: Full Example

### v0.x

```python
from hotmart_python import Hotmart
from hotmart_python.decorators import paginate
import logging

hotmart = Hotmart(
    client_id="your_client_id",
    client_secret="your_client_secret",
    basic="your_basic_token",
    log_level=logging.INFO,
)

# Single page
result = hotmart.get_sales_history(buyer_email="paula@example.com")
for item in result:
    print(item["buyer"]["name"])

# Paginated
@paginate
def all_sales(*args, **kwargs):
    return hotmart.get_sales_history(*args, **kwargs)

for item in all_sales():
    print(item["buyer"]["name"])

# Cancel subscription
hotmart.cancel_subscription("SUB-ABC123")
```

### v1.0

```python
from hotmart import Hotmart
import logging

client = Hotmart(
    client_id="your_client_id",
    client_secret="your_client_secret",
    basic="Basic your_base64_credentials",
    log_level=logging.INFO,
)

# Single page
page = client.sales.history(buyer_email="paula@example.com")
for sale in page.items:
    print(sale.buyer.name)

# Autopaginate (replaces @paginate decorator)
for sale in client.sales.history_autopaginate():
    print(sale.buyer.name)

# Cancel subscription (now takes a list)
client.subscriptions.cancel(["SUB-ABC123"])
```

---

## Notes on `**kwargs`

The `**kwargs` passthrough still works in v1.0. Any extra keyword argument you pass to a method is forwarded to the API as a query parameter:

```python
# This still works — undocumented params are passed through
page = client.sales.history(some_extra_param="value")
```

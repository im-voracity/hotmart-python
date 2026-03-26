# Sandbox Guide

The Hotmart API provides a sandbox environment for testing your integration without affecting production data. All sandbox data is fictional.

---

## Getting Sandbox Credentials

Sandbox credentials are separate from production credentials and must be generated specifically for the sandbox environment.

1. Log in to [Hotmart](https://app.hotmart.com).
2. Go to **Tools → Developer Tools → Credentials**.
3. Click to generate a new credential set and select **Sandbox** as the environment.
4. You will receive a separate set of `client_id`, `client_secret`, and `basic` values for sandbox.

These credentials only work against the sandbox base URL (`sandbox.hotmart.com`). Do not use production credentials with `sandbox=True` or vice versa.

---

## Enabling Sandbox Mode

Pass `sandbox=True` when constructing the client:

```python
from hotmart import Hotmart

client = Hotmart(
    client_id="your_sandbox_client_id",
    client_secret="your_sandbox_client_secret",
    basic="Basic your_sandbox_base64_credentials",
    sandbox=True,
)

# All requests now go to sandbox.hotmart.com
page = client.sales.history()
```

When `sandbox=True`, the SDK replaces `developers.hotmart.com` with `sandbox.hotmart.com` across all API domains (payments, club, products).

---

## Endpoint Behavior in Sandbox

Most read endpoints (GET) work as expected in sandbox and return fictional data. The following endpoints have known issues in the sandbox environment and may return `404 Not Found` or `500 Internal Server Error`:

### Subscriptions

| Method | Sandbox status |
|--------|---------------|
| `subscriptions.list()` | Works |
| `subscriptions.summary()` | Works |
| `subscriptions.purchases(subscriber_code)` | May not work — 404 errors reported |
| `subscriptions.transactions(subscriber_code)` | May not work |
| `subscriptions.cancel(subscriber_code)` | May not work — 500 errors reported |
| `subscriptions.reactivate(subscriber_code)` | May not work |
| `subscriptions.reactivate_single(subscriber_code)` | May not work |
| `subscriptions.change_due_day(subscriber_code, day)` | May not work |

The sandbox API does provide some sample `subscriber_code` values in the API reference pages, but these do not reliably work as expected at the time of writing.

### Coupons

| Method | Sandbox status |
|--------|---------------|
| `coupons.list(product_id)` | May not work |
| `coupons.create(product_id, code, discount)` | May not work |
| `coupons.delete(coupon_id)` | May not work |

### Sales

| Method | Sandbox status |
|--------|---------------|
| `sales.history()` | Works |
| `sales.summary()` | Works |
| `sales.participants()` | Works |
| `sales.commissions()` | Works |
| `sales.price_details()` | Works |
| `sales.refund(transaction_code)` | Untested |

### Products / Club / Events / Negotiation

These endpoints have limited sandbox support. Behavior may vary.

---

## Known Issues

### `sandbox.hotmart.com` has no DNS record

During integration testing, we found that `sandbox.hotmart.com` does not resolve — the host has no DNS entry. This means all requests with `sandbox=True` will fail with a connection error at the DNS resolution stage, regardless of credentials.

This is a Hotmart infrastructure issue, not an SDK bug. It is documented in [`HOTMART-API-BUGS.md`](HOTMART-API-BUGS.md).

As a workaround, test against production with low-value or throwaway data, or use the SDK's unit test suite (which mocks all HTTP) to validate your integration logic.

---

## Tips for Sandbox Testing

- Use the `sales.history()` and `subscriptions.list()` endpoints to verify your authentication and basic connectivity.
- Do not rely on sandbox for write operation testing (cancel, reactivate, create coupon) — test the happy path in production with real but low-value data, or use mocks in your test suite.
- Sandbox errors are environmental — they do not indicate bugs in the SDK.

---

## Switching Between Environments

You can maintain two client instances:

```python
from hotmart import Hotmart

production_client = Hotmart(
    client_id="prod_client_id",
    client_secret="prod_client_secret",
    basic="Basic prod_base64",
)

sandbox_client = Hotmart(
    client_id="sandbox_client_id",
    client_secret="sandbox_client_secret",
    basic="Basic sandbox_base64",
    sandbox=True,
)
```

Never use production credentials with `sandbox=True` or sandbox credentials without `sandbox=True`.

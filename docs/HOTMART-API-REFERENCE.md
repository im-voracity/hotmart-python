# Hotmart API — Complete Reference for AI Agents

> **Source**: Scraped directly from https://developers.hotmart.com/docs/en/ on 2026-03-24.
> **Purpose**: AI-optimized reference for agents and LLMs that cannot access the official docs (Next.js/Gatsby SPA — HTML not returned by crawlers).
> **Official docs**: https://developers.hotmart.com/docs/en/
> **Library**: This file lives in the `hotmart-python` Python wrapper repository.

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Base URLs](#base-urls)
4. [Rate Limits](#rate-limits)
5. [Pagination](#pagination)
6. [HTTP Response Codes](#http-response-codes)
7. [Sandbox Environment](#sandbox-environment)
8. [API Groups](#api-groups)
   - [Sales](#sales)
   - [Subscriptions](#subscriptions)
   - [Products](#products)
   - [Discount Coupons](#discount-coupons)
   - [Members Area (Club)](#members-area-club)
   - [Event Tickets](#event-tickets)
   - [Installments Negotiation](#installments-negotiation)
9. [Webhooks](#webhooks)
10. [Enums & Value Reference](#enums--value-reference)

---

## Overview

Hotmart API is a REST API for creators and developers. All operations use HTTP verbs (GET, POST, PUT, PATCH, DELETE), and all responses are JSON. A sandbox environment is available for development.

**Two API domains:**
- `payments` — sales, subscriptions, coupons, refunds
- `club` — Members Area (students, modules, pages, progress)
- `products` — product catalog, offers, plans

---

## Authentication

Hotmart uses **OAuth 2.0 Client Credentials** flow.

### Step 1 — Get Credentials

In the Hotmart dashboard: **Tools → Developer Tools → Credentials**. Generate:
- `client_id`
- `client_secret`
- `basic` — Base64 encoded string `client_id:client_secret` prefixed with `Basic `

### Step 2 — Request Access Token

```
POST https://api-sec-vlc.hotmart.com/security/oauth/token
```

**Headers:**
```
Authorization: Basic <base64(client_id:client_secret)>
Content-Type: application/x-www-form-urlencoded
```

**Query Parameters:**
```
grant_type=client_credentials
client_id=<your_client_id>
client_secret=<your_client_secret>
```

**Response:**
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

> Token is valid for **86400 seconds (24 hours)**. Cache and reuse it.

### Step 3 — Use Token

All API requests must include:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

---

## Base URLs

| Environment | Payments API | Club API | Products API |
|-------------|-------------|----------|--------------|
| Production  | `https://developers.hotmart.com/payments/api/v1` | `https://developers.hotmart.com/club/api/v1` | `https://developers.hotmart.com/products/api/v1` |
| Sandbox     | `https://sandbox.hotmart.com/payments/api/v1` | `https://sandbox.hotmart.com/club/api/v1` | `https://sandbox.hotmart.com/products/api/v1` |

**Switch sandbox**: Change `developers.hotmart.com` → `sandbox.hotmart.com`. Credentials must be sandbox-specific.

---

## Rate Limits

- **Limit**: 500 calls per minute (reads + writes combined)
- **Response on exceeded**: HTTP 429 `too_many_requests`

**Rate Limit Headers returned on every response:**

| Header | Description |
|--------|-------------|
| `RateLimit-Limit` | Total calls allowed per minute |
| `RateLimit-Remaining` | Remaining calls in current window |
| `RateLimit-Reset` | Seconds until quota resets |
| `X-RateLimit-Limit-Minute` | Calls allowed per minute |
| `X-RateLimit-Remaining-Minute` | Remaining calls in current minute |

---

## Pagination

Hotmart uses **cursor-based pagination**.

**Request query parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `max_results` | integer | Max items per page |
| `page_token` | string | Cursor for the desired page |

**Response `page_info` object:**

```json
{
  "page_info": {
    "total_results": 95,
    "next_page_token": "eyJyb3dzIjo1LCJwYWdlIjozfQ==",
    "prev_page_token": "eyJyb3dzIjo1LCJwYWdlIjoxfQ==",
    "results_per_page": 50
  }
}
```

**Usage:** Pass `next_page_token` value as `page_token` in the next request to get the next page.

---

## HTTP Response Codes

| Status | Error Type | Meaning |
|--------|-----------|---------|
| 200 | — | Success |
| 201 | — | Resource created |
| 400 | `invalid_parameter`, `invalid_value_parameter`, `invalid_value_headers`, `invalid_token` | Bad request |
| 401 | `unauthorized`, `token_expired`, `invalid_token` | Authentication required |
| 403 | `unauthorized_client` | User lacks permission |
| 404 | `not_found` | URL not found |
| 429 | `too_many_requests` | Rate limit exceeded |
| 500 | `internal_server_error` | Unexpected server error |
| 502 | `internal_server_error` | Request timed out (>30s) |
| 503 | `internal_server_error` | API unavailable |

**Error response body:**
```json
{
  "error": "invalid_token",
  "error_description": "The page_token parameter is invalid"
}
```

---

## Sandbox Environment

- **Purpose**: Test integrations without affecting production data. All data is fictional.
- **Credentials**: Must be generated specifically for Sandbox inside Hotmart dashboard.
- **Base URL**: Replace `developers.hotmart.com` with `sandbox.hotmart.com`.
- **Note**: Some endpoints are not supported in sandbox (noted per endpoint below).

---

## API Groups

---

## Sales

All sales endpoints: `GET /payments/api/v1/sales/...`

> **Important**: Without `transaction` or `transaction_status` filters, endpoints only return `APPROVED` and `COMPLETE` statuses.

---

### GET /payments/api/v1/sales/history

**Description**: Lists all sales with detailed information. Use other endpoints for participants, commissions, and price breakdown.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `max_results` | integer | No | Max items per page |
| `page_token` | string | No | Pagination cursor |
| `product_id` | long | No | 7-digit product ID |
| `start_date` | long | No | Start date in milliseconds (Unix epoch ms) |
| `end_date` | long | No | End date in milliseconds |
| `sales_source` | string | No | SRC tracking code (e.g. from `pay.hotmart.com/B00000000T?src=campaignname`) |
| `transaction` | string | No | Transaction code (e.g. `HP17715690036014`) |
| `buyer_name` | string | No | Buyer's full name |
| `buyer_email` | string | No | Buyer's email |
| `transaction_status` | string | No | See [Purchase Statuses](#purchase-statuses) |
| `payment_type` | string | No | See [Payment Types](#payment-types) |
| `offer_code` | string | No | Product offer code |
| `commission_as` | string | No | `PRODUCER`, `COPRODUCER`, or `AFFILIATE` |

**Example cURL:**
```bash
curl --request GET \
  'https://developers.hotmart.com/payments/api/v1/sales/history?transaction_status=APPROVED' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer :access_token'
```

**Response `items[]` fields:**

```json
{
  "items": [
    {
      "product": {
        "name": "Product06",
        "id": 2125812
      },
      "buyer": {
        "name": "Ian Victor Baptista",
        "ucode": "839F1A4F-43DC-F60F-13FE-6C8BD23F6781",
        "email": "ian@teste.com"
      },
      "producer": {
        "name": "Bárbara Sebastiana Cardoso",
        "ucode": "252A74C5-4A97-143A-9349-E45D871C6018"
      },
      "purchase": {
        "transaction": "HP12455690122399",
        "order_date": 1622948400000,
        "approved_date": 1622948400000,
        "status": "UNDER_ANALISYS",
        "recurrency_number": 2,
        "is_subscription": false,
        "commission_as": "PRODUCER",
        "price": {
          "value": 235.76,
          "currency_code": "USD"
        },
        "payment": {
          "method": "BILLET",
          "installments_number": 1,
          "type": "BILLET"
        },
        "tracking": {
          "source_sck": "HOTMART_PRODUCT_PAGE",
          "source": "HOTMART",
          "external_code": "FD256D24-401C-7C93-284C-C5E0181CD5DB"
        },
        "warranty_expire_date": 1625022000000,
        "offer": {
          "payment_mode": "INVOICE",
          "code": "k2pasun0"
        },
        "hotmart_fee": {
          "total": 36.75,
          "fixed": 0,
          "currency_code": "EUR",
          "base": 11.12,
          "percentage": 9.9
        }
      }
    }
  ],
  "page_info": { "total_results": 14, "next_page_token": "...", "results_per_page": 5 }
}
```

**Sandbox**: ✅ Supported

---

### GET /payments/api/v1/sales/summary

**Description**: Displays total commission values per currency.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `max_results` | integer | No | Max items per page |
| `page_token` | string | No | Pagination cursor |
| `product_id` | long | No | 7-digit product ID |
| `start_date` | long | No | Start date (ms) |
| `end_date` | long | No | End date (ms) |
| `sales_source` | string | No | SRC tracking code |
| `affiliate_name` | string | No | Affiliate's name |
| `payment_type` | string | No | See [Payment Types](#payment-types) |
| `offer_code` | string | No | Offer code |
| `transaction` | string | No | Transaction code |
| `transaction_status` | string | No | See [Purchase Statuses](#purchase-statuses) |

**Response:**
```json
{
  "items": [
    {
      "total_items": 14,
      "total_value": {
        "value": 3290.64,
        "currency_code": "BRL"
      }
    }
  ],
  "page_info": { "total_results": 1, "results_per_page": 10 }
}
```

**Sandbox**: ✅ Supported

---

### GET /payments/api/v1/sales/users

**Description**: Lists participants (buyer, producer, affiliate, co-creator) for each sale with full contact/address details.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `max_results` | integer | No | Max items per page |
| `page_token` | string | No | Pagination cursor |
| `product_id` | long | No | 7-digit product ID |
| `start_date` | long | No | Start date (ms) |
| `end_date` | long | No | End date (ms) |
| `buyer_email` | string | No | Buyer email |
| `buyer_name` | string | No | Buyer name |
| `sales_source` | string | No | SRC tracking code |
| `transaction` | string | No | Transaction code |
| `affiliate_name` | string | No | Affiliate name |
| `commission_as` | string | No | `PRODUCER`, `COPRODUCER`, `AFFILIATE` |
| `transaction_status` | string | No | See [Purchase Statuses](#purchase-statuses) |

**Response:**
```json
{
  "items": [
    {
      "transaction": "HP10014546320130",
      "product": { "name": "Product 1", "id": 178598 },
      "users": [
        {
          "role": "PRODUCER",
          "user": {
            "ucode": "c9e5e3f4-097e-11e4-be45-22000b409f8a",
            "locale": "FR",
            "name": "Producer Name",
            "trade_name": "Producer Trade Name",
            "cellphone": "1199999999",
            "phone": "6825565681",
            "email": "producerEmail@email.com",
            "documents": [
              { "value": "564654", "type": "DOCUMENT" },
              { "value": "68658197646", "type": "CPF" }
            ],
            "address": {
              "city": "Campo Grande",
              "state": "Campo Grande",
              "country": "Brasil",
              "zip_code": "1213454",
              "address": "Rua Carlos Fortunato Paiva",
              "complement": "",
              "neighborhood": "",
              "number": "123"
            }
          }
        }
      ]
    }
  ],
  "page_info": { "total_results": 55, "next_page_token": "...", "results_per_page": 1 }
}
```

**Sandbox**: ✅ Supported

---

### GET /payments/api/v1/sales/commissions

**Description**: Shows commission amounts and percentages per participant (producer, co-producer, addon) per transaction.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `max_results` | integer | No | Max items per page |
| `page_token` | string | No | Pagination cursor |
| `product_id` | long | No | 7-digit product ID |
| `start_date` | long | No | Start date (ms) |
| `end_date` | long | No | End date (ms) |
| `transaction` | string | No | Transaction code |
| `commission_as` | string | No | `PRODUCER`, `COPRODUCER`, `AFFILIATE` |
| `transaction_status` | string | No | See [Purchase Statuses](#purchase-statuses) |

**Response:**
```json
{
  "items": [
    {
      "transaction": "HP12345678901234",
      "product": { "name": "Product Test", "id": 123456 },
      "exchange_rate_currency_payout": 0.001334,
      "commissions": [
        {
          "commission": { "currency_value": "USD", "value": 95.00 },
          "user": { "ucode": "1c2fbe3a-...", "name": "Name User Producer Test" },
          "source": "PRODUCER"
        },
        {
          "commission": { "currency_value": "USD", "value": 4.35 },
          "user": { "ucode": "1c2fbe3a-...", "name": "Name User Coproducer Test" },
          "source": "COPRODUCER"
        },
        {
          "commission": { "currency_value": "USD", "value": 0.65 },
          "user": { "ucode": "1c2fbe3a-...", "name": "Name User Addon Test" },
          "source": "ADDON"
        }
      ]
    }
  ],
  "page_info": { "total_results": 10, "results_per_page": 10 }
}
```

**Sandbox**: ✅ Supported

---

### GET /payments/api/v1/sales/price/details

**Description**: Breakdown of purchase value — base amount, total, VAT, Hotmart fee, coupon discount, currency conversion.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `max_results` | integer | No | Max items per page |
| `page_token` | string | No | Pagination cursor |
| `product_id` | long | No | 7-digit product ID |
| `start_date` | long | No | Start date (ms) |
| `end_date` | long | No | End date (ms) |
| `transaction` | string | No | Transaction code |
| `transaction_status` | string | No | See [Purchase Statuses](#purchase-statuses) |
| `payment_type` | string | No | See [Payment Types](#payment-types) |

**Response:**
```json
{
  "items": [
    {
      "transaction": "HP14916251567230",
      "product": { "id": 8547854, "name": "product1" },
      "base": { "value": 930, "currency_code": "MXN" },
      "total": { "value": 486.25, "currency_code": "MXN" },
      "vat": { "value": 193.25, "currency_code": "BRL" },
      "fee": { "value": 55, "currency_code": "USD" },
      "coupon": { "code": "coupon1", "value": 22.9 },
      "real_conversion_rate": 708.75
    }
  ],
  "page_info": { "total_results": 14, "next_page_token": "...", "results_per_page": 10 }
}
```

**Sandbox**: ✅ Supported

---

### PUT /payments/api/v1/sales/:transaction_code/refund

**Description**: Requests a refund for a sale.

**Conditions for refund eligibility:**
- Sale status must be `APPROVED` or `COMPLETE`
- Not in trial mode
- Not paid with BACS or SEPA (those require bank-direct refund)
- Within refund window: minimum 7 days, up to 30 days (extendable to 60 days)
- Affiliate sales: within 30 days of purchase

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `transaction_code` | string | **Yes** | Transaction code (e.g. `HP17715690036014`) |

**Request Body:** None

**Response:** Empty body (`{}`). Evaluate HTTP status code only.

**Example cURL:**
```bash
curl --request PUT \
  'https://developers.hotmart.com/payments/api/v1/sales/HP17715690036014/refund' \
  --header 'Authorization: Bearer :access_token' \
  --header 'Content-Type: application/json'
```

**Sandbox**: ✅ Supported

---

## Subscriptions

All subscription endpoints: `/payments/api/v1/subscriptions/...`

---

### GET /payments/api/v1/subscriptions

**Description**: Lists all subscriptions/subscribers with detailed information.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `max_results` | integer | No | Max items per page |
| `page_token` | string | No | Pagination cursor |
| `product_id` | long | No | 7-digit product ID |
| `plan` | array[string] | No | Plan name(s) — repeatable param |
| `plan_id` | long | No | Unique subscription plan ID |
| `accession_date` | long | No | Subscription start date (ms). Default: now - 30 days |
| `end_accession_date` | long | No | Subscription end date filter (ms) |
| `status` | string | No | See [Subscription Statuses](#subscription-statuses) |
| `subscriber_code` | string | No | Unique subscriber code |
| `subscriber_email` | string | No | Subscriber email |
| `transaction` | string | No | Transaction code |
| `trial` | boolean | No | Filter by trial period |
| `cancelation_date` | long | No | Cancellations from date (ms). Default: now - 30 days |
| `end_cancelation_date` | long | No | Cancellations until date (ms). Default: now |
| `date_next_charge` | long | No | Next charge date filter (ms) |
| `end_date_next_charge` | long | No | Next charge until date (ms) |

**Response:**
```json
{
  "items": [
    {
      "subscriber_code": "ABC12DEF",
      "subscription_id": 123456,
      "status": "ACTIVE",
      "accession_date": 1577847600,
      "end_accession_date": 1641005999,
      "request_date": 1577847600,
      "date_next_charge": 1580558059,
      "trial": false,
      "transaction": "HP16616613605324",
      "plan": {
        "name": "Plan name",
        "id": 726420,
        "recurrency_period": 30,
        "max_charge_cycles": 6
      },
      "product": {
        "id": 123456,
        "name": "Product Name",
        "ucode": "12a34bcd-56e7-4847-fg89-h1i23j4567l8"
      },
      "price": { "value": 123.45, "currency_code": "BRL" },
      "subscriber": {
        "name": "Subscriber name",
        "email": "subscriber@email.com.br",
        "ucode": "10a98bcd-76e5-4321-fg09-h8i76j5432l1"
      }
    }
  ],
  "page_info": {
    "total_results": 30,
    "next_page_token": "05b60506...",
    "prev_page_token": "cf1fg8bd...",
    "results_per_page": 10
  }
}
```

**Sandbox**: ✅ Supported

---

### GET /payments/api/v1/subscriptions/summary

**Description**: Overview of subscription status including Smart Installments and Smart Recovery data. **Data has up to 24-hour delay.**

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `max_results` | integer | No | Max items per page |
| `page_token` | string | No | Pagination cursor |
| `product_id` | long | No | 7-digit product ID |
| `subscriber_code` | string | No | Subscriber code |
| `accession_date` | long | No | Start date (ms) |
| `end_accession_date` | long | No | End date (ms) |
| `date_next_charge` | long | No | Next payment date filter (ms) |

**Response:**
```json
{
  "items": [
    {
      "subscriber_code": "ABC12DEF",
      "subscription_id": 1223334,
      "status": "ACTIVE",
      "lifetime": 200,
      "accession_date": 1694113403000,
      "end_accession_date": 1694113503000,
      "trial": true,
      "plan": { "name": "Plan name", "recurrency_period": 180 },
      "product": { "name": "Product name", "id": 12345 },
      "offer": { "code": "o1c97lta" },
      "last_recurrency": {
        "number": 2,
        "request_date": 1694113403000,
        "status": "NOT_PAID",
        "transaction_number": 1,
        "billing_type": "SMART_INSTALLMENT"
      },
      "unpaid_recurrencies": [{ "number": 2, "charge_date": 1694113403000 }],
      "subscriber": { "name": "John", "id": 12345, "email": "teste@email.com" }
    }
  ],
  "page_info": { "results_per_page": 10, "next_page_token": "...", "prev_page_token": "..." }
}
```

**`billing_type` values:** `SUBSCRIPTION`, `SMART_INSTALLMENT`, `SMART_RECOVERY`

**Sandbox**: ✅ Supported

---

### GET /payments/api/v1/subscriptions/:subscriber_code/purchases

**Description**: Lists all recurrence payment transactions linked to a subscription. Important for metrics and refund actions.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `subscriber_code` | string | **Yes** | Unique subscriber code |

**Response (array):**
```json
[
  {
    "transaction": "HP12315823516751",
    "approved_date": 1583331578000,
    "payment_engine": "HotPay",
    "status": "APPROVED",
    "price": { "value": 108.0, "currency_code": "BRL" },
    "payment_type": "CREDIT_CARD",
    "payment_method": "VISA_CREDIT_CARD",
    "recurrency_number": 1,
    "under_warranty": false,
    "purchase_subscription": true
  }
]
```

**Sandbox**: ✅ Supported

---

### GET /payments/api/v1/subscriptions/:subscriber_code/transactions

**Description**: Lists transactions linked to a subscription (similar to purchases, subscription-level view).

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `subscriber_code` | string | **Yes** | Unique subscriber code |

**Sandbox**: ✅ Supported

---

### POST /payments/api/v1/subscriptions/cancel

**Description**: Cancels a list of subscriptions, interrupts the charge cycle, and notifies sub-systems (Club, Webhook).

**Request Body:**
```json
{
  "subscriber_code": ["9W2LNSG2", "RGT90XMB"],
  "send_mail": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `subscriber_code` | array[string] | **Yes** | List of subscriber codes to cancel |
| `send_mail` | boolean | No | Send cancellation email. Default: `true` |

**Response:**
```json
{
  "success_subscriptions": [
    {
      "status": "INACTIVE",
      "subscriber_code": "9W2LNSG2",
      "creation_date": "2020-07-20 17:57:42",
      "current_recurrence": 1,
      "date_last_recurrence": "2020-07-20 17:57:42",
      "date_next_charge": "2020-08-24 12:00:00",
      "due_day": 24,
      "trial_period": 26,
      "interval_type_between_charges": "MONTH",
      "interval_between_charges": 1,
      "max_charge_cycles": 13,
      "activation_date": "2020-07-20 17:57:44",
      "shopper": { "email": "shopper@email.com.br", "phone": "(31) 988888888" }
    }
  ],
  "fail_subscriptions": [
    {
      "status": "INACTIVE",
      "error": "SUBSCRIPTION_ALREADY_CANCELED_OR_OVERDUE",
      "subscriber_code": "RGT90XMB",
      "creation_date": "2020-07-08 16:35:57",
      "interval_between_charges": 30,
      "shopper": { "email": "shopper2@email.com.br", "phone": "(31) 988888888" }
    }
  ]
}
```

**Sandbox**: ✅ Supported

---

### POST /payments/api/v1/subscriptions/reactivate

**Description**: Reactivates a list of inactive subscriptions. Optionally issues a new charge. Subscriber receives an email with a reactivation link **valid for 3 days** to confirm.

**Request Body:**
```json
{
  "subscriber_code": ["9W2LNSG2"],
  "charge": false
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `subscriber_code` | array[string] | **Yes** | List of subscriber codes to reactivate |
| `charge` | boolean | No | Issue new charge after reactivation. Default: `false` |

**Response:** Same structure as cancel — `success_subscriptions` and `fail_subscriptions` arrays.

**Sandbox**: ✅ Supported

---

### POST /payments/api/v1/subscriptions/:subscriber_code/reactivate

**Description**: Reactivates a single inactive subscription. Subscriber receives email with reactivation link valid 3 days.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `subscriber_code` | string | **Yes** | Unique subscriber code |

**Request Body:**
```json
{
  "charge": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `charge` | boolean | No | Issue new charge. Default: `false`. Billing date stays the same as before deactivation. |

**Response:**
```json
{
  "status": "INACTIVE",
  "subscriber_code": "9W2LNSG2",
  "creation_date": "2020-07-20 17:57:42",
  "interval_between_charges": 30,
  "shopper": { "email": "shopper@email.com.br", "phone": "(31) 988888888" }
}
```

**`interval_between_charges` values:** `7` (weekly), `30` (monthly), `60` (bimonthly), `90` (quarterly), `180` (semi-annual), `360` (annual)

**Sandbox**: ✅ Supported

---

### PATCH /payments/api/v1/subscriptions/:subscriber_code

**Description**: Changes the billing due day for a subscription.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `subscriber_code` | string | **Yes** | Unique subscriber code |

**Request Body:**
```json
{
  "due_day": 15
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `due_day` | integer | **Yes** | New billing day of month (1–31) |

**Response:** Empty body. Evaluate HTTP status code only (200 = success).

**Sandbox**: ⚠️ Not supported (as of last library update)

---

## Products

All product endpoints: `/products/api/v1/products/...`

---

### GET /products/api/v1/products

**Description**: Lists all products created by the authenticated account.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `max_results` | integer | No | Max items per page (default: 50) |
| `page_token` | string | No | Pagination cursor |
| `id` | long | No | 7-digit product ID |
| `status` | string | No | See [Product Statuses](#product-statuses) |
| `format` | string | No | See [Product Formats](#product-formats) |

**Response:**
```json
{
  "items": [
    {
      "id": 698441,
      "name": "Product A",
      "ucode": "f2b3be1f-313f-4a2d-b5b7-1c39d67dd3ee",
      "status": "DRAFT",
      "created_at": 1586459699000,
      "format": "EBOOK",
      "is_subscription": false,
      "warranty_period": 7
    },
    {
      "id": 1117869,
      "name": "Product B",
      "ucode": "26a97448-2ac2-458d-9e03-bcc01e82bdd8",
      "status": "DRAFT",
      "created_at": 1603816477000,
      "format": "ONLINE_COURSE",
      "is_subscription": true,
      "warranty_period": 15
    }
  ],
  "page_info": {
    "next_page_token": "eyJyb3dzIjo1LCJwYWdlIjozfQ==",
    "prev_page_token": "eyJyb3dzIjo1LCJwYWdlIjoxfQ==",
    "results_per_page": 4
  }
}
```

**Sandbox**: ✅ Supported

---

### GET /products/api/v1/products/:ucode/offers

**Description**: Returns all offers for a product including pricing, payment mode, and configuration flags.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `ucode` | string | **Yes** | Product UUID (from products list) |

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `max_results` | integer | No | Max items per page |
| `page_token` | string | No | Pagination cursor |

**Response:**
```json
{
  "items": [
    {
      "code": "02mhofjd",
      "name": "",
      "description": "",
      "price": { "value": 10, "currency_code": "BRL" },
      "payment_mode": "PAY_IN_FULL",
      "is_currency_conversion_enabled": true,
      "is_main_offer": true,
      "is_smart_recovery_enabled": false
    }
  ],
  "page_info": { "next_page_token": "...", "prev_page_token": null, "results_per_page": 1 }
}
```

**Sandbox**: ✅ Supported

---

### GET /products/api/v1/products/:ucode/plans

**Description**: Returns all subscription plans for a product including pricing, periodicity, trial, and installment settings.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `ucode` | string | **Yes** | Product UUID |

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `max_results` | integer | No | Max items per page |
| `page_token` | string | No | Pagination cursor |

**Response:**
```json
{
  "items": [
    {
      "code": "tz12qeev",
      "name": "Básico Mensal",
      "description": "Plano básico mensal",
      "price": { "value": 10, "currency_code": "BRL" },
      "payment_mode": "ASSINATURA",
      "periodicity": "MONTHLY",
      "max_installments": 1,
      "is_subscription_recovery_enabled": false,
      "is_switch_plan_enabled": true
    },
    {
      "code": "pr6yifbw",
      "name": "Plano com Trial",
      "description": "Plano teste mensal com trial",
      "price": { "value": 200, "currency_code": "BRL" },
      "payment_mode": "ASSINATURA",
      "periodicity": "MONTHLY",
      "max_installments": 1,
      "trial_period": 7,
      "is_subscription_recovery_enabled": false,
      "is_switch_plan_enabled": false
    }
  ],
  "page_info": { "results_per_page": 7 }
}
```

**`periodicity` values:** `MONTHLY`, `BIMONTHLY`, `QUARTERLY`, `BIANNUAL`, `ANNUAL`

**Sandbox**: ✅ Supported

---

## Discount Coupons

---

### POST /payments/api/v1/product/:product_id/coupon

**Description**: Creates a discount coupon for a specific product.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `product_id` | string | **Yes** | Product UID (7-digit ID) |

**Request Body:**
```json
{
  "code": "SUMMER20",
  "discount": 0.20
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `code` | string | **Yes** | Coupon code (alphanumeric) |
| `discount` | float | **Yes** | Discount fraction. Must be > 0 and < 0.99 (e.g., 0.20 = 20% off) |

**Response:** Empty body. Evaluate HTTP status code (200 = success).

**Sandbox**: ⚠️ Not supported (as of last library update)

---

### GET /payments/api/v1/coupon/product/:product_id

**Description**: Retrieves coupon information for a product.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `product_id` | string | **Yes** | Product UID |

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `code` | string | No | Coupon code to filter |

**Sandbox**: ⚠️ Not supported (as of last library update)

---

### DELETE /payments/api/v1/coupon/:coupon_id

**Description**: Deletes a coupon by its ID.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `coupon_id` | string | **Yes** | Coupon ID |

**Response:** Empty body. Evaluate HTTP status code (200 = success).

**Sandbox**: ⚠️ Not supported (as of last library update)

---

## Members Area (Club)

All Club endpoints: `/club/api/v1/...`

> **Note**: Club endpoints use the `subdomain` query parameter to identify which Members Area to query. Find the subdomain in Club settings.

---

### GET /club/api/v1/modules

**Description**: Retrieves all content modules created by the Producer in the Members Area, including main modules and extra modules.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `subdomain` | string | **Yes** | Members Area subdomain name (from Club settings) |
| `is_extra` | boolean | No | `true` = return extra modules only, `false` = main modules only. Default: `false` |

**Response (array):**
```json
[
  {
    "module_id": "2z7ramxejw",
    "name": "Hotmart Club - Module 1",
    "sequence": 1,
    "is_extra": false,
    "is_extra_paid": false,
    "is_public": false,
    "classes": ["qV7y1Jm7Jn"],
    "total_pages": 2
  },
  {
    "module_id": "j14okvB4pL",
    "name": "Hotmart Club - Module 2",
    "sequence": 2,
    "is_extra": false,
    "is_extra_paid": false,
    "is_public": true,
    "classes": ["qV7y1Jm7Jn"],
    "total_pages": 4
  }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `module_id` | string | Unique module ID |
| `name` | string | Module name |
| `sequence` | integer | Display order |
| `is_public` | boolean | Free/public module (no purchase required) |
| `is_extra` | boolean | Extra/additional module |
| `is_extra_paid` | boolean | Whether extra module is paid |
| `classes` | array[string] | Array of lesson/class IDs in the module |
| `total_pages` | integer | Total number of pages in module |

**Sandbox**: ✅ Supported

---

### GET /club/api/v1/pages

**Description**: Retrieves pages (lessons) within a module.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `subdomain` | string | **Yes** | Members Area subdomain |
| `module_id` | string | **Yes** | Module ID (from get-modules) |

**Sandbox**: ✅ Supported

---

### GET /club/api/v1/students

**Description**: Retrieves the list of students enrolled in the Members Area.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `subdomain` | string | **Yes** | Members Area subdomain |

**Sandbox**: ✅ Supported

---

### GET /club/api/v1/students/progress

**Description**: Retrieves progress data for students (pages viewed, completion percentage).

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `subdomain` | string | **Yes** | Members Area subdomain |
| `student_email` | string | No | Filter by student email |

**Sandbox**: ✅ Supported

---

## Event Tickets

---

### GET /payments/api/v1/events/:event_id

**Description**: Returns event information for a specific product event.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `event_id` | string | **Yes** | Event ID |

---

### GET /payments/api/v1/tickets

**Description**: Lists tickets and participants for an event. Only tickets with **confirmed payment** or **complimentary** status are returned.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `product_id` | long | **Yes** | Product ID |
| `max_results` | integer | No | Max items per page |
| `page_token` | string | No | Pagination cursor |

---

## Installments Negotiation

> **New endpoint** (added 2025). Allows generating installment negotiation offers for overdue payments.

### POST /payments/api/v1/negotiation

**Description**: Generates an installment negotiation offer for a subscriber with overdue payments.

**Request Body:**
```json
{
  "subscriber_code": "9W2LNSG2"
}
```

**Sandbox**: ✅ Supported

---

## Webhooks

Webhooks allow your system to receive real-time event notifications from Hotmart.

**Setup**: In Hotmart dashboard → Tools → Developer Tools → Webhooks. Configure a URL to receive POST requests.

**Security**: Each account has a unique `Hottok` token. Verify incoming webhooks by checking the `hottok` field in the payload matches your configured token.

**Webhook versions**: `1.0.0` (legacy) and `2.0.0` (current, recommended). Version 2.0.0 was updated on 2026-03-09 with a new `variants` field on purchase events.

### Webhook Event Types

| Event | Trigger |
|-------|---------|
| `PURCHASE_APPROVED` | Purchase approved |
| `PURCHASE_COMPLETE` | Purchase completed |
| `PURCHASE_CANCELED` | Purchase canceled |
| `PURCHASE_REFUNDED` | Purchase refunded |
| `PURCHASE_CHARGEBACK` | Chargeback initiated |
| `PURCHASE_BILLET_PRINTED` | Bank slip generated |
| `PURCHASE_PROTEST` | Purchase protested |
| `PURCHASE_EXPIRED` | Purchase expired |
| `PURCHASE_DELAYED` | Purchase delayed |
| `SUBSCRIPTION_CANCELLATION` | Subscription canceled |
| `SWITCH_PLAN` | Subscriber changed plan |
| `CART_ABANDONMENT` | Cart abandoned |
| `SUBSCRIPTION_BILLING_DATE_CHANGE` | Billing date changed |
| `CLUB_FIRST_ACCESS` | Student first access to Club |
| `CLUB_MODULE_COMPLETED` | Student completed a module |

---

### Webhook Payload Structure (v2.0.0)

All webhook events share a common envelope:

```json
{
  "id": "evt_12345",
  "creation_date": 1622948400000,
  "event": "PURCHASE_APPROVED",
  "version": "2.0.0",
  "data": { ... }
}
```

---

### Purchase Event Payload (v2.0.0)

Triggered on: `PURCHASE_APPROVED`, `PURCHASE_COMPLETE`, `PURCHASE_CANCELED`, `PURCHASE_REFUNDED`, `PURCHASE_CHARGEBACK`, `PURCHASE_BILLET_PRINTED`, `PURCHASE_EXPIRED`

```json
{
  "event": "PURCHASE_APPROVED",
  "id": "evt_abc123",
  "creation_date": 1622948400000,
  "version": "2.0.0",
  "data": {
    "product": {
      "id": 12345,
      "ucode": "f2b3be1f-...",
      "name": "My Course",
      "has_co_production": false
    },
    "affiliates": [
      {
        "affiliate_code": "aff123",
        "name": "Affiliate Name"
      }
    ],
    "buyer": {
      "email": "buyer@example.com",
      "name": "Buyer Name",
      "first_name": "Buyer",
      "last_name": "Name",
      "ucode": "839F1A4F-...",
      "address": {
        "country": "Brasil",
        "country_iso": "BR",
        "city": "São Paulo",
        "state": "SP",
        "zip_code": "01310-100"
      },
      "document": "123.456.789-00",
      "document_type": "CPF",
      "phone": "11999999999",
      "checkout_phone": "11999999999"
    },
    "producer": {
      "name": "Producer Name",
      "ucode": "252A74C5-...",
      "email": "producer@example.com",
      "document": "12345678000195"
    },
    "commissions": [
      {
        "value": 100.0,
        "currency_value": "BRL",
        "source": "PRODUCER"
      }
    ],
    "purchase": {
      "approved_date": 1622948400000,
      "full_price": { "value": 197.0, "currency_code": "BRL" },
      "original_offer_price": { "value": 197.0, "currency_code": "BRL" },
      "price": { "value": 197.0, "currency_code": "BRL" },
      "payment": {
        "method": "CREDIT_CARD",
        "installments_number": 1,
        "installment_value": 197.0,
        "type": "CREDIT_CARD"
      },
      "order_bump": { "is_order_bump": false },
      "offer": {
        "code": "k2pasun0",
        "payment_mode": "INVOICE"
      },
      "status": "APPROVED",
      "transaction": "HP12455690122399",
      "recurrency_number": 1,
      "is_subscription": false,
      "subscription": {
        "plan": {
          "name": "Monthly Plan",
          "id": 726420,
          "frequency": { "periodicity": "MONTHLY", "value": 1 }
        },
        "subscriber_code": "ABC12DEF",
        "status": "ACTIVE"
      },
      "hottok": "YOUR_HOTTOK_HERE",
      "date_next_charge": 1625540400000,
      "warranty_expire_date": 1625022000000,
      "tracking": {
        "source": "ORGANIC",
        "source_sck": "HOTMART_PRODUCT_PAGE",
        "external_code": "FD256D24-..."
      },
      "variants": [
        {
          "name": "Color",
          "option": { "name": "Blue" }
        }
      ]
    }
  }
}
```

> **Note**: `variants` field added 2026-03-09 to v2.0.0.

---

### Subscription Cancellation Event

```json
{
  "event": "SUBSCRIPTION_CANCELLATION",
  "data": {
    "subscriber_code": "ABC12DEF",
    "subscription_id": 123456,
    "status": "CANCELLED_BY_CUSTOMER",
    "product": { "id": 12345, "name": "My Course" },
    "subscriber": { "email": "subscriber@email.com", "name": "Subscriber Name" }
  }
}
```

---

### Plan Change Event (`SWITCH_PLAN`)

```json
{
  "event": "SWITCH_PLAN",
  "data": {
    "subscriber_code": "ABC12DEF",
    "old_plan": { "name": "Basic", "id": 111 },
    "new_plan": { "name": "Premium", "id": 222 },
    "product": { "id": 12345, "name": "My Course" }
  }
}
```

---

### Cart Abandonment Event (`CART_ABANDONMENT`)

```json
{
  "event": "CART_ABANDONMENT",
  "data": {
    "product": { "id": 12345, "name": "My Course" },
    "buyer": { "email": "buyer@email.com", "name": "Buyer Name" }
  }
}
```

---

### Subscription Billing Date Change Event

```json
{
  "event": "SUBSCRIPTION_BILLING_DATE_CHANGE",
  "data": {
    "subscriber_code": "ABC12DEF",
    "old_date_next_charge": 1622948400000,
    "new_date_next_charge": 1625540400000
  }
}
```

---

### First Access Event (`CLUB_FIRST_ACCESS`)

Triggered when a student accesses the Members Area for the first time.

```json
{
  "event": "CLUB_FIRST_ACCESS",
  "data": {
    "product": { "id": 12345, "name": "My Course" },
    "subscriber": { "email": "student@email.com", "name": "Student Name" }
  }
}
```

---

### Completed Module Event (`CLUB_MODULE_COMPLETED`)

Triggered when a student completes all pages in a module.

```json
{
  "event": "CLUB_MODULE_COMPLETED",
  "data": {
    "module_id": "2z7ramxejw",
    "module_name": "Module 1",
    "product": { "id": 12345, "name": "My Course" },
    "subscriber": { "email": "student@email.com", "name": "Student Name" }
  }
}
```

---

## Enums & Value Reference

### Purchase Statuses

| Value | Description |
|-------|-------------|
| `APPROVED` | Payment approved |
| `BLOCKED` | Blocked (under review) |
| `CANCELLED` | Canceled |
| `CHARGEBACK` | Chargeback initiated |
| `COMPLETE` | Completed (warranty period expired) |
| `EXPIRED` | Expired |
| `NO_FUNDS` | Insufficient funds |
| `OVERDUE` | Overdue |
| `PARTIALLY_REFUNDED` | Partially refunded |
| `PRE_ORDER` | Pre-order |
| `PRINTED_BILLET` | Bank slip printed (awaiting payment) |
| `PROCESSING_TRANSACTION` | Processing |
| `PROTESTED` | Protested |
| `REFUNDED` | Fully refunded |
| `STARTED` | Started |
| `UNDER_ANALISYS` | Under analysis |
| `WAITING_PAYMENT` | Waiting for payment |

---

### Subscription Statuses

| Value | Description |
|-------|-------------|
| `ACTIVE` | Active subscription |
| `INACTIVE` | Inactive |
| `DELAYED` | Payment delayed |
| `CANCELLED_BY_CUSTOMER` | Canceled by subscriber |
| `CANCELLED_BY_SELLER` | Canceled by producer |
| `CANCELLED_BY_ADMIN` | Canceled by admin |
| `STARTED` | Just started |
| `OVERDUE` | Overdue |

---

### Payment Types

| Value | Description |
|-------|-------------|
| `BILLET` | Bank slip (boleto) |
| `CASH_PAYMENT` | Cash payment |
| `CREDIT_CARD` | Credit card |
| `DIRECT_BANK_TRANSFER` | Direct bank transfer |
| `DIRECT_DEBIT` | Direct debit |
| `FINANCED_BILLET` | Financed bank slip |
| `FINANCED_INSTALLMENT` | Financed installment |
| `GOOGLE_PAY` | Google Pay |
| `HOTCARD` | Hotmart card |
| `HYBRID` | Hybrid payment |
| `MANUAL_TRANSFER` | Manual transfer |
| `PAYPAL` | PayPal |
| `PAYPAL_INTERNACIONAL` | PayPal International |
| `PICPAY` | PicPay |
| `PIX` | Pix |
| `SAMSUNG_PAY` | Samsung Pay |
| `WALLET` | Digital wallet |

---

### Product Statuses

| Value | Description |
|-------|-------------|
| `DRAFT` | Not yet published |
| `ACTIVE` | Published and active |
| `PAUSED` | Temporarily paused |
| `NOT_APPROVED` | Rejected in review |
| `IN_REVIEW` | Under review |
| `DELETED` | Deleted |
| `CHANGES_PENDING_ON_PRODUCT` | Changes pending approval |

---

### Product Formats

| Value | Description |
|-------|-------------|
| `EBOOK` | E-book |
| `SOFTWARE` | Software |
| `MOBILE_APPS` | Mobile applications |
| `VIDEOS` | Video course |
| `AUDIOS` | Audio course |
| `TEMPLATES` | Templates |
| `IMAGES` | Images |
| `ONLINE_COURSE` | Online course |
| `SERIAL_CODES` | Serial codes |
| `ETICKET` | E-ticket (event) |
| `ONLINE_SERVICE` | Online service |
| `ONLINE_EVENT` | Online event |
| `BUNDLE` | Bundle / Pack |
| `COMMUNITY` | Community / Forum |
| `AGENT` | AI Agent |

---

### Commission Source Types

| Value | Description |
|-------|-------------|
| `PRODUCER` | Product producer |
| `COPRODUCER` | Co-producer |
| `AFFILIATE` | Affiliate |
| `ADDON` | Add-on (extra product/service) |

---

### Subscription Periodicity / Interval Between Charges

| `interval_between_charges` | `periodicity` | Description |
|----------------------------|---------------|-------------|
| 7 | — | Weekly |
| 30 | `MONTHLY` | Monthly |
| 60 | `BIMONTHLY` | Bimonthly |
| 90 | `QUARTERLY` | Quarterly |
| 180 | `BIANNUAL` | Semi-annual |
| 360 | `ANNUAL` | Annual |

---

## Quick Reference — All Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/payments/api/v1/sales/history` | Sales history |
| `GET` | `/payments/api/v1/sales/summary` | Sales summary |
| `GET` | `/payments/api/v1/sales/users` | Sales participants |
| `GET` | `/payments/api/v1/sales/commissions` | Sales commissions |
| `GET` | `/payments/api/v1/sales/price/details` | Sales price breakdown |
| `PUT` | `/payments/api/v1/sales/:transaction_code/refund` | Request refund |
| `GET` | `/payments/api/v1/subscriptions` | List subscriptions |
| `GET` | `/payments/api/v1/subscriptions/summary` | Subscription summary |
| `GET` | `/payments/api/v1/subscriptions/:code/purchases` | Subscriber purchases |
| `GET` | `/payments/api/v1/subscriptions/:code/transactions` | Subscriber transactions |
| `POST` | `/payments/api/v1/subscriptions/cancel` | Cancel subscription(s) |
| `POST` | `/payments/api/v1/subscriptions/reactivate` | Reactivate subscription(s) |
| `POST` | `/payments/api/v1/subscriptions/:code/reactivate` | Reactivate single subscription |
| `PATCH` | `/payments/api/v1/subscriptions/:code` | Change billing due day |
| `GET` | `/products/api/v1/products` | List products |
| `GET` | `/products/api/v1/products/:ucode/offers` | Product offers |
| `GET` | `/products/api/v1/products/:ucode/plans` | Product subscription plans |
| `POST` | `/payments/api/v1/product/:product_id/coupon` | Create coupon |
| `GET` | `/payments/api/v1/coupon/product/:product_id` | Get coupon |
| `DELETE` | `/payments/api/v1/coupon/:coupon_id` | Delete coupon |
| `GET` | `/club/api/v1/modules` | List Members Area modules |
| `GET` | `/club/api/v1/pages` | List module pages |
| `GET` | `/club/api/v1/students` | List students |
| `GET` | `/club/api/v1/students/progress` | Students progress |
| `GET` | `/payments/api/v1/events/:event_id` | Event information |
| `GET` | `/payments/api/v1/tickets` | List tickets and participants |
| `POST` | `/payments/api/v1/negotiation` | Generate installment negotiation |

---

## Notes for AI Agents

- **Dates**: All date fields are Unix timestamp in **milliseconds** (not seconds). Multiply Python `datetime.timestamp()` by 1000.
- **Token caching**: Always cache the access token. It expires in 86400s. Fetching a new one on every request will hit rate limits.
- **Default filter**: Sales and commission endpoints only return `APPROVED` and `COMPLETE` by default. To get all statuses, always pass `transaction_status` or `transaction` parameters.
- **Subscription `subscriber_code`**: This is NOT the buyer's `ucode`. It's a separate code uniquely identifying a subscription relationship. Always use `subscriber_code` for subscription operations.
- **Product `ucode` vs `id`**: Product endpoints use `ucode` (UUID format). Sales/subscription endpoints use the 7-digit numeric `id`.
- **Club `subdomain`**: The subdomain is the URL prefix of the Members Area (e.g., if the Club URL is `mymembers.hotmart.com`, subdomain is `mymembers`).
- **Refund window**: Default is buyer can request refund for 7–30 days. Extended period can go up to 60 days. Check before calling refund endpoint.
- **Webhook verification**: Always verify `hottok` field in webhook payload matches your configured token to prevent forgery.
- **Pagination**: This API uses cursor-based pagination, not page numbers. Never use integer page numbers — always pass the `next_page_token` from the previous response as `page_token`.

# Hotmart Python

This is a Python Wrapper for the Hotmart API, which allows you to interact with resources offered by
the platform:

**Nota**: A documentação em português está disponível [aqui](README-ptBR.md).

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
    - [Usage example 1](#usage-example-1)
    - [Logs](#logs)
    - [Sandbox](#sandbox)
    - [Usage example 2](#usage-example-2)
    - [Pagination](#pagination)
- [Supported Parameters](#supported-parameters)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## Features:

- ✅ Authentication
- ✅ Pagination
- ✅ All sales endpoints
- ✅ All subscriptions endpoints
- ✅ All coupons endpoints

## Installation

```bash
pip install hotmart-python
```

## Usage

### Usage example 1:

Here's how you can use the Hotmart Python Wrapper in your Python code:

```python
from hotmart_python import Hotmart

# Initialize the Hotmart client
hotmart = Hotmart(client_id='your_client_id',
                  client_secret='your_client_secret',
                  basic='your_basic_token')

# Example usage: Get sales history
sales_history = hotmart.get_sales_history()
print(sales_history)
```

### Logs:

By default, logging is disabled. You can enable it and set the log level by passing the `log_level`
parameter when initializing the Hotmart object. The available log levels are:

- ️️☣️ `logging.DEBUG`: Debug level logging, which includes detailed information such as request
  URLs and parameters
  (**not recommended for production use due to sensitive information being logged**).
- `logging.INFO`: Information level logging, which provides basic information about the operations
  being performed.
- `logging.WARNING`: Warning level logging, which indicates potential issues or unexpected behavior.
- `logging.ERROR`: Error level logging, which indicates errors that occur during API interactions.
- `logging.CRITICAL`: Critical level logging, which indicates critical errors that require immediate
  attention.

```python
import logging
from hotmart_python import Hotmart

# Initialize the Hotmart client
hotmart = Hotmart(client_id='your_client_id',
                  client_secret='your_client_secret',
                  basic='your_basic_token',
                  log_level=logging.INFO)
```

The parameter log_level can be omitted, and if done, it will fall back to the default log level,
which is `logging.WARNING`.

### Sandbox:

It is also possible to use the `sandbox` parameter to enable the sandbox environment, which can only
be accessed if previously generated credentials targeting sandbox mode are generated inside Hotmart.
By default, e sandbox environment is disabled.

```python
import logging
from hotmart_python import Hotmart

# Initialize the Hotmart client
hotmart = Hotmart(client_id='your_sandbox_client_id',
                  client_secret='your_sandbox_client_secret',
                  basic='your_sandbox_basic_token',
                  log_level=logging.INFO,
                  sandbox=True)
```

### Usage example 2:

Usage example for getting sales history with logging enabled and log level set to INFO and using
query filters to get sales by buyer email:

```python
from hotmart_python import Hotmart
import logging

# Initialize the Hotmart client with logging enabled and log level set to DEBUG
hotmart = Hotmart(client_id='your_client_id',
                  client_secret='your_client_secret',
                  basic='your_basic',
                  log_level=logging.INFO)

# Example usage: Get sales history
sales_history = hotmart.get_sales_history(buyer_email='johndoe@example.com')
print(sales_history)
```

### Pagination:

By default, pagination is disabled. If you want to enable pagination, you can use de `paginate`
decorator, there are two ways of doing it.

The first one (and simplest) is to use the decorator in a wrapper function

```python
from hotmart_python import Hotmart
from hotmart_python.decorators import paginate

hotmart = Hotmart(client_id='your_client_id',
                  client_secret='your_client_secret',
                  basic='your_basic')


@paginate
def get_sales_history(*args, **kwargs):
    return hotmart.get_sales_history(*args, **kwargs)


print(get_sales_history())
```

The second one, it's a one-liner lambda function

```python
from hotmart_python import Hotmart
from hotmart_python.decorators import paginate

hotmart = Hotmart(client_id='your_client_id',
                  client_secret='your_client_secret',
                  basic='your_basic')

get_sales_history = paginate(lambda *args, **kwargs: hotmart.get_sales_history(*args, **kwargs))
print(get_sales_history())
```

## Supported Parameters

These are the supported parameters for all methods that interact with the Hotmart API:

- `kwargs`: Any queries that are supported by the endpoint. For example, the `get_sales_history`
  method supports the
  following parameters:
    - `max_results` (int): The maximum number of items per page that can be returned.
    - `product_id` (int): Unique identifier (ID) of the product sold (7-digit number).
    - `start_date` (int): Start date of the filter period. The date must be in milliseconds,
      starting from 1970-01-01
      00:00:00 UTC.
    - `end_date` (int): End date of the filter period. The date must be in milliseconds, starting
      from 1970-01-01 00:00:
      00 UTC.
    - `sales_source` (str): SRC code used in the link on the product payment page to track the
      origin. (
      E.g., `pay.hotmart.com/B00000000T?src=campaignname`)
    - `buyer_name` (str): Buyer Name.
    - `buyer_email` (str): Email address of the buyer. You can use this information to search for
      specific purchases.
    - `product_id` (str): The ID of the product.
    - `transaction` (str): Unique reference code for a transaction, e.g., HP17715690036014. A
      transaction happens when
      an order is placed. An order can be a bank payment slip generated, an approved purchase, a
      recurring payment, and
      more.
    - `transaction_status` (str): The status of the sale (e.g. 'approved', 'pending', 'refunded', '
      canceled', '
      chargeback').
    - And others.

For more information about queries, please refer to
the [Hotmart API documentation](https://developers.hotmart.com/docs/en/). Any query parameter that
is supported by the
endpoint can be passed as a keyword argument to the method.

## API Reference

Here's a brief overview of the methods available in the `Hotmart` class:

- `get_sales_history(**kwargs)`: Retrieves the sales history. Accepts optional keyword arguments for
  filtering the
  results. [Reference](https://developers.hotmart.com/docs/en/v1/sales/sales-history/)

- `get_sales_summary(**kwargs)`: Retrieves the sales summary. Accepts optional keyword arguments for
  filtering the
  results. [Reference](https://developers.hotmart.com/docs/en/v1/sales/sales-summary/)

- `get_sales_participants(**kwargs)`: Retrieves the sales participants. Accepts optional keyword
  arguments for filtering
  the results. [Reference](https://developers.hotmart.com/docs/en/v1/sales/sales-users/)

- `get_sales_commissions(**kwargs)`: Retrieves the sales commissions. Accepts optional keyword
  arguments for filtering
  the results. [Reference](https://developers.hotmart.com/docs/en/v1/sales/sales-commissions/)

- `get_sales_price_details(**kwargs)`: Retrieves the sales price details. Accepts optional keyword
  arguments for
  filtering the
  results. [Reference](https://developers.hotmart.com/docs/en/v1/sales/sales-price-details/)

- `get_subscriptions(paginate=False, **kwargs)`: Retrieves the subscriptions. Accepts an
  optional `paginate` argument
  and additional keyword arguments for filtering the
  results. [Reference](https://developers.hotmart.com/docs/en/v1/subscription/get-subscribers/)

- `get_subscription_summary(paginate=False, **kwargs)`: Retrieves the subscription summary. Accepts
  an
  optional `paginate` argument and additional keyword arguments for filtering the
  results. [Reference](https://developers.hotmart.com/docs/en/v1/subscription/get-subscription-summary/)

- `get_subscription_purchases(subscriber_code, paginate=False, **kwargs)`: Retrieves the
  subscription purchases for a
  specific subscriber. Requires a `subscriber_code` argument and accepts an optional `paginate`
  argument and additional
  keyword arguments for filtering the
  results. [Reference](https://developers.hotmart.com/docs/en/v1/subscription/get-subscription-purchases/)

- `cancel_subscription(subscriber_code, send_email=True)`: Cancels a subscription. Requires
  a `subscriber_code` argument
  and accepts an optional `send_email`
  argument. [Reference](https://developers.hotmart.com/docs/en/v1/subscription/cancel-subscriptions/)

- `reactivate_and_charge_subscription(subscriber_code, charge=True)`: Reactivates and charges a
  subscription. Requires
  a `subscriber_code` argument and accepts an optional `charge`
  argument. [Reference](https://developers.hotmart.com/docs/en/v1/subscription/reactivate-subscription/)

For more detailed information about these methods and the parameters they accept, please refer to
the source code or the
[official Hotmart API documentation](https://developers.hotmart.com/docs/en/).

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please open
an issue or submit a
pull request on the GitHub repository.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](../LICENSE.txt) file for
details.

This package is not affiliated with Hotmart. It is an open-source project that is not officially
supported by Hotmart.

0.5.0 / 2024-03-24
==================

* Changed underlying way of making requests, now standardizing the output of the response for it
  to be always a list of dicts.
* Added new _handle_response method for standardizing the response.
* Added new decorator `@paginate` for handling pagination in the endpoints.
* Removed old `_paginate` method.
* Changed references to the old `_paginate` method to `_request_with_token`.
* Enhanced type hints for better readability.
* Most tests were refactored to reflect the changes in the new request handling.
* Fixed a bug where `subscriber_code` was not being passed to the request body as expected in
  `change_due_day` method.
* Updated README with the new changes.

0.4.1 / 2024-03-22
==================

* Better error handling for _make_request.
* Removed custom exceptions.
* Changed tests to better fit exceptions changes.

0.4.0 / 2024-03-21
==================

* New endpoint added: Discount Coupons
* Added tests for the new endpoint
* Added code examples for Sandbox testing

0.3.0 / 2024-03-21
==================

* **Breaking change**: Removed support for python <3.9 due to the use of flake8
  for linting.
* Added .editorconfig file for better code standardization.
* Code slightly refactored to comply with flake8.
* Added GitHub Actions for Testing and Linting.

0.2.2 / 2024-03-21
==================

* Refactored helper methods for better error handling
* Refactored tests to reflect the changes in the helper methods
* Changed _pagination output to return a list of dicts instead a list of lists.
* Removed unnecessary setup.py file.

0.2.1 / 2024-03-20
==================

* Added subscriptions endpoint
* Added tests for subscriptions
* Changed _get_with_token and _post_with_token methods to use the new _request_with_token for more
  flexibility
* Fixed issue with pagination
* Updated docs for the new subscriptions endpoint
* Renamed README.dev.md to CONTRIBUTING.md, for better standardization
* Changed get_sales_users to get_sales_participants to better reflect the endpoint's name in
  the [API Reference](https://developers.hotmart.com/docs/en/v1/sales/sales-users/)
* Changed tests references to the updated name of the get_sales_participants
* Migrated to Poetry for dependency management.

0.1.20 / 2024
==================

* Test releases

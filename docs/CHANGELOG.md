0.3.0 / 2024-03-21
==================

* Breaking change: Removed support for python <3.9 due to the use of flake8
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

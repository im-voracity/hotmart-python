# Hotmart Sandbox Mode Usage Guide

The Hotmart API provides a Sandbox mode for testing purposes. This guide will help you understand
the particularities of some methods when used in Sandbox mode.

Although the Hotmart API provides a Sandbox mode, some methods may not work as expected. This is
because the API does not support some methods, or they not work as expected for Sandbox
mode. This guide will help you understand which methods are not supported in the Sandbox mode.

For all subscriptions methods that need a `subscriber_code`, please note that the Sandbox API
DOES provide some codes that should, in theory, work, and you can find them at the bottom of some
pages in the API Reference. However, that's not true, at least at the time of the last update for
this library.

The same happens to the discount coupons methods.

Usually, you'll find errors ranging from `404 Not Found` to `500 Internal Server Error`.
This is only for the Sandbox environment. The production environment should work as expected.

Below there are a list of methods that currently are not working as expeceted in Sandbox Mode.

`get_subscription_purchases`

`cancel_subscription`

`reactivate_and_charge_subscription`

`change_due_day`

`create_coupon`

`get_coupon`

`delete_coupon`

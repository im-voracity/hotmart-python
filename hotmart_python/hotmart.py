import coloredlogs
import requests
import logging
import time
import sys

from typing import List, Dict, Any, Optional

# Base Logging Configs
logger = logging.getLogger(__name__)

# Coloredlogs Configs
coloredFormatter = coloredlogs.ColoredFormatter(
    fmt='[%(name)s] %(asctime)s  %(message)s',
    level_styles=dict(
        debug=dict(color='white'),
        info=dict(color='blue'),
        warning=dict(color='yellow', bright=True),
        error=dict(color='red', bold=True, bright=True),
        critical=dict(color='black', bold=True, background='red'),
    ),
    field_styles=dict(
        name=dict(color='white'),
        asctime=dict(color='white'),
        funcName=dict(color='white'),
        lineno=dict(color='white'),
    )
)

# Console Handler Configs
ch = logging.StreamHandler(stream=sys.stdout)
ch.setFormatter(fmt=coloredFormatter)
logger.addHandler(hdlr=ch)
logger.setLevel(level=logging.CRITICAL)

# URL Configs
PRODUCTION_BASE_URL = "https://developers.hotmart.com/payments/api/"
SANDBOX_BASE_URL = "https://sandbox.hotmart.com/payments/api/"


class Hotmart:
    def __init__(self, client_id: str, client_secret: str, basic: str,
                 api_version: int = 1,
                 sandbox: bool = False,
                 log_level: int = logging.CRITICAL) -> None:
        """
        Initializes the Hotmart API client. Full docs can be found at
        https://developers.hotmart.com/docs/en/
        :param client_id: The Client ID provided by Hotmart.
        :param client_secret: The Client Secret provided by Hotmart.
        :param basic: The Basic Token provided by Hotmart.
        :param api_version: The version of the API to use (default is "1").
        :param sandbox: Whether to use the sandbox or not (default is False).
        :param log_level: The logging level to use (default is logging.INFO).
        """

        self.id = client_id
        self.secret = client_secret
        self.basic = basic
        self.sandbox = sandbox
        self.base_url = SANDBOX_BASE_URL if sandbox else PRODUCTION_BASE_URL
        self.base_url = f'{self.base_url}v{api_version}'

        # Token caching and some logic to do better logging.
        self.token_cache = None
        self.token_expires_at = None
        self.token_found_in_cache = False

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

    def _sandbox_error_warning(self):
        self.logger.warning("At the date of last update for this library"
                            " the Hotmart Sandbox API does NOT supported this method.")
        self.logger.warning("This method probably won't work in the Sandbox mode.")
        return

    @staticmethod
    def _build_payload(**kwargs: Any) -> Dict[str, Any]:
        """
        Builds a payload with the given kwargs, ignoring the ones
        with None value
        :param kwargs: Expected kwargs can be found in the "Request parameters"
         section of the API Docs.
        :return: Dict[str, Any]: The built payload as a dictionary.
        """
        payload = {}
        for key, value in kwargs.items():
            if value is not None:
                payload[key] = value
        return payload

    def _log_instance_mode(self) -> None:
        """
        Logs the instance mode (Sandbox or Production).
        :return: None
        """
        return self.logger.warning(
            f"Instance in {'Sandbox' if self.sandbox else 'Production'} mode")

    def _make_request(self,
                      method: Any,
                      url: str,
                      headers: Optional[Dict[str, str]] = None,
                      params: Optional[Dict[str, Any]] = None,
                      body: Optional[Dict[str, str]] = None,
                      log_level: int = None) -> Optional[Dict[str, Any]]:
        """
        Makes a request to the given url.
        :param method: The request method (e.g, requests.get, requests.post).
        :param url: The URL to make the request to.
        :param headers: Optional request headers.
        :param params: Optional request parameters.
        :param log_level: The logging level for this method (default is None,
        inherits from class level).
        :return: The JSON response if the request was successful,
        None otherwise.
        """

        if log_level is not None:
            logger = logging.getLogger(__name__)  # noqa
            logger.setLevel(log_level)

        self.logger.debug(f"Request URL: {url}")
        self.logger.debug(f"Request headers: {headers}")
        self.logger.debug(f"Request params: {params}")
        self.logger.debug(f"Request body: {body}")

        try:
            response = method(url, headers=headers, params=params, data=body)
            self.logger.debug(f"Response content: {response.text}")
            if response.status_code == requests.codes.ok:
                return response.json()
            response.raise_for_status()

        except requests.exceptions.HTTPError as HTTPError:
            # noinspection PyUnboundLocalVariable
            if response.status_code == 401 or response.status_code == 403:
                if self.sandbox:
                    self.logger.error("Perhaps the credentials aren't for Sandbox Mode?")
                else:
                    self.logger.error("Perhaps the credentials aren't for Sandbox Mode?")
                raise HTTPError

            if response.status_code == 422:
                self.logger.error(f"Error {response.status_code}")
                self.logger.error("This usually happens when the request is missing"
                                  " body parameters.")
                raise HTTPError

            if response.status_code == 500 and self.sandbox:
                self.logger.error("This happens with some endpoints in the Sandbox Mode.")
                self.logger.error("Usually the API it's not down, it's just a bug.")

            raise HTTPError

    def _is_token_expired(self) -> bool:
        """
        Checks if the current token has expired.
        :return: True if the token has expired, False otherwise.
        """
        return (self.token_expires_at is not None and self.token_expires_at <
                time.time())

    def _fetch_new_token(self) -> str:
        self.logger.info("Fetching a new access token.")

        method_url = 'https://api-sec-vlc.hotmart.com/security/oauth/token'
        headers = {'Authorization': self.basic}
        payload = {'grant_type': 'client_credentials', 'client_id': self.id,
                   'client_secret': self.secret}

        response = self._make_request(requests.post, method_url,
                                      headers=headers, params=payload)
        self.logger.info("Token obtained successfully")
        return response['access_token']

    def _get_token(self) -> Optional[str]:
        """
        Retrieves an access token to authenticate requests.
        :return: The access token if obtained successfully, otherwise None.
        """
        if not self._is_token_expired() and self.token_cache is not None:
            if not self.token_found_in_cache:
                self.logger.info("Token found in cache.")
                self.token_found_in_cache = True
            return self.token_cache

        self.logger.info("Token not found in cache or expired.")

        token = self._fetch_new_token()
        if token is not None:
            self.token_cache = token
            self.token_found_in_cache = False
        return token

    def _request_with_token(self, method: str, url: str, body: Optional[Dict[str, Any]] = None,
                            params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Makes an authenticated request (GET, POST, PATCH, etc.) to the
        specified URL with the given body or params.
        :param method: The HTTP method (e.g., 'GET', 'POST', 'PATCH').
        :param url: the URL to make the request to.
        :param body: Optional request body.
        :param params: Optional request parameters.
        :return: The JSON Response if successful,
        otherwise raises an exception.
        """
        token = self._get_token()

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        method_mapping = {
            'GET': requests.get,
            'POST': requests.post,
            'PATCH': requests.patch,
            'DELETE': requests.delete
        }

        if method.upper() not in method_mapping:
            raise ValueError(f"Unsupported method: {method}")

        return self._make_request(method_mapping[method.upper()], url, headers=headers,
                                  params=params, body=body)

    def _pagination(self, method: str, url: str, params: Optional[Dict[str, Any]] = None,
                    paginate: bool = False) -> Optional[List[Dict[str, Any]]]:
        """
        Retrieves all pages of data for a paginated endpoint.
        :param url: The URL of the paginated endpoint.
        :param params: Optional request parameters.
        :param paginate: Whether to paginate the results or not
         (default is False).
        :return: A list containing data from all pages,
         or None if an error occurred.
        """
        if not paginate:
            response = self._request_with_token(method=method, url=url, params=params)
            return response.get("items", []) if response else None
        all_items = []

        self.logger.info("Fetching first page...")
        response = self._request_with_token(method=method, url=url, params=params)

        if response is None:
            raise ValueError("Failed to fetch first page.")

        all_items.extend(response.get("items", []))

        while "next_page_token" in response.get("page_info", {}):
            next_page_token = response["page_info"]["next_page_token"]
            self.logger.info(f"Fetching next page with token: {next_page_token}")
            params["page_token"] = next_page_token
            response = self._request_with_token(method, url, params=params)

            if response is None:
                raise ValueError(
                    f"Failed to fetch next page with token: {next_page_token}")

            all_items.extend(response.get("items", []))

        self.logger.info("Finished fetching all pages.")
        return all_items

    def get_sales_history(self, paginate: bool = False, **kwargs: Any) -> Optional[Dict[str, Any]]:
        """
        Retrieves sales history data based on the provided filters.

        :param kwargs: Filters to apply on the request. Expected kwargs can be found in
        the "Request parameters" section of the API Docs.
        :param paginate: Whether to paginate the results or not (default is False).
        :return: Sales history data if available, otherwise None.
        """
        self._log_instance_mode()

        method = "get"
        url = f'{self.base_url}/sales/history'
        payload = self._build_payload(**kwargs)
        return self._pagination(method=method, url=url, params=payload,
                                paginate=paginate)

    def get_sales_summary(self, paginate: bool = False, **kwargs: Any) -> Optional[Dict[str, Any]]:
        """
        Retrieves sales summary data based on the provided filters.

        :param kwargs: Filters to apply on the request. Expected kwargs can be found in the
        "Request parameters" section of the API Docs.
        :param paginate: Whether to paginate the results or not (default is False).
        :return: Sales summary data if available, otherwise None.
        """

        self._log_instance_mode()

        method = "get"
        url = f'{self.base_url}/sales/summary'
        payload = self._build_payload(**kwargs)
        return self._pagination(method=method, url=url, params=payload,
                                paginate=paginate)

    def get_sales_participants(self, paginate: bool = True, **kwargs: Any) -> \
            Optional[Dict[str, Any]]:
        """
        Retrieves sales user data based on the provided filters.

        :param kwargs: Filters to apply on the request. Expected kwargs can be found in the
        "Request parameters" section of the API Docs.
        :param paginate: Whether to paginate the results or not (default is True).
        :return: Sales user data if available, otherwise None.
        """

        self._log_instance_mode()

        method = "get"
        url = f'{self.base_url}/sales/users'
        payload = self._build_payload(**kwargs)
        return self._pagination(method=method, url=url, params=payload, paginate=paginate)

    def get_sales_commissions(self, paginate: bool = False, **kwargs: Any) -> \
            Optional[Dict[str, Any]]:
        """
        Retrieves sales commissions data based on the provided filters.

        :param kwargs: Filters to apply on the request. Expected kwargs can be found in the
        "Request parameters" section of the API Docs.
        :param paginate: Whether to paginate the results or not (default is False).
        :return: Sales commissions data if available, otherwise None.
        """

        self._log_instance_mode()

        method = "get"
        url = f'{self.base_url}/sales/commissions'
        payload = self._build_payload(**kwargs)
        return self._pagination(method=method, url=url, params=payload, paginate=paginate)

    def get_sales_price_details(self, paginate: bool = False, **kwargs: Any) \
            -> Optional[Dict[str, Any]]:
        """
        Retrieves sales price details based on the provided filters.

        :param kwargs: Filters to apply on the request. Expected kwargs can be found in the
        "Request parameters" section of the API Docs.
        :param paginate: Whether to paginate the results or not (default is False).
        :return: Sales price details if available, otherwise None.
        """

        self._log_instance_mode()

        method = "get"
        url = f'{self.base_url}/sales/price/details'
        payload = self._build_payload(**kwargs)
        return self._pagination(method=method, url=url, params=payload, paginate=paginate)

    def get_subscriptions(self, paginate: bool = False, **kwargs: Any) -> \
            Optional[Dict[str, Any]]:
        """
        Retrieves subscription data based on the provided filters.

        :param kwargs: Filters to apply on the request. Expected kwargs can be found in the
        "Request parameters" section of the API Docs.
        :param paginate: Whether to paginate the results or not (default is False).
        :return: Subscription data if available, otherwise None.
        """

        self._log_instance_mode()

        method = "get"
        url = f'{self.base_url}/subscriptions'
        payload = self._build_payload(**kwargs)
        return self._pagination(method=method, url=url, params=payload, paginate=paginate)

    def get_subscriptions_summary(self, paginate: bool = False, **kwargs: Any) -> \
            Optional[Dict[str, Any]]:
        """
        Retrieves subscription summary data based on the provided filters.
        :param paginate: Whether to paginate the results or not (default is False).
        :param kwargs: Filters to apply on the request. Expected kwargs can be found in the
        "Request parameters" section of the API Docs.
        :return: Subscription data if available, otherwise None.
        """

        self._log_instance_mode()

        method = "get"
        url = f'{self.base_url}/subscriptions/summary'
        payload = self._build_payload(**kwargs)
        return self._pagination(method=method, url=url, params=payload, paginate=paginate)

    def get_subscription_purchases(self, subscriber_code, paginate: bool = False, **kwargs: Any) -> \
            Optional[Dict[str, Any]]:
        """
        Retrieves subscription purchases data based on the provided filters.

        :param subscriber_code: The subscriber code to filter the request.
        :param kwargs: Filters to apply on the request. Expected kwargs can be found in the
        "Request parameters" section of the API Docs.
        :param paginate: Whether to paginate the results or not (default is False).
        :return: Subscription purchases data if available, otherwise None.
        """

        self._log_instance_mode()
        if self.sandbox:
            self._sandbox_error_warning()

        method = "get"
        url = f'{self.base_url}/subscriptions/{subscriber_code}/purchases'
        payload = self._build_payload(**kwargs)
        return self._pagination(method=method, url=url, params=payload, paginate=paginate)

    def cancel_subscription(self, subscriber_code: list[str], send_email: bool = True) -> \
            Optional[Dict[str, Any]]:
        """
        Cancels a subscription.

        :param subscriber_code: The subscriber code you want to cancel the subscription
        :param send_email: Whether to email the subscriber or not (default is True).
        :return:
        """

        self._log_instance_mode()
        if self.sandbox:
            self._sandbox_error_warning()

        method = "post"
        url = f'{self.base_url}/subscriptions/cancel'
        payload = {
            "subscriber_code": subscriber_code,
            "send_email": send_email
        }
        return self._request_with_token(method=method, url=url, body=payload)

    def reactivate_and_charge_subscription(self, subscriber_code: list[str], charge: bool = False) \
            -> Optional[Dict[str, Any]]:
        """
        Reactivates and charges a subscription.

        :param subscriber_code: The subscriber code you want to reactivate
        and charge the subscription
        :param charge: Whether to make a new charge to the subscriber or not (default is False).
        :return: A dict containing in
        """

        self._log_instance_mode()
        if self.sandbox:
            self._sandbox_error_warning()

        method = "post"
        url = f'{self.base_url}/subscriptions/reactivate'
        payload = {
            "subscriber_code": subscriber_code,
            "charge": charge
        }
        return self._request_with_token(method=method, url=url, body=payload)

    def change_due_day(self, subscriber_code: str, new_due_day: int) -> Optional[Dict[str, Any]]:
        """
        Changes the due day of a subscription.

        :param subscriber_code: The subscriber code you want to change the due day
        :param new_due_day: The new due day you want to set
        :return: Empty body, just a status code 200 is successful.
        """

        self._log_instance_mode()
        if self.sandbox:
            self._sandbox_error_warning()

        method = "patch"
        url = f'{self.base_url}/subscriptions/change-due-day'
        payload = {
            "subscriber_code": subscriber_code,
            "new_due_day": new_due_day
        }
        return self._request_with_token(method=method, url=url, body=payload)

    def create_coupon(self, product_id: str, coupon_code: str, discount: float) -> \
            Optional[Dict]:
        """
        Creates a coupon for a product.

        :param product_id: UID of the product you want to create the coupon for.
        :param coupon_code: The code of the coupon you want to create.
        :param discount: The discount you want to apply to the coupon, must be greater than 0 and
        less than 0.99.
        :return: Empty body, just a status code 200 is successful.
        """

        self._log_instance_mode()
        if self.sandbox:
            self._sandbox_error_warning()

        method = "post"
        url = f'{self.base_url}/product/{product_id}/coupon'
        payload = {
            "code": coupon_code,
            "discount": discount
        }
        return self._request_with_token(method=method, url=url, body=payload)

    def get_coupon(self, product_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a coupon for a product.

        :param product_id: UID of the product you want to retrieve the coupon for.
        :return: All Coupons for the product.
        """

        self._log_instance_mode()
        if self.sandbox:
            self._sandbox_error_warning()

        method = "get"
        url = f'{self.base_url}/coupon/product/{product_id}'
        return self._request_with_token(method=method, url=url)

    def delete_coupon(self, coupon_id):
        """
        Deletes a coupon.
        :param coupon_id:
        :return: Empty body, just a status code 200 is successful.
        """

        self._log_instance_mode()
        if self.sandbox:
            self._sandbox_error_warning()

        method = "delete"
        url = f'{self.base_url}/coupon/{coupon_id}'
        return self._request_with_token(method=method, url=url)

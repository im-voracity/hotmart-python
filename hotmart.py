import coloredlogs
import requests
import logging
import time
import sys

from typing import List, Dict, Any, Optional

# Base Logging Configs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
coloredlogs.install(logger=logger)
logger.propagate = False

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
    def __init__(self, client_id: str, client_secret: str, basic: str, api_version: int = 1,
                 sandbox: bool = False, log_level: int = logging.CRITICAL) -> None:
        """
        Initializes the Hotmart API client. Full docs can be found at https://developers.hotmart.com/docs/en/
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
        self.base_url = f'{self.base_url}v{api_version}/'

        # Token caching and some logic to do better logging.
        self.token_cache = None
        self.token_expires_at = None
        self.token_found_in_cache = False

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

    @staticmethod
    def _build_payload(**kwargs: Any) -> Dict[str, Any]:
        """
        Builds a payload with the given kwargs, ignoring the ones with None value
        :param kwargs: Expected kwargs can be found in the "Request parameters" section of the API Docs.
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
        return self.logger.info(f"Instance in {'Sandbox' if self.sandbox else 'Production'} mode")

    def _make_request(self, method: Any, url: str, headers: Optional[Dict[str, str]] = None,
                      params: Optional[Dict[str, Any]] = None, log_level: int = None) -> Optional[Dict[str, Any]]:
        """
        Makes a request to the given url.
        :param method: The request method (e.g, requests.get, requests.post).
        :param url: The URL to make the request to.
        :param headers: Optional request headers.
        :param params: Optional request parameters.
        :param log_level: The logging level for this method (default is None, inherits from class level).
        :return: The JSON response if the request was successful, None otherwise.
        """

        if log_level is not None:
            logger = logging.getLogger(__name__)
            logger.setLevel(log_level)
        try:
            self.logger.debug(f"Request URL: {url}")
            self.logger.debug(f"Request headers: {headers}")
            self.logger.debug(f"Request params: {params}")
            response = method(url, headers=headers, params=params)
            self.logger.debug(f"Response content: {response.text}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError:
            # noinspection PyUnboundLocalVariable
            if response.status_code == 403:
                error_message = "Forbidden."
                self.logger.error(f"Error {response.status_code}: {error_message}")
                if self.sandbox:
                    self.logger.error("Check if the provided credentials were created for Sandbox mode.")
                else:
                    self.logger.error("Perhaps the provided credentials are for Sandbox mode?")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error making request to {url}: {e}")
            return None

    def _fetch_new_token(self) -> Optional[Dict[str, Any]]:
        """
        Fetches a new access token.
        :return: The new access token if obtained successfully, otherwise None.
        """
        if self.token_expires_at is not None and self.token_expires_at < time.time():
            self.logger.warning("Current token has expired. Fetching a new one.")
        else:
            self.logger.info("Fetching a new access token.")

        method_url = 'https://api-sec-vlc.hotmart.com/security/oauth/token'
        headers = {'Authorization': self.basic}
        payload = {'grant_type': 'client_credentials', 'client_id': self.id, 'client_secret': self.secret}
        try:
            response = self._make_request(requests.post, method_url, headers=headers, params=payload)
            logger.info("Token obtained successfully")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting token: {e}")
            return None

    def _get_token(self) -> Optional[Dict[str, Any]]:
        """
        Retrieves an access token for making authenticated requests.
        :return: The access token if obtained successfully, otherwise None.
        """
        if self.token_cache is not None and self.token_expires_at is not None:
            current_time = time.time()
            if current_time < self.token_expires_at:
                if not self.token_found_in_cache:
                    self.logger.info("Token found in cache.")
                    self.token_found_in_cache = True
                return self.token_cache

        self.logger.warning("Token not found in cache or expired.")

        token = self._fetch_new_token()
        if token is not None:
            self.token_cache = token  # Armazena o token em cache
            self.token_expires_at = time.time() + token.get('expires_in', 0)  # Calcula o tempo de expiração
            self.token_found_in_cache = False  # Reinicia a variável de controle
        return token

    def _get_with_token(self, url: str, params: Optional[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
        """
        Makes authenticated a GET request to the specified URL with the given params.
        :param url: the URL to make the request to.
        :param params: Optional request parameters.
        :return: The JSON Response if successful, otherwise None.
        """
        token = self._get_token().get('access_token')
        headers = {'Authorization': f'Bearer {token}'}
        return self._make_request(requests.get, url, headers=headers, params=params)

    def _pagination(self, url: str, params: Optional[Dict[str, Any]] = None, paginate: bool = False) -> Optional[
            List[Dict[str, Any]]]:
        """
        Retrieves all pages of data for a paginated endpoint.
        :param url: The URL of the paginated endpoint.
        :param params: Optional request parameters.
        :param paginate: Whether to paginate the results or not (default is False).
        :return: A list containing data from all pages, or None if an error occurred.
        """
        if not paginate:
            return self._get_with_token(url, params=params)
        all_items = []

        self.logger.info("Fetching first page...")
        response = self._get_with_token(url, params=params)

        if response is None:
            self.logger.error("Failed to fetch first page.")
            return None

        all_items.extend(response.get("items", []))

        while "next_page_token" in response.get("page_info", {}):
            next_page_token = response["page_info"]["next_page_token"]
            self.logger.info(f"Fetching next page with token: {next_page_token}")
            params["page_token"] = next_page_token
            response = self._get_with_token(url, params=params)

            if response is None:
                self.logger.error("Failed to fetch next page.")
                return None

            all_items.extend(response.get("items", []))

        self.logger.info("Finished fetching all pages.")
        return all_items

    def get_sales_history(self, paginate: bool = False, **kwargs: Any) -> Optional[Dict[str, Any]]:
        """
        Retrieves sales history data based on the provided filters.
        :param kwargs: Filters to apply on the request. Expected kwargs can be found in the "Request parameters"
        section of the API Docs.
        :param paginate: Whether to paginate the results or not (default is False).
        :return: Sales history data if available, otherwise None.
        """
        self._log_instance_mode()
        method_url = f'{self.base_url}/sales/history'
        payload = self._build_payload(**kwargs)
        return self._pagination(method_url, params=payload, paginate=paginate)

    def get_sales_summary(self, paginate: bool = False, **kwargs: Any) -> Optional[Dict[str, Any]]:
        """
        Retrieves sales summary data based on the provided filters.

        :param kwargs: Filters to apply on the request. Expected kwargs can be found in the "Request parameters"
        section of the API Docs.
        :param paginate: Whether to paginate the results or not (default is False).
        :return: Sales summary data if available, otherwise None.
        """

        self._log_instance_mode()
        method_url = f'{self.base_url}/sales/summary'
        payload = self._build_payload(**kwargs)
        return self._pagination(method_url, params=payload, paginate=paginate)

    def get_sales_users(self, paginate: bool = True, **kwargs: Any) -> Optional[Dict[str, Any]]:
        """
        Retrieves sales user data based on the provided filters.

        :param kwargs: Filters to apply on the request. Expected kwargs can be found in the "Request parameters"
        section of the API Docs.
        :param paginate: Whether to paginate the results or not (default is True).
        :return: Sales user data if available, otherwise None.
        """

        self._log_instance_mode()
        method_url = f'{self.base_url}/sales/users'
        payload = self._build_payload(**kwargs)
        return self._pagination(method_url, params=payload, paginate=paginate)

    def get_sales_commissions(self, paginate: bool = False, **kwargs: Any) -> Optional[Dict[str, Any]]:
        """
        Retrieves sales commissions data based on the provided filters.

        :param kwargs: Filters to apply on the request. Expected kwargs can be found in the "Request parameters"
        section of the API Docs.
        :param paginate: Whether to paginate the results or not (default is False).
        :return: Sales commissions data if available, otherwise None.
        """

        self._log_instance_mode()
        method_url = f'{self.base_url}/sales/commissions'
        payload = self._build_payload(**kwargs)
        return self._pagination(method_url, params=payload, paginate=paginate)

    def get_sales_price_details(self, paginate: bool = False, **kwargs: Any) -> Optional[Dict[str, Any]]:
        """
        Retrieves sales price details based on the provided filters.

        :param kwargs: Filters to apply on the request. Expected kwargs can be found in the "Request parameters"
        section of the API Docs.
        :param paginate: Whether to paginate the results or not (default is False).
        :return: Sales price details if available, otherwise None.
        """

        self._log_instance_mode()
        method_url = f'{self.base_url}/sales/price/details'
        payload = self._build_payload(**kwargs)
        return self._pagination(method_url, params=payload, paginate=paginate)

    def get_subscriptions(self, paginate: bool = False, **kwargs: Any) -> Optional[Dict[str, Any]]:
        """
        Retrieves subscription data based on the provided filters.

        :param kwargs: Filters to apply on the request. Expected kwargs can be found in the "Request parameters"
        section of the API Docs.
        :param paginate: Whether to paginate the results or not (default is False).
        :return: Subscription data if available, otherwise None.
        """

        self._log_instance_mode()
        method_url = f'{self.base_url}/subscriptions'
        payload = self._build_payload(**kwargs)
        return self._pagination(method_url, params=payload, paginate=paginate)

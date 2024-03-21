import requests
import unittest
from unittest.mock import patch
from hotmart_python import Hotmart, RequestException, HTTPRequestException

client_id = 'b32450c1-1352-246a-b6d3-d49d6db815ea'
client_secret = '90bcc221-cebd-5a5b-00e2-72cab47d9282'
basic = ('Basic YjIzNTQxYzAtMyEzNS20MjVhLWI1ZDItZDM4ZDVkYjcwNGVhOjA5Y2JiMTEz'
         'LWRiZWMtNGI0YS05OWUxLTI3Y2FiNDdkOTI4Mg==')


class TestHotmart(unittest.TestCase):
    def setUp(self):
        self.hotmart = Hotmart(client_id=client_id,
                               client_secret=client_secret,
                               basic=basic)

    # Build Payload
    def test_build_payload_with_all_values(self):
        result = self.hotmart._build_payload(key1='value1', key2='value2')
        self.assertEqual(result, {'key1': 'value1', 'key2': 'value2'})

    def test_build_payload_with_none_values(self):
        result = self.hotmart._build_payload(key1='value1', key2=None)
        self.assertEqual(result, {'key1': 'value1'})

    def test_build_payload_with_no_values(self):
        result = self.hotmart._build_payload()
        self.assertEqual(result, {})

    # Sandbox Mode
    def test_sandbox_mode_true(self):
        hotmart = Hotmart(client_id='123', client_secret='123', basic='123',
                          sandbox=True)
        self.assertTrue(hotmart.sandbox)

    def test_sandbox_mode_false(self):
        hotmart1 = Hotmart(client_id='123', client_secret='123', basic='123')
        hotmart2 = Hotmart(client_id='123', client_secret='123', basic='123',
                           sandbox=False)

        self.assertFalse(hotmart1.sandbox)
        self.assertFalse(hotmart2.sandbox)

    @patch('requests.get')
    def test_successful_request(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"success": True}
        response = self.hotmart._make_request(requests.get,
                                              'https://example.com')
        self.assertEqual(response, {"success": True})

    @patch('requests.get')
    def test_http_error_request(self, mock_get):
        mock_get.return_value.raise_for_status.side_effect = (
            requests.exceptions.HTTPError)

        with self.assertRaises(HTTPRequestException):
            self.hotmart._make_request(requests.get, 'https://example.com')

    @patch('requests.get')
    def test_request_exception(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException
        with self.assertRaises(RequestException):
            self.hotmart._make_request(requests.get, 'https://example.com')

    @patch('requests.get')
    def test_forbidden_request_in_sandbox_mode(self, mock_get):
        self.hotmart.sandbox = True
        mock_get.return_value.status_code = 403
        mock_get.return_value.raise_for_status.side_effect = (
            requests.exceptions.HTTPError)

        with self.assertRaises(HTTPRequestException):
            self.hotmart._make_request(requests.get, 'https://example.com')

    @patch('requests.get')
    def test_forbidden_request_in_production_mode(self, mock_get):
        self.hotmart.sandbox = False
        mock_get.return_value.status_code = 403
        mock_get.return_value.raise_for_status.side_effect = (
            requests.exceptions.HTTPError)

        with self.assertRaises(HTTPRequestException):
            self.hotmart._make_request(requests.get, 'https://example.com')

    @patch('time.time')
    def test_token_expired_when_expiry_in_past(self, mock_time):
        mock_time.return_value = 100
        self.hotmart.token_expires_at = 99
        self.assertTrue(self.hotmart._is_token_expired())

    @patch('time.time')
    def test_token_not_expired_when_expiry_in_future(self, mock_time):
        mock_time.return_value = 100
        self.hotmart.token_expires_at = 101
        self.assertFalse(self.hotmart._is_token_expired())

    @patch('requests.post')
    def test_token_obtained_successfully(self, mock_post):
        mock_post.return_value.json.return_value = {
            'access_token': 'test_token'}
        token = self.hotmart._fetch_new_token()
        self.assertEqual(token, 'test_token')

    @patch('requests.post')
    def test_token_obtained_failure(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException
        with self.assertRaises(RequestException):
            self.hotmart._fetch_new_token()

    @patch.object(Hotmart, '_is_token_expired')
    @patch.object(Hotmart, '_fetch_new_token')
    def test_token_found_in_cache(self, mock_fetch_new_token,
                                  mock_is_token_expired):
        mock_is_token_expired.return_value = False
        self.hotmart.token_cache = 'test_token'
        token = self.hotmart._get_token()
        self.assertEqual(token, 'test_token')
        mock_fetch_new_token.assert_not_called()

    @patch.object(Hotmart, '_is_token_expired')
    @patch.object(Hotmart, '_fetch_new_token')
    def test_token_not_in_cache_and_fetched_success(self,
                                                    mock_fetch_new_token,
                                                    mock_is_token_expired):
        mock_is_token_expired.return_value = True
        mock_fetch_new_token.return_value = 'new_token'
        token = self.hotmart._get_token()
        self.assertEqual(token, 'new_token')

    @patch.object(Hotmart, '_is_token_expired')
    @patch.object(Hotmart, '_fetch_new_token')
    def test_token_not_in_cache_and_fetch_failed(self, mock_fetch_new_token,
                                                 mock_is_token_expired):
        mock_is_token_expired.return_value = True
        mock_fetch_new_token.return_value = None
        token = self.hotmart._get_token()
        self.assertIsNone(token)

    @patch.object(Hotmart, '_get_token')
    @patch.object(Hotmart, '_make_request')
    def test_successful_request_with_token(self, mock_make_request,
                                           mock_get_token):
        mock_get_token.return_value = 'test_token'
        mock_make_request.return_value = {"success": True}
        result = self.hotmart._request_with_token('GET',
                                                  'https://example.com')
        self.assertEqual(result, {"success": True})

    @patch.object(Hotmart, '_get_token')
    @patch.object(Hotmart, '_make_request')
    def test_failed_request_with_token(self, mock_make_request,
                                       mock_get_token):
        mock_get_token.return_value = 'test_token'
        mock_make_request.side_effect = RequestException("Error",
                                                         "url")
        with self.assertRaises(RequestException):
            self.hotmart._request_with_token('GET',
                                             'https://example.com')

    @patch.object(Hotmart, '_get_token')
    def test_unsupported_method_with_token(self,
                                           mock_get_token):
        mock_get_token.return_value = 'test_token'
        with self.assertRaises(ValueError):
            self.hotmart._request_with_token('PUT',
                                             'https://example.com')

    @patch.object(Hotmart, '_request_with_token')
    def test_pagination_without_pagination(self, mock_request_with_token):
        mock_request_with_token.return_value = {
            "items": ["item1", "item2"]
        }
        result = self.hotmart._pagination('GET',
                                          'https://example.com')

        self.assertEqual(result, ["item1", "item2"])

    @patch.object(Hotmart, '_request_with_token')
    def test_pagination_with_single_page(self, mock_request_with_token):
        mock_request_with_token.return_value = {
            "items": ["item1", "item2"],
            "page_info": {}
        }

        result = self.hotmart._pagination('GET',
                                          'https://example.com',
                                          paginate=True)

        self.assertEqual(result, ["item1", "item2"])

    @patch.object(Hotmart, '_request_with_token')
    def test_pagination_with_multiple_pages(self, mock_request_with_token):
        mock_request_with_token.side_effect = [
            {
                "items": ["item1", "item2"],
                "page_info": {"next_page_token": "token"}
            },
            {
                "items": ["item3", "item4"],
                "page_info": {}
            }
        ]
        params = {}
        result = self.hotmart._pagination('GET',
                                          'https://example.com',
                                          params=params,
                                          paginate=True)

        self.assertEqual(result, ["item1", "item2", "item3", "item4"])

    @patch.object(Hotmart, '_request_with_token')
    def test_pagination_with_failed_first_page(self, mock_request_with_token):
        mock_request_with_token.return_value = None

        with self.assertRaises(ValueError):
            self.hotmart._pagination('GET',
                                     'https://example.com',
                                     paginate=True)


if __name__ == '__main__':
    unittest.main()

import requests
import unittest
from unittest.mock import patch
from hotmart_python import Hotmart

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

    def test_build_payload_with_valid_arguments(self):
        """
        None values should be ignored
        """
        result = self.hotmart._build_payload(buyer_email='test@example.com',
                                             purchase_value=123,
                                             is_buyer=True,
                                             param4=None)

        # Assert
        self.assertEqual(result, {
            "buyer_email": "test@example.com",
            "purchase_value": 123,
            "is_buyer": True
        })

    def test_build_payload_with_no_arguments(self):
        result = self.hotmart._build_payload()
        self.assertEqual(result, {})

    def test_build_url_with_valid_endpoint_payments(self):
        result = self.hotmart._build_url('payments')
        expected_result = 'https://developers.hotmart.com/payments/api/v1'
        self.assertEqual(result, expected_result)

    def test_build_url_with_valid_endpoint_club(self):
        result = self.hotmart._build_url('club')
        expected_result = 'https://developers.hotmart.com/club/api/v1'
        self.assertEqual(result, expected_result)

    def test_build_url_with_valid_endpoint_sandbox_payments(self):
        self.hotmart.sandbox = True
        result = self.hotmart._build_url('payments')
        expected_result = 'https://sandbox.hotmart.com/payments/api/v1'
        self.assertEqual(result, expected_result)

    def test_build_url_with_valid_endpoint_sandbox_club(self):
        self.hotmart.sandbox = True
        result = self.hotmart._build_url('club')
        expected_result = 'https://sandbox.hotmart.com/club/api/v1'
        self.assertEqual(result, expected_result)

    def test_build_url_with_invalid_endpoint(self):
        with self.assertRaises(ValueError):
            self.hotmart._build_url('invalid_endpoint')

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

        with self.assertRaises(requests.exceptions.HTTPError):
            self.hotmart._make_request(requests.get, 'https://example.com')

    @patch('requests.get')
    def test_request_exception(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException
        with self.assertRaises(requests.exceptions.RequestException):
            self.hotmart._make_request(requests.get, 'https://example.com')

    @patch('requests.get')
    def test_forbidden_request_in_sandbox_mode(self, mock_get):
        self.hotmart.sandbox = True
        mock_get.return_value.status_code = 403
        mock_get.return_value.raise_for_status.side_effect = (
            requests.exceptions.HTTPError)

        with self.assertRaises(requests.exceptions.HTTPError):
            self.hotmart._make_request(requests.get, 'https://example.com')

    @patch('requests.get')
    def test_forbidden_request_in_production_mode(self, mock_get):
        self.hotmart.sandbox = False
        mock_get.return_value.status_code = 403
        mock_get.return_value.raise_for_status.side_effect = (
            requests.exceptions.HTTPError)

        with self.assertRaises(requests.exceptions.HTTPError):
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

    @patch.object(Hotmart, '_make_request')
    def test_token_obtained_successfully(self, mock_make_request):
        mock_make_request.return_value = {
            'access_token': 'test_token'
        }
        token = self.hotmart._fetch_new_token()
        self.assertEqual(token, 'test_token')

    @patch('requests.post')
    def test_token_obtained_failure(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException
        with self.assertRaises(requests.exceptions.RequestException):
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
    def test_token_not_in_cache_and_fetch_failed(self, mock_fetch_new_token, mock_is_token_expired):
        mock_is_token_expired.return_value = True
        mock_fetch_new_token.return_value = None
        token = self.hotmart._get_token()
        self.assertIsNone(token)

    @patch.object(Hotmart, '_get_token')
    @patch.object(Hotmart, '_make_request')
    def test_successful_request_with_token(self, mock_make_request, mock_get_token):
        mock_get_token.return_value = 'test_token'
        mock_make_request.return_value = {"success": True}
        result = self.hotmart._request_with_token('GET', 'https://example.com')
        self.assertEqual(result, {"success": True})

    @patch.object(Hotmart, '_get_token')
    @patch.object(Hotmart, '_make_request')
    def test_failed_request_with_token(self, mock_make_request,
                                       mock_get_token):
        mock_get_token.return_value = 'test_token'
        mock_make_request.side_effect = requests.exceptions.RequestException
        with self.assertRaises(requests.exceptions.RequestException):
            self.hotmart._request_with_token('GET', 'https://example.com')

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

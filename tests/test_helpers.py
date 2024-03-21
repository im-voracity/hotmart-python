import requests
import unittest
from unittest.mock import patch
from hotmart_python import Hotmart


class TestHotmart(unittest.TestCase):
    def setUp(self):
        self.hotmart = Hotmart(client_id='b32450c1-1352-246a-b6d3-d49d6db815ea',
                               client_secret='90bcc221-cebd-5a5b-00e2-72cab47d9282',
                               basic='Basic '
                                     'YjIzNTQxYzAtMyEzNS20MjVhLWI1ZDItZDM4ZDVkYjcwNGVhOjA5Y2JiMTEzLWRiZWMtNGI0YS05OWUx'
                                     'LTI3Y2FiNDdkOTI4Mg==')

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
        hotmart = Hotmart(client_id="123", client_secret="123", basic="123", sandbox=True)
        self.assertTrue(hotmart.sandbox)

    def test_sandbox_mode_false(self):
        hotmart1 = Hotmart(client_id="123", client_secret="123", basic="123")
        hotmart2 = Hotmart(client_id="123", client_secret="123", basic="123", sandbox=False)

        arr = [hotmart1, hotmart2]

        for hotmart in arr:
            self.assertFalse(hotmart.sandbox)

    @patch('requests.get')
    def test_successful_request_with_get_method(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"success": True}
        response = self.hotmart._make_request(requests.get, 'https://testurl.com', headers={}, params={})
        self.assertEqual(response, {"success": True})

    @patch('requests.post')
    def test_successful_request_with_post_method(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"success": True}
        response = self.hotmart._make_request(requests.post, 'https://testurl.com', headers={}, params={})
        self.assertEqual(response, {"success": True})

    @patch('requests.get')
    def test_request_with_http_error(self, mock_get):
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError
        response = self.hotmart._make_request(requests.get, 'https://testurl.com', headers={}, params={})
        self.assertIsNone(response)

    @patch('requests.get')
    def test_request_with_request_exception(self, mock_get):
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.RequestException
        response = self.hotmart._make_request(requests.get, 'https://testurl.com', headers={}, params={})
        self.assertIsNone(response)

    def test_token_is_expired_when_token_expires_at_is_none(self):
        self.hotmart.token_expires_at = None
        self.assertFalse(self.hotmart._is_token_expired())

    @patch('time.time')
    def test_token_is_expired_when_token_expires_at_is_in_the_future(self, mock_time):
        mock_time.return_value = 1000
        self.hotmart.token_expires_at = 2000
        self.assertFalse(self.hotmart._is_token_expired())

    @patch('time.time')
    def test_token_is_expired_when_token_expires_at_is_in_the_past(self, mock_time):
        mock_time.return_value = 3000
        self.hotmart.token_expires_at = 2000
        self.assertTrue(self.hotmart._is_token_expired())
    
    @patch('requests.post')
    def test_successful_token_fetch(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'access_token': 'abc123'
        }
        response = self.hotmart._fetch_new_token()
        self.assertEqual(response, 'abc123')

    @patch('requests.post')
    def test_failed_token_fetch_due_to_request_exception(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException
        response = self.hotmart._fetch_new_token()
        self.assertIsNone(response)

    @patch.object(Hotmart, '_is_token_expired')
    @patch.object(Hotmart, '_fetch_new_token')
    def test_token_retrieval_when_token_not_expired_and_in_cache(self, mock_fetch_new_token, mock_is_token_expired):
        mock_is_token_expired.return_value = False
        self.hotmart.token_cache = "abc123"
        self.hotmart.token_found_in_cache = False
        result = self.hotmart._get_token()
        self.assertEqual(result, "abc123")
        mock_fetch_new_token.assert_not_called()

    @patch.object(Hotmart, '_is_token_expired')
    @patch.object(Hotmart, '_fetch_new_token')
    def test_token_retrieval_when_token_expired_and_in_cache(self, mock_fetch_new_token, mock_is_token_expired):
        mock_is_token_expired.return_value = True
        self.hotmart.token_cache = "abc123"
        mock_fetch_new_token.return_value = "def456"
        result = self.hotmart._get_token()
        self.assertEqual(result, "def456")

    @patch.object(Hotmart, '_is_token_expired')
    @patch.object(Hotmart, '_fetch_new_token')
    def test_token_retrieval_when_token_not_in_cache(self, mock_fetch_new_token, mock_is_token_expired):
        mock_is_token_expired.return_value = True
        self.hotmart.token_cache = None
        mock_fetch_new_token.return_value = "def456"
        result = self.hotmart._get_token()
        self.assertEqual(result, "def456")

    @patch.object(Hotmart, '_is_token_expired')
    @patch.object(Hotmart, '_fetch_new_token')
    def test_token_retrieval_when_fetch_new_token_returns_none(self, mock_fetch_new_token, mock_is_token_expired):
        mock_is_token_expired.return_value = True
        self.hotmart.token_cache = None
        mock_fetch_new_token.return_value = None
        result = self.hotmart._get_token()
        self.assertIsNone(result)

    @patch.object(Hotmart, '_request_with_token')
    def test_successful_get_with_token(self, mock_request_with_token):
        mock_request_with_token.return_value = {"success": True}
        result = self.hotmart._request_with_token('GET', 'https://testurl.com')
        self.assertEqual(result, {"success": True})

    @patch.object(Hotmart, '_request_with_token')
    def test_get_with_token_when_make_request_returns_none(self, mock_request_with_token):
        mock_request_with_token.return_value = None
        result = self.hotmart._request_with_token('GET', 'https://testurl.com')
        self.assertIsNone(result)

    @patch.object(Hotmart, '_request_with_token')
    def test_get_with_token_when_get_token_returns_none(self, mock_request_with_token):
        mock_request_with_token.return_value = None
        result = self.hotmart._request_with_token('GET', 'https://testurl.com')
        self.assertIsNone(result)

    @patch.object(Hotmart, '_request_with_token')
    def test_pagination_with_no_pagination(self, mock_request_with_token):
        mock_request_with_token.return_value = {"items": [{"id": 5}, {"id": 6}], "page_info": {}}
        result = self.hotmart._pagination('GET', 'https://testurl.com', params={}, paginate=False)
        self.assertEqual(result, {"items": [{"id": 5}, {"id": 6}], "page_info": {}})

    @patch.object(Hotmart, '_request_with_token')
    def test_pagination_with_successful_pagination(self, mock_request_with_token):
        mock_request_with_token.side_effect = [
            {"items": [{"id": 1}, {"id": 2}], "page_info": {"next_page_token": "token1"}},
            {"items": [{"id": 3}, {"id": 4}], "page_info": {"next_page_token": "token2"}},
            {"items": [{"id": 5}, {"id": 6}], "page_info": {}}
        ]
        result = self.hotmart._pagination('GET', 'http://testurl.com', params={}, paginate=True)
        self.assertEqual(result, [{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}, {"id": 5}, {"id": 6}])

    @patch.object(Hotmart, '_request_with_token')
    def test_pagination_with_failed_first_page_fetch(self, mock_request_with_token):
        mock_request_with_token.return_value = None
        result = self.hotmart._pagination('GET', 'https://testurl.com', params={}, paginate=True)
        self.assertIsNone(result)

    @patch.object(Hotmart, '_request_with_token')
    def test_pagination_with_failed_next_page_fetch(self, mock_request_with_token):
        mock_request_with_token.side_effect = [
            {"items": [{"id": 1}, {"id": 2}], "page_info": {"next_page_token": "token1"}},
            None
        ]
        result = self.hotmart._pagination('GET', 'https://testurl.com', params={}, paginate=True)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()

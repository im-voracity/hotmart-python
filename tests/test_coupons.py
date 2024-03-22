import unittest
import requests.exceptions
from unittest.mock import patch
from hotmart_python import Hotmart

client_id = 'b32450c1-1352-246a-b6d3-d49d6db815ea'
client_secret = '90bcc221-cebd-5a5b-00e2-72cab47d9282'
basic = ('Basic YjIzNTQxYzAtMyEzNS20MjVhLWI1ZDItZDM4ZDVkYjcwNGVhOjA5Y2JiMTEzLWRiZWMtNGI0YS05OWUxLT\
I3Y2FiNDdkOTI4Mg==')


class TestHotmart(unittest.TestCase):
    def setUp(self):
        self.hotmart = Hotmart(client_id=client_id,
                               client_secret=client_secret,
                               basic=basic)

    @patch.object(Hotmart, '_request_with_token')
    def test_create_coupon_successfully(self, mock_request_with_token):
        mock_request_with_token.return_value = {}
        result = self.hotmart.create_coupon('product_id',
                                            'coupon_code',
                                            0.5)

        self.assertEqual(result, {})

    @patch.object(Hotmart, '_request_with_token')
    def test_create_coupon_with_invalid_discount(self, mock_request_with_token):
        mock_request_with_token.side_effect = requests.exceptions.HTTPError
        with self.assertRaises(requests.exceptions.HTTPError):
            self.hotmart.create_coupon('product_id',
                                       'coupon_code',
                                       1.5)

    @patch.object(Hotmart, '_request_with_token')
    def test_create_coupon_with_negative_discount(self, mock_request_with_token):
        mock_request_with_token.side_effect = requests.exceptions.HTTPError
        with self.assertRaises(requests.exceptions.HTTPError):
            self.hotmart.create_coupon('product_id', 'coupon_code', -0.5)

    @patch.object(Hotmart, '_request_with_token')
    def test_create_coupon_with_zero_discount(self, mock_request_with_token):
        mock_request_with_token.side_effect = requests.exceptions.HTTPError
        with self.assertRaises(requests.exceptions.HTTPError):
            self.hotmart.create_coupon('product_id', 'coupon_code', 0)

    @patch.object(Hotmart, '_request_with_token')
    def test_create_coupon_with_request_exception(self, mock_request_with_token):
        mock_request_with_token.side_effect = requests.exceptions.RequestException

        with self.assertRaises(requests.exceptions.RequestException):
            self.hotmart.create_coupon('product_id',
                                       'coupon_code',
                                       0.5)

    @patch.object(Hotmart, '_request_with_token')
    def test_get_coupon_successfully(self, mock_request_with_token):
        mock_request_with_token.return_value = {"coupon": "COUPON_CODE"}
        result = self.hotmart.get_coupon('product_id')
        self.assertEqual(result, {"coupon": "COUPON_CODE"})

    @patch.object(Hotmart, '_request_with_token')
    def test_get_coupon_with_invalid_product_id(self, mock_request_with_token):
        mock_request_with_token.side_effect = requests.exceptions.HTTPError
        with self.assertRaises(requests.exceptions.HTTPError):
            self.hotmart.get_coupon('invalid_product_id')

    @patch.object(Hotmart, '_request_with_token')
    def test_get_coupon_with_request_exception(self, mock_request_with_token):
        mock_request_with_token.side_effect = requests.exceptions.RequestException
        with self.assertRaises(requests.exceptions.RequestException):
            self.hotmart.get_coupon('product_id')

    @patch.object(Hotmart, '_request_with_token')
    def test_delete_coupon_successfully(self, mock_request_with_token):
        mock_request_with_token.return_value = {}

        result = self.hotmart.delete_coupon('coupon_id')
        self.assertEqual(result, {})

    @patch.object(Hotmart, '_request_with_token')
    def test_delete_coupon_with_invalid_coupon_id(self, mock_request_with_token):
        mock_request_with_token.side_effect = requests.exceptions.HTTPError

        with self.assertRaises(requests.exceptions.HTTPError):
            self.hotmart.delete_coupon('invalid_coupon_id')

    @patch.object(Hotmart, '_request_with_token')
    def test_delete_coupon_with_request_exception(self, mock_request_with_token):
        mock_request_with_token.side_effect = requests.exceptions.RequestException
        with self.assertRaises(requests.exceptions.RequestException):
            self.hotmart.delete_coupon('coupon_id')

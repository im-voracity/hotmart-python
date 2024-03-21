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

    @patch.object(Hotmart, '_request_with_token')
    def test_should_retrieve_subscriptions_when_valid_request(self, mock_request_with_token):
        mock_request_with_token.return_value = {"subscriptions": [{"id": 1}, {"id": 2}]}
        result = self.hotmart.get_subscriptions(paginate=False)
        self.assertEqual(result, {"subscriptions": [{"id": 1}, {"id": 2}]})

    @patch.object(Hotmart, '_request_with_token')
    def test_should_return_none_when_retrieving_subscriptions_fails(self, mock_request_with_token):
        mock_request_with_token.return_value = None
        result = self.hotmart.get_subscriptions(paginate=False)
        self.assertIsNone(result)

    @patch.object(Hotmart, '_request_with_token')
    def test_should_retrieve_subscription_summary_when_valid_request(self, mock_request_with_token):
        mock_request_with_token.return_value = {"summary": {"total": 10}}
        result = self.hotmart.get_subscriptions_summary(paginate=False)
        self.assertEqual(result, {"summary": {"total": 10}})

    @patch.object(Hotmart, '_request_with_token')
    def test_should_return_none_when_retrieving_subscription_summary_fails(self, mock_request_with_token):
        mock_request_with_token.return_value = None
        result = self.hotmart.get_subscriptions_summary(paginate=False)
        self.assertIsNone(result)

    @patch.object(Hotmart, '_request_with_token')
    def test_should_retrieve_subscription_purchases_when_valid_request(self, mock_request_with_token):
        mock_request_with_token.return_value = {"purchases": [{"id": 1}, {"id": 2}]}
        result = self.hotmart.get_subscription_purchases(subscriber_code="123", paginate=False)
        self.assertEqual(result, {"purchases": [{"id": 1}, {"id": 2}]})

    @patch.object(Hotmart, '_request_with_token')
    def test_should_return_none_when_retrieving_subscription_purchases_fails(self, mock_request_with_token):
        mock_request_with_token.return_value = None
        result = self.hotmart.get_subscription_purchases(subscriber_code="123", paginate=False)
        self.assertIsNone(result)

    @patch.object(Hotmart, '_request_with_token')
    def test_should_cancel_subscription_when_valid_request(self, mock_request_with_token):
        mock_request_with_token.return_value = {"status": "cancelled"}
        result = self.hotmart.cancel_subscription(subscriber_code=["123"], send_email=True)
        self.assertEqual(result, {"status": "cancelled"})

    @patch.object(Hotmart, '_request_with_token')
    def test_should_return_none_when_cancelling_subscription_fails(self, mock_request_with_token):
        mock_request_with_token.return_value = None
        result = self.hotmart.cancel_subscription(subscriber_code=["123"], send_email=True)
        self.assertIsNone(result)

    @patch.object(Hotmart, '_request_with_token')
    def test_should_reactivate_and_charge_subscription_when_valid_request(self, mock_request_with_token):
        mock_request_with_token.return_value = {"status": "reactivated"}
        result = self.hotmart.reactivate_and_charge_subscription(subscriber_code=["123"], charge=True)
        self.assertEqual(result, {"status": "reactivated"})

    @patch.object(Hotmart, '_request_with_token')
    def test_should_return_none_when_reactivating_and_charging_subscription_fails(self, mock_request_with_token):
        mock_request_with_token.return_value = None
        result = self.hotmart.reactivate_and_charge_subscription(subscriber_code=["123"], charge=True)
        self.assertIsNone(result)

    @patch.object(Hotmart, '_request_with_token')
    def test_should_change_due_day_when_valid_request(self, mock_request_with_token):
        mock_request_with_token.return_value = {"status": "due day changed"}
        result = self.hotmart.change_due_day(subscriber_code="123", new_due_day=15)
        self.assertEqual(result, {"status": "due day changed"})

    @patch.object(Hotmart, '_request_with_token')
    def test_should_return_none_when_changing_due_day_fails(self, mock_request_with_token):
        mock_request_with_token.return_value = None
        result = self.hotmart.change_due_day(subscriber_code="123", new_due_day=15)
        self.assertIsNone(result)

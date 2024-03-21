import unittest
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

    @patch.object(Hotmart, '_build_payload')
    @patch.object(Hotmart, '_pagination')
    def test_get_sales_history_with_pagination(self, mock_pagination, mock_build_payload):
        mock_build_payload.return_value = {"transaction_status": "approved"}
        mock_pagination.return_value = [{"id": 1}, {"id": 2}]
        result = self.hotmart.get_sales_history(paginate=True, transaction_status="approved")

        self.assertEqual(result, [{"id": 1}, {"id": 2}])

    @patch.object(Hotmart, '_build_payload')
    @patch.object(Hotmart, '_pagination')
    def test_get_sales_history_no_pagination(self, mock_pagination, mock_build_payload):
        mock_build_payload.return_value = {"filter1": "value1"}
        mock_pagination.return_value = [{"id": 1}, {"id": 2}]
        result = self.hotmart.get_sales_history(paginate=False, filter1="value1")
        self.assertEqual(result, [{"id": 1}, {"id": 2}])

    @patch.object(Hotmart, '_build_payload')
    @patch.object(Hotmart, '_pagination')
    def test_get_sales_history_with_failed_pagination(self, mock_pagination, mock_build_payload):
        mock_build_payload.return_value = {"filter1": "value1"}
        mock_pagination.return_value = None
        result = self.hotmart.get_sales_history(paginate=True, filter1="value1")

        self.assertIsNone(result)

    @patch.object(Hotmart, '_build_payload')
    @patch.object(Hotmart, '_pagination')
    def test_get_sales_summary_with_pagination(self, mock_pagination, mock_build_payload):
        mock_build_payload.return_value = {
            "filter1": "value1"
        }
        mock_pagination.return_value = [
            {"id": 1},
            {"id": 2}
        ]
        result = self.hotmart.get_sales_summary(paginate=True, filter1="value1")

        self.assertEqual(result, [
            {"id": 1},
            {"id": 2}
        ])

    @patch.object(Hotmart, '_build_payload')
    @patch.object(Hotmart, '_pagination')
    def test_get_sales_summary_no_pagination(self, mock_pagination, mock_build_payload):
        mock_build_payload.return_value = {
            "filter1": "value1"
        }
        mock_pagination.return_value = [
            {"id": 1},
            {"id": 2}
        ]
        result = self.hotmart.get_sales_summary(paginate=False, filter1="value1")

        self.assertEqual(result, [
            {"id": 1},
            {"id": 2}
        ])

    @patch.object(Hotmart, '_build_payload')
    @patch.object(Hotmart, '_pagination')
    def test_get_sales_summary_with_failed_pagination(self, mock_pagination, mock_build_payload):
        mock_build_payload.return_value = {
            "filter1": "value1"
        }
        mock_pagination.return_value = None
        result = self.hotmart.get_sales_summary(paginate=True, filter1="value1")

        self.assertIsNone(result)

    @patch.object(Hotmart, '_build_payload')
    @patch.object(Hotmart, '_pagination')
    def test_sales_participants_retrieval_with_pagination(self, mock_pagination,
                                                          mock_build_payload):
        mock_build_payload.return_value = {
            "filter1": "value1"
        }
        mock_pagination.return_value = [
            {"id": 1},
            {"id": 2}
        ]
        result = self.hotmart.get_sales_participants(paginate=True, filter1="value1")

        self.assertEqual(result, [
            {"id": 1},
            {"id": 2}
        ])

    @patch.object(Hotmart, '_build_payload')
    @patch.object(Hotmart, '_pagination')
    def test_sales_participants_retrieval_no_pagination(self, mock_pagination, mock_build_payload):
        mock_build_payload.return_value = {
            "filter1": "value1"
        }
        mock_pagination.return_value = [
            {"id": 1},
            {"id": 2}
        ]
        result = self.hotmart.get_sales_participants(paginate=False, filter1="value1")

        self.assertEqual(result, [
            {"id": 1},
            {"id": 2}
        ])

    @patch.object(Hotmart, '_build_payload')
    @patch.object(Hotmart, '_pagination')
    def test_sales_participants_retrieval_failed_pagination(self, mock_pagination,
                                                            mock_build_payload):
        mock_build_payload.return_value = {
            "filter1": "value1"
        }
        mock_pagination.return_value = None
        result = self.hotmart.get_sales_participants(paginate=True, filter1="value1")

        self.assertIsNone(result)

    @patch.object(Hotmart, '_build_payload')
    @patch.object(Hotmart, '_pagination')
    def test_sales_commissions_retrieval_with_pagination(self, mock_pagination, mock_build_payload):
        mock_build_payload.return_value = {
            "filter1": "value1"
        }
        mock_pagination.return_value = [
            {"id": 1},
            {"id": 2}
        ]
        result = self.hotmart.get_sales_commissions(paginate=True, filter1="value1")

        self.assertEqual(result, [
            {"id": 1},
            {"id": 2}
        ])

    @patch.object(Hotmart, '_build_payload')
    @patch.object(Hotmart, '_pagination')
    def test_sales_commissions_retrieval_no_pagination(self, mock_pagination, mock_build_payload):
        mock_build_payload.return_value = {
            "filter1": "value1"
        }
        mock_pagination.return_value = [
            {"id": 1},
            {"id": 2}
        ]
        result = self.hotmart.get_sales_commissions(paginate=False, filter1="value1")

        self.assertEqual(result, [
            {"id": 1},
            {"id": 2}
        ])

    @patch.object(Hotmart, '_build_payload')
    @patch.object(Hotmart, '_pagination')
    def test_sales_commissions_retrieval_failed_pagination(self, mock_pagination,
                                                           mock_build_payload):
        mock_build_payload.return_value = {
            "filter1": "value1"
        }
        mock_pagination.return_value = None
        result = self.hotmart.get_sales_commissions(paginate=True, filter1="value1")

        self.assertIsNone(result)

    @patch.object(Hotmart, '_build_payload')
    @patch.object(Hotmart, '_pagination')
    def test_sales_price_details_retrieval_with_pagination(self, mock_pagination,
                                                           mock_build_payload):
        mock_build_payload.return_value = {
            "filter1": "value1"
        }
        mock_pagination.return_value = [
            {"id": 1},
            {"id": 2}
        ]
        result = self.hotmart.get_sales_price_details(paginate=True, filter1="value1")
        self.assertEqual(result, [
            {"id": 1},
            {"id": 2}
        ])

    @patch.object(Hotmart, '_build_payload')
    @patch.object(Hotmart, '_pagination')
    def test_sales_price_details_retrieval_no_pagination(self, mock_pagination, mock_build_payload):
        mock_build_payload.return_value = {
            "filter1": "value1"
        }
        mock_pagination.return_value = [
            {"id": 1},
            {"id": 2}
        ]
        result = self.hotmart.get_sales_price_details(paginate=False, filter1="value1")
        self.assertEqual(result, [
            {"id": 1},
            {"id": 2}
        ])

    @patch.object(Hotmart, '_build_payload')
    @patch.object(Hotmart, '_pagination')
    def test_sales_price_details_retrieval_failed_pagination(self, mock_pagination,
                                                             mock_build_payload):
        mock_build_payload.return_value = {
            "filter1": "value1"
        }
        mock_pagination.return_value = None
        result = self.hotmart.get_sales_price_details(paginate=True, filter1="value1")

        self.assertIsNone(result)

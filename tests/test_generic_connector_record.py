import json
import unittest
from unittest.mock import patch, MagicMock

import boomi_cicd


class TestGenericConnectorRecord(unittest.TestCase):
    @patch("boomi_cicd.atomsphere_request")
    def test_get_generic_connector_record(self, mock_post):
        generic_connector_record_id = "123456789"
        mock_post.return_value.text = json.dumps({"id": generic_connector_record_id})
        boomi_cicd.get_generic_connector_record(generic_connector_record_id)
        mock_post.assert_called_with(
            method="get",
            resource_path=f"/GenericConnectorRecord/{generic_connector_record_id}",
        )

    @patch("boomi_cicd.atomsphere_request")
    def test_get_generic_connector_record_invalid_json(self, mock_post):
        # Test for handling invalid JSON response
        generic_connector_record_id = "123456789"
        mock_post.return_value.text = "invalid json"

        with self.assertRaises(ValueError):
            boomi_cicd.get_generic_connector_record(generic_connector_record_id)

        mock_post.assert_called_with(
            method="get",
            resource_path=f"/GenericConnectorRecord/{generic_connector_record_id}",
        )

    @patch("boomi_cicd.atomsphere_request")
    @patch("time.sleep", return_value=None)  # To avoid actual sleeping during the test
    def test_query_generic_connector_record_success(self, mock_sleep, mock_post):
        execution_id = "execution-123"
        execution_connector_id = "connector-456"
        payload = {
            "QueryFilter": {
                "expression": {
                    "operator": "and",
                    "nestedExpression": [
                        {
                            "argument": [execution_id],
                            "operator": "EQUALS",
                            "property": "executionId",
                        },
                        {
                            "argument": [execution_connector_id],
                            "operator": "EQUALS",
                            "property": "executionConnectorId",
                        },
                    ],
                }
            }
        }

        expected_response = {"numberOfResults": 1, "records": ["some_record"]}

        # Mock responses for the atomsphere_request
        response_1 = MagicMock()
        response_1.text = json.dumps({"numberOfResults": 0})
        response_2 = MagicMock()
        response_2.text = json.dumps(expected_response)

        mock_post.side_effect = [response_1, response_2]

        # Call the function under test
        boomi_cicd.query_generic_connector_record(execution_id, execution_connector_id)

        mock_post.assert_called_with(
            method="post",
            resource_path="/GenericConnectorRecord/query",
            payload=payload,
        )
        self.assertEqual(mock_post.call_count, 2)

    @patch("boomi_cicd.atomsphere_request")
    def test_query_generic_connector_record_timeout(self, mock_post):
        execution_id = "execution-123"
        execution_connector_id = "connector-456"
        payload = {
            "QueryFilter": {
                "expression": {
                    "operator": "and",
                    "nestedExpression": [
                        {
                            "argument": [execution_id],
                            "operator": "EQUALS",
                            "property": "executionId",
                        },
                        {
                            "argument": [execution_connector_id],
                            "operator": "EQUALS",
                            "property": "executionConnectorId",
                        },
                    ],
                }
            }
        }

        mock_post.return_value.text = json.dumps({"numberOfResults": 0})

        boomi_cicd.query_generic_connector_record(
            execution_id, execution_connector_id, request_interval_sec=1, max_wait_sec=5
        )

        mock_post.assert_called_with(
            method="post",
            resource_path="/GenericConnectorRecord/query",
            payload=payload,
        )
        self.assertEqual(mock_post.call_count, 5)

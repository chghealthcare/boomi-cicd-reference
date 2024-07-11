import unittest
from unittest.mock import patch, MagicMock

import boomi_cicd


class TestExecutionConnector(unittest.TestCase):
    @patch("boomi_cicd.atomsphere_request")
    def test_query_execution_connector(self, mock_post):
        execution_record_id = "executionrecord-43ecd865-9b5e-4e15-ae1b-f8465dafc707"
        payload = {'QueryFilter': {'expression': {'operator': 'and', 'nestedExpression': [
            {'argument': [execution_record_id], 'operator': 'EQUALS',
             'property': 'executionId'}, {'argument': ['return'], 'operator': 'EQUALS', 'property': 'connectorType'}]}}}
        mock_post.return_value.text = '{"numberOfResults": 1}'

        boomi_cicd.query_execution_connector(execution_record_id)
        mock_post.assert_called_with(
            method="post", resource_path=f"/ExecutionConnector/query", payload=payload
        )

    @patch("boomi_cicd.atomsphere_request")
    @patch("time.sleep", return_value=None)
    def test_query_execution_connector_twice(self, mock_sleep, mock_post):
        execution_record_id = "executionrecord-43ecd865-9b5e-4e15-ae1b-f8465dafc707"
        payload = {'QueryFilter': {'expression': {'operator': 'and', 'nestedExpression': [
            {'argument': [execution_record_id], 'operator': 'EQUALS',
             'property': 'executionId'}, {'argument': ['return'], 'operator': 'EQUALS', 'property': 'connectorType'}]}}}

        # Define the mock response objects
        response_1 = MagicMock()
        response_1.text = '{"numberOfResults": 0}'
        response_2 = MagicMock()
        response_2.text = '{"numberOfResults": 1}'

        # Set the side_effect of the mock to return different responses
        mock_post.side_effect = [response_1, response_2]

        boomi_cicd.query_execution_connector(execution_record_id)
        mock_post.assert_called_with(
            method="post", resource_path=f"/ExecutionConnector/query", payload=payload
        )
        self.assertEqual(mock_post.call_count, 2)

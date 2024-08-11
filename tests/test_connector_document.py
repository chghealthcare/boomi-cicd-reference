import json
import unittest
from unittest.mock import patch

import pytest

import boomi_cicd


class TestConnectorDocument(unittest.TestCase):
    @patch("boomi_cicd.requests_get")
    def test_get_execution_record(self, mock_get):
        request_id = "executionrecord-43ecd865-9b5e-4e15-ae1b-f8465dafc707"
        boomi_cicd.get_execution_record(request_id)
        mock_get.assert_called_with(f"/ExecutionRecord/async/{request_id}")

    @patch("boomi_cicd.atomsphere_request")
    @patch("requests.get")
    def test_get_connector_document(self, mock_get, mock_post):
        generic_connector_record_id = "123456789"
        response_url = "https://platform.boomi.com/account/boomi_account_id/api/download/ConnectorDocument-86321d4b-2834-4f38-89e1-8b6eada2707f"
        payload = {"genericConnectorRecordId": generic_connector_record_id}
        mock_post.return_value.text = json.dumps({"url": response_url})
        mock_post.return_data.status_code = 200

        boomi_cicd.USERNAME = "username"
        boomi_cicd.PASSWORD = "password"
        mock_get.return_value.text = "connector_document_data"
        mock_get.return_data.status_code = 200

        boomi_cicd.get_connector_document(generic_connector_record_id)

        mock_post.assert_called_with(
            method="post", resource_path="/ConnectorDocument", payload=payload
        )

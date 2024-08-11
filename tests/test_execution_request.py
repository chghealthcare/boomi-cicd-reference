import json
import unittest
from unittest.mock import patch

import pytest

import boomi_cicd


class TestExecutionRequest(unittest.TestCase):
    @patch("boomi_cicd.requests_post")
    def test_create_execution_request(self, mock_post):
        mock_post.return_value.text = json.dumps(
            {
                "@type": "ExecutionRequest",
                "processId": "7b1e4d59-8d28-488b-988e-8f7826df1588",
                "atomId": "fa065728-2235-4583-87ea-a9d69762f10b",
                "requestId": "executionrecord-43ecd865-9b5e-4e15-ae1b-f8465dafc707",
            }
        )

        expected_payload = {
            "@type": "ExecutionRequest",
            "atomId": "fa065728-2235-4583-87ea-a9d69762f10b",
            "processId": "7b1e4d59-8d28-488b-988e-8f7826df1588",
        }
        result = boomi_cicd.create_execution_request(
            "fa065728-2235-4583-87ea-a9d69762f10b",
            "7b1e4d59-8d28-488b-988e-8f7826df1588",
        )
        mock_post.assert_called_with("/ExecutionRequest", expected_payload)
        assert result == "executionrecord-43ecd865-9b5e-4e15-ae1b-f8465dafc707"

    @patch("boomi_cicd.requests_post")
    def test_create_execution_request_fail(self, mock_post):
        mock_post.return_value.text = json.dumps(
            {
                "@type": "ExecutionRequest",
                "processId": "7b1e4d59-8d28-488b-988e-8f7826df1588",
                "atomId": "fa065728-2235-4583-87ea-a9d69762f10b",
            }
        )

        with pytest.raises(ValueError) as pytest_wrapper_e:
            boomi_cicd.create_execution_request(
                "fa065728-2235-4583-87ea-a9d69762f10b",
                "7b1e4d59-8d28-488b-988e-8f7826df1588",
            )
        assert pytest_wrapper_e.type == ValueError

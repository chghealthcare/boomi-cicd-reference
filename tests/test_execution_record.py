import unittest
from unittest.mock import patch

import pytest

import boomi_cicd


class TestExecutionRecord(unittest.TestCase):
    @patch("boomi_cicd.requests_get")
    def test_get_execution_record(self, mock_get):
        request_id = "executionrecord-43ecd865-9b5e-4e15-ae1b-f8465dafc707"
        boomi_cicd.get_execution_record(request_id)
        mock_get.assert_called_with(f"/ExecutionRecord/async/{request_id}")

    @patch("boomi_cicd.util.execution_record.get_execution_record")
    def test_get_execution_status(self, mock_get):
        request_id = "executionrecord-43ecd865-9b5e-4e15-ae1b-f8465dafc707"
        mock_get.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": [
                {
                    "executionId": "execution-01234567-89ab-cdef-0123-456789abcdef-2013.05.21",
                    "account": "account-123456",
                },
                {
                    "executionId": "execution-87654321-9abc-def0-1234-56789abcdef0-2013.05.21",
                    "account": "account-123456",
                },
            ],
        }

        expected_payload = {
            "account": "account-123456",
            "executionId": "execution-01234567-89ab-cdef-0123-456789abcdef-2013.05.21",
        }
        result = boomi_cicd.get_execution_status(request_id, request_internal_sec=1)
        mock_get.assert_called_with(request_id)
        assert result == expected_payload

    @patch("boomi_cicd.util.execution_record.get_execution_record")
    def test_get_execution_status_timeout(self, mock_get):
        request_id = "executionrecord-43ecd865-9b5e-4e15-ae1b-f8465dafc707"
        mock_get.status_code = 202

        with pytest.raises(TimeoutError) as pytest_wrapper_e:
            boomi_cicd.get_execution_status(request_id, request_internal_sec=1, max_wait_sec=1)
        assert pytest_wrapper_e.type == TimeoutError

    @patch("boomi_cicd.util.execution_record.get_execution_status")
    def test_get_completed_execution_status(self, mock_get):
        request_id = "executionrecord-43ecd865-9b5e-4e15-ae1b-f8465dafc707"
        mock_get.return_value = {
            "executionId": "execution-01234567-89ab-cdef-0123-456789abcdef-2013.05.21",
            "account": "account-123456",
            "status": "COMPLETE"
        }
        result = boomi_cicd.get_completed_execution_status(request_id, request_internal_sec=1)
        assert result == mock_get.return_value

    @patch("boomi_cicd.util.execution_record.get_execution_status")
    def test_get_completed_execution_status_inprocess(self, mock_get):
        request_id = "executionrecord-43ecd865-9b5e-4e15-ae1b-f8465dafc707"
        mock_get.return_value = {
            "executionId": "execution-01234567-89ab-cdef-0123-456789abcdef-2013.05.21",
            "account": "account-123456",
            "status": "INPROCESS"
        }
        with pytest.raises(TimeoutError) as pytest_wrapper_e:
            boomi_cicd.get_completed_execution_status(request_id, request_internal_sec=1, max_wait_sec=6)
        assert pytest_wrapper_e.type == TimeoutError
        assert mock_get.call_count == 6


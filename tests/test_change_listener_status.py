import unittest
from unittest.mock import patch

import boomi_cicd


class TestChangeListenerStatus(unittest.TestCase):
    @patch("boomi_cicd.requests_post")
    def test_change_listener_status(self, mock_post):
        mock_env = {
            "baseUrl": "https://api.boomi.com/api/rest/v1",
            "accountId": "boomi_account-123",
            "username": "",
            "password": "",
            "environmentName": "Test Cloud Environment",
            "atomName": "Test Atom",
            "listenerId": "1234567890",
            "atomId": "8a0a749b-4e1f-45c8-b5cc-e637f7c282e5",
            "action": "RESUME",
        }
        expected_payload = {
            "listenerId": "1234567890",
            "containerId": "8a0a749b-4e1f-45c8-b5cc-e637f7c282e5",
            "action": "RESUME",
        }
        result = boomi_cicd.change_listener_status(
            mock_env["listenerId"], mock_env["atomId"], mock_env["action"]
        )

        # Assert the function calls requests_post with the expected arguments
        mock_post.assert_called_with("/changeListenerStatus", expected_payload)
        # Assert the function returns the expected Atom ID
        assert result is True

    #  TODO: Test the other actions
    # def test_change_listener_status_503(self, mock_post):


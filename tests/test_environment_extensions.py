import boomi_cicd
import json
import unittest
from unittest.mock import patch


class TestEnvironmentExtensions(unittest.TestCase):
    @patch("boomi_cicd.requests_get")
    def test_get_environment_extensions(self, mock_get):
        mock_get.return_value.text = json.dumps(
            {
                "@type": "EnvironmentExtensions",
                "environmentId": "c5256e0d-a9fe-4f8d-afe9-66dc7f016083",
                "extensionGroupId": "",
                "id": "c5256e0d-a9fe-4f8d-afe9-66dc7f016083",
            }
        )
        mock_env = {
            "baseUrl": "https://api.boomi.com/api/rest/v1",
            "accountId": "boomi_account-123",
            "username": "",
            "password": "",
            "environmentId": "04490020-7c27-4972-b58f-917dd5e241bd",
        }

        boomi_cicd.get_environment_extensions(mock_env["environmentId"])

        mock_get.assert_called_with(
            f"/EnvironmentExtensions/{mock_env['environmentId']}"
        )

    @patch("boomi_cicd.requests_post")
    def test_update_environment_extensions(self, mock_post):
        mock_payload = {
            "@type": "EnvironmentExtensions",
            "processProperties": {
                "@type": "OverrideProcessProperties",
                "ProcessProperty": [
                    {
                        "@type": "OverrideProcessProperty",
                        "ProcessPropertyValue": [
                            {
                                "@type": "ProcessPropertyValue",
                                "label": "String",
                                "key": "new-1355426770730",
                                "encryptedValueSet": False,
                                "useDefault": False,
                                "value": "Partialupdates",
                            },
                            {
                                "@type": "ProcessPropertyValue",
                                "label": "Password",
                                "key": "new-1355426788553",
                                "value": "PasswordUpdated",
                                "encryptedValueSet": False,
                                "useDefault": False,
                            },
                        ],
                        "id": "24a56789...",
                        "name": "Boomi Test",
                    }
                ],
            },
            "environmentId": "456789ab...",
            "extensionGroupId": "",
            "id": "6f678d09...",
            "partial": True,
        }
        mock_post.return_value.text = json.dumps(
            {
                "@type": "EnvironmentExtensions",
                "processProperties": {
                    "@type": "OverrideProcessProperties",
                    "ProcessProperty": [
                        {
                            "@type": "OverrideProcessProperty",
                            "ProcessPropertyValue": [
                                {
                                    "@type": "ProcessPropertyValue",
                                    "label": "String",
                                    "key": "68dad3cb...",
                                    "value": "Partialupdates",
                                    "encryptedValueSet": False,
                                    "useDefault": False,
                                },
                                {
                                    "@type": "ProcessPropertyValue",
                                    "label": "Password",
                                    "key": "af61be8f...",
                                    "value": "PasswordUpdated",
                                    "encryptedValueSet": False,
                                    "useDefault": False,
                                },
                            ],
                            "id": "23a30680...",
                            "name": "Test Some Props Yo",
                        }
                    ],
                },
                "environmentId": "456789ab...",
                "extensionGroupId": "",
                "id": "6f678d09...",
                "partial": True,
            }
        )
        mock_env = {
            "baseUrl": "https://api.boomi.com/api/rest/v1",
            "accountId": "boomi_account-123",
            "username": "",
            "password": "",
            "environmentId": "04490020-7c27-4972-b58f-917dd5e241bd",
        }

        boomi_cicd.update_environment_extensions(
            mock_env["environmentId"], mock_payload
        )
        mock_post.assert_called_with(
            f"/EnvironmentExtensions/{mock_env['environmentId']}/update", mock_payload
        )

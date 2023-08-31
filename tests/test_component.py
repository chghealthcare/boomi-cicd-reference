import unittest
from unittest.mock import patch

import pytest
import boomi_cicd


class TestComponent(unittest.TestCase):
    @patch('boomi_cicd.requests_get_xml')
    def test_query_component(self, mock_post):
        mock_post.return_value = '''
            <?xml version="1.0" ?>
            <bns:Component xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:bns="http://api.platform.boomi.com/" folderFullPath="Boomi_AdamBedenbaugh/Examples/Circuit Breaker/Circuit Breaker with Parking Lot/01 - Target Application" componentId="4ffd1564-c1d0-4e45-bd8d-3a2e6bc44850" version="1" name="sleep" type="processproperty" createdDate="2020-09-10T18:15:40Z" createdBy="ajay.natarajan@dell.com" modifiedDate="2020-09-10T18:15:40Z" modifiedBy="ajay.natarajan@dell.com" deleted="false" currentVersion="true" folderName="01 - Target Application" folderId="RjozNTI5Mzgx" copiedFromComponentId="89918898-5105-4b69-a702-8a8b3ff16311" copiedFromComponentVersion="1">
              <bns:encryptedValues/>
              <bns:description/>
              <bns:object>
                <DefinedProcessProperties xmlns="">
                  <definedProcessProperty key="f056e8a0-cab0-4cc6-bc11-59deba9aca50">
                    <helpText/>
                    <label>Process Property #1</label>
                    <type>string</type>
                    <defaultValue>3000</defaultValue>
                    <allowedValues/>
                    <persisted>true</persisted>
                  </definedProcessProperty>
                </DefinedProcessProperties>
              </bns:object>
            </bns:Component>
            '''
        mock_component_id = "4ffd1564-c1d0-4e45-bd8d-3a2e6bc44850"

        result = boomi_cicd.query_component(mock_component_id)
        # Assert the function calls requests_post with the expected arguments
        mock_post.assert_called_with(f"/Component/{mock_component_id}")
        # Assert the function returns the expected environment ID
        assert result == mock_post.return_value



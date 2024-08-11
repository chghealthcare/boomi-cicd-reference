import pytest
import boomi_cicd


def test_convert_csv_report_to_json():
    # Test case: Valid CSV data with a title and a single data row
    csv_data = '''"Title"
"ENVIRONMENT_ID","ENVIRONMENT_NAME"
"123","Test Environment"'''

    expected_output = [
        {"ENVIRONMENT_ID": "123", "ENVIRONMENT_NAME": "Test Environment"}
    ]

    assert boomi_cicd.convert_csv_report_to_json(csv_data) == expected_output


def test_convert_csv_report_to_json_multiple_rows():
    # Test case: Valid CSV data with multiple data rows
    csv_data = '''"Title"
"ENVIRONMENT_ID","ENVIRONMENT_NAME"
"123","Test Environment"
"456","Prod Environment"'''

    expected_output = [
        {"ENVIRONMENT_ID": "123", "ENVIRONMENT_NAME": "Test Environment"},
        {"ENVIRONMENT_ID": "456", "ENVIRONMENT_NAME": "Prod Environment"},
    ]

    assert boomi_cicd.convert_csv_report_to_json(csv_data) == expected_output


def test_convert_csv_report_to_json_empty_data():
    # Test case: Empty CSV data (only the title line)
    csv_data = '''"Title"'''

    expected_output = []

    assert boomi_cicd.convert_csv_report_to_json(csv_data) == expected_output


def test_convert_csv_report_to_json_invalid_format():
    # Test case: CSV data with invalid format (no headers)
    csv_data = '''"Title"
"123","Test Environment"'''

    expected_output = []

    assert boomi_cicd.convert_csv_report_to_json(csv_data) == expected_output

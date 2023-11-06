import json
import pytest
import boomi_cicd


def test_parse_json(tmpdir):
    # Create a temporary file with some JSON data
    test_data = {'name': 'test', 'value': 42}
    test_file = tmpdir.join('test.json')
    test_file.write(json.dumps(test_data))

    # Test the function
    result = boomi_cicd.parse_json(str(test_file))
    assert result == test_data


def test_parse_json_no_file():
    # Test that the function raises a FileNotFoundError
    with pytest.raises(FileNotFoundError):
        boomi_cicd.parse_json('nonexistent/file.json')


def test_parse_json_invalid_json(tmpdir):
    # Create a temporary file with invalid JSON data
    test_file = tmpdir.join('invalid.json')
    test_file.write('not valid json')

    # Test that the function raises a JSONDecodeError
    with pytest.raises(json.JSONDecodeError):
        boomi_cicd.parse_json(str(test_file))




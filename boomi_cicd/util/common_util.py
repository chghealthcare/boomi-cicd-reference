import argparse
import json
import os
import urllib3
from ratelimit import limits, sleep_and_retry
from retrying import retry

import base64

import boomi_cicd
from boomi_cicd import logger


def parse_json(file_path):
    """
    Parse a JSON file and return the parsed data.

    :param file_path: The path to the JSON file.
    :type file_path: str
    :return: The parsed data from the JSON file.
    :rtype: dict or list
    """
    f = open(os.path.join(boomi_cicd.CLI_BASE_DIR, file_path))
    data = json.load(f)
    f.close()
    return data


def parse_release(file_path):
    """
    Parse a release file and return the parsed data.

    :param file_path: The path to the release file.
    :type file_path: str
    :return: The parsed data from the release file.
    :rtype: dict
    """
    f = open(os.path.join(boomi_cicd.RELEASE_BASE_DIR, file_path))
    data = json.load(f)
    f.close()
    return data


def parse_args():
    """Will parse arguments from the command line. Looks for a release file with a -r or --release argument."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--release")
    args = parser.parse_args()
    return args


def set_release():
    """
    Set the release data based on command-line arguments or environment variable.

    This function retrieves the release data from either the command-line argument or the default configuration.
    If the `--release` argument is provided, it reads the JSON data from the specified file path.
    Otherwise, it reads the JSON data from the default release file path.

    :return: The release data as a dictionary.
    """
    args = parse_args()
    if args.release:
        return parse_json(args.release)
    else:
        if boomi_cicd.RELEASE_FILE is not None:
            release_file = boomi_cicd.RELEASE_FILE
        else:
            raise ValueError("No release file specified.")
        return parse_release(release_file)


def set_env_release():
    """
    Set the environment extensions release data based on the BOOMI_ENV_RELEASE_FILE environment variable.

    This function retrieves the environment extensions release file.

    :return: The environment extensions release data as a dictionary.
    """
    if boomi_cicd.ENV_RELEASE_FILE is not None:
        release_file = boomi_cicd.ENV_RELEASE_FILE
    else:
        raise ValueError("No environment extensions release file specified.")
    return parse_release(release_file)


@sleep_and_retry
@limits(calls=boomi_cicd.CALLS_PER_SECOND, period=boomi_cicd.RATE_LIMIT_SECONDS)
def check_limit():
    """
    Empty function to limit the number of calls to the Atomsphere API.

    This function is used as a decorator to enforce a rate limit on API calls. It ensures that the decorated function
    is called within the specified rate limit.

    :return: None
    """
    return


@retry(
    stop_max_attempt_number=3,
    wait_fixed=boomi_cicd.RATE_LIMIT_MILLISECONDS,
    retry_on_result=lambda x: x == 503,
)
def requests_get_xml(resource_path):
    """
    Perform a GET request to the Atomsphere API and retrieve XML data.

    :param resource_path: The resource path for the API endpoint.
    :type resource_path: str
    :return: The response object containing the XML data.
    :rtype: str
    :raises requests.HTTPError: If the GET request fails (non-2xx response). A 503 response will be retried up to 3 times.
    """
    check_limit()
    headers = urllib3.HTTPHeaderDict()
    headers.add("Accept", "application/xml")
    headers.add("Authorization", get_authorization_token())
    url = boomi_cicd.BASE_URL + "/" + boomi_cicd.ACCOUNT_ID + resource_path

    response = urllib3.request("GET", url, headers=headers)

    logger.info(
        "Response: {}".format(
            response.data.decode().replace("\r", "").replace("\n", "")
        )
    )

    raise_for_status(response.status)
    return response.data.decode()


@retry(
    stop_max_attempt_number=3,
    wait_fixed=boomi_cicd.RATE_LIMIT_MILLISECONDS,
    retry_on_result=lambda x: x == 503,
)
def requests_get(resource_path):
    """
    Perform a GET request to the Atomsphere API and retrieve JSON data.

    :param resource_path: The resource path for the API endpoint.
    :type resource_path: str
    :return: The response object containing the JSON data.
    :rtype: dict
    :raises requests.HTTPError: If the GET request fails (non-2xx response).  A 503 response will be retried up to 3 times.
    """
    check_limit()
    headers = urllib3.HTTPHeaderDict()
    headers.add("Accept", "application/json")
    headers.add("Authorization", get_authorization_token())
    url = f"{boomi_cicd.BASE_URL}/{boomi_cicd.ACCOUNT_ID}{resource_path}"

    response = urllib3.request("GET", url, headers=headers)

    logger.info(f"Status: {response.status}. Response: {response.json()}")
    raise_for_status(response.status)
    return response.json()


@retry(
    stop_max_attempt_number=3,
    wait_fixed=boomi_cicd.RATE_LIMIT_MILLISECONDS,
    retry_on_result=lambda x: x == 503,
)
def requests_post(resource_path, payload):
    """
    Perform a POST request to the Atomsphere API with the specified payload.

    :param resource_path: The resource path for the API endpoint.
    :type resource_path: str
    :param payload: The payload to be sent in the request body (as JSON).
    :type payload: dict
    :return: The response object containing the JSON response data.
    :rtype: dict
    :raises requests.HTTPError: If the POST request fails (non-2xx response). A 503 response will be retried up to 3 times.
    """
    check_limit()
    logger.info("Request: {}".format(json.dumps(payload)))
    headers = urllib3.HTTPHeaderDict()
    headers.add("Accept", "application/json")
    headers.add("Content-Type", "application/json")
    headers.add("Authorization", get_authorization_token())
    url = boomi_cicd.BASE_URL + "/" + boomi_cicd.ACCOUNT_ID + resource_path

    response = urllib3.request("POST", url, body=json.dumps(payload), headers=headers)

    logger.info(f"Status: {response.status}. Response: {response.json()}")
    raise_for_status(response.status)
    return response.json()


@retry(
    stop_max_attempt_number=3,
    wait_fixed=boomi_cicd.RATE_LIMIT_MILLISECONDS,
    retry_on_result=lambda x: x == 503,
)
def requests_delete(resource_path):
    """
    Perform a DELETE request to the Atomsphere API.

    :param resource_path: The resource path for the API endpoint.
    :type resource_path: str
    :return: The response object containing the JSON response data.
    :rtype: dict
    :raises requests.HTTPError: If the DELETE request fails (non-2xx response). A 503 response will be retried up to 3 times.
    """
    check_limit()
    headers = urllib3.HTTPHeaderDict()
    headers.add("Accept", "application/json")
    url = boomi_cicd.BASE_URL + "/" + boomi_cicd.ACCOUNT_ID + resource_path

    response = urllib3.request("DELETE", url, headers=headers)

    logger.info("Response: {}".format(response.data))
    raise_for_status(response.status)
    return response.json()


def get_authorization_token():
    token_bytes = (boomi_cicd.USERNAME + ":" + boomi_cicd.PASSWORD).encode("ascii")
    token_bytes_base64 = base64.b64encode(token_bytes)
    auth_token = token_bytes_base64.decode("ascii")
    return "Basic " + auth_token


def raise_for_status(status_code):
    # Raise an exception if the response status is not 2xx
    if status_code < 200 or status_code >= 300:
        raise Exception("HTTPError: {}".format(status_code))

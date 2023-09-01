import boomi_cicd
import sys

from boomi_cicd import logger


# https://help.boomi.com/bundle/developer_apis/page/r-atm-Environment_object.html


def query_environment(environment_name):
    """
    Query the Boomi environment by name to retrieve the environment ID.

    :param environment_name: The name of the Boomi environment.
    :type environment_name: str
    :return: The environment ID.
    :rtype: str
    :raises SystemExit: If the environment is not found.
    """
    resource_path = "/Environment/query"
    logger.info(resource_path)
    environment_query = "boomi_cicd/util/json/environmentQuery.json"
    payload = boomi_cicd.parse_json(environment_query)
    payload["QueryFilter"]["expression"]["argument"][0] = environment_name

    response = boomi_cicd.requests_post(resource_path, payload)

    if response["numberOfResults"] == 0:
        logger.error(
            f"Environment not found. EnvironmentName: {boomi_cicd.ENVIRONMENT_NAME}"
        )
        sys.exit(1)
    environment_id = response["result"][0]["id"]
    return environment_id

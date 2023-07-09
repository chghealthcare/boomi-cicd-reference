import boomi_cicd
from boomi_cicd.util.common_util import set_release
from boomi_cicd.util.deployed_package import query_deployed_package, create_deployed_package
from boomi_cicd.util.environment import query_environment
from boomi_cicd.util.packaged_component import (
    query_packaged_component,
    create_packaged_component,
)

# Open release json
releases = set_release()

environment_id = query_environment(boomi_cicd.ENVIRONMENT_NAME)

for release in releases["pipelines"]:
    component_id = release["componentId"]
    package_version = release["packageVersion"]
    notes = release.get("notes")

    package_id = query_packaged_component(component_id, package_version)

    if not package_id:
        package_id = create_packaged_component(component_id, package_version, notes)

    # The third parameter determines if the package is currently deployed (True) or has every been deployed (False)
    package_deployed = query_deployed_package(package_id, environment_id, False)
    if not package_deployed:
        deployment_id = create_deployed_package(release, package_id, environment_id)
        # delete_deployed_package(deployment_id) # Delete deployment is useful for testing

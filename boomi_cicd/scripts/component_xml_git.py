import boomi_cicd
import datetime
import xml.etree.ElementTree as ET
import os

from xml.dom import minidom
from git import Repo
from boomi_cicd import logger


# TODO: Refactor code into smaller functions.

# Open release json
releases = boomi_cicd.set_release()

# Clone repo
repo = Repo.clone_from(boomi_cicd.COMPONENT_GIT_URL, boomi_cicd.COMPONENT_REPO_NAME)
logger.info(f"Git Repo Status: {repo.git.status()}".replace("\n", " "))

file_components = boomi_cicd.get_component_xml_file_refs(boomi_cicd.COMPONENT_REPO_NAME)

for release in releases["pipelines"]:
    component_id = release["componentId"]
    process_name = release["processName"]
    package_version = release["packageVersion"]
    process_base_dir = f"{boomi_cicd.COMPONENT_REPO_NAME}/{process_name}"

    # Check if the packaged component's name has changed. If so, rename the folder
    # The directory name comes from the process name in the release json
    if (
        component_id in file_components
        and process_name != file_components[component_id]
    ):
        logger.info(
            f"Process name changed. Original: {file_components[component_id]}. New: {process_name}"
        )
        repo.git.mv(f"{file_components[component_id]}", f"{process_name}")
        file_components[component_id] = process_name

    component_refs = {}
    # Check if component id exists in packaged component's .componentRef
    if os.path.exists(process_base_dir):
        component_refs = boomi_cicd.get_component_xml_file_refs(process_base_dir)
        logger.info(f"Created component_refs: {component_refs}")

    # Parse xml for component id
    packaged_component_id = boomi_cicd.query_packaged_component(
        component_id, package_version
    )
    packaged_manifest = boomi_cicd.get_package_component_manifest(packaged_component_id)
    root = ET.fromstring(packaged_manifest)
    component_info_names = set()
    for component_info in root.findall(".//bns:componentInfo", boomi_cicd.NAMESPACES):
        component_info_id = component_info.attrib["id"]

        # Query components
        # TODO: Update query_component to accept version.
        component_xml = boomi_cicd.query_component(component_info_id)

        # Use the dict to know if a file should be updated or created.
        # Get the component name for the filename
        component_name = ET.fromstring(component_xml).attrib["name"]
        component_file_name = f"{component_name}.xml"
        component_info_names.add(component_file_name)

        if (
            component_info_id in component_refs
            and component_file_name != component_refs[component_info_id]
        ):
            # Check if file needs to be renamed
            logger.info(
                f"Component name changed. Original: {component_refs[component_info_id]}. New: {component_name}"
            )
            repo.git.mv(
                f"{process_name}/{component_refs[component_info_id]}",
                f"{process_name}/{component_file_name}",
            )

        # Write component xml to file
        with open(f"{process_base_dir}/{component_file_name}", "w") as f:
            f.write(minidom.parseString(component_xml).toprettyxml(indent="  "))

        component_refs[component_info_id] = component_file_name

    # Delete files that are not in the component manifest and romove from component_refs of the packaged component
    for dirpath, dirnames, filenames in os.walk(process_base_dir):
        for filename in filenames:
            if filename not in component_info_names and filename != ".componentRef":
                repo.git.rm(f"{process_name}/{filename}")
                logger.info(f"Deleted {filename} from {process_name}")

    boomi_cicd.set_component_xml_file_refs(process_base_dir, component_refs)

# Commit all changes
repo.index.add("*")
commit_message = "Commit from Boomi CICD on {}".format(
    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
)
logger.info(f"Commiting changes: {commit_message}")
repo.index.commit(commit_message)
repo.remote("origin").push("main")

boomi_cicd.set_component_xml_file_refs(boomi_cicd.COMPONENT_REPO_NAME, file_components)

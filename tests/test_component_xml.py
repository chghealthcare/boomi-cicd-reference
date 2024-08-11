import os
import shutil
from unittest.mock import patch

import boomi_cicd


# TODO: Mock clone_repository()


@patch(
    "boomi_cicd.platform.system", return_value="Linux"
)  # Mock the 'platform' function for Windows
def test_install_sonarqube_linux(mock_platform):
    sonarqube_zip_file = "sonar-scanner-cli-4.8.0.2856-linux.zip"
    sonarqube_dir = boomi_cicd.install_sonarqube()

    assert sonarqube_dir == "sonar-scanner-4.8.0.2856-linux"
    assert os.path.exists(sonarqube_dir)
    assert os.path.exists(sonarqube_zip_file)

    remove_directory(sonarqube_dir)
    os.remove(sonarqube_zip_file)


@patch(
    "boomi_cicd.platform.system", return_value="Windows"
)  # Mock the 'platform' function for Windows
def test_install_sonarqube_windows(mock_platform):
    sonarqube_zip_file = "sonar-scanner-cli-4.8.0.2856-windows.zip"
    sonarqube_dir = boomi_cicd.install_sonarqube()

    assert sonarqube_dir == "sonar-scanner-4.8.0.2856-windows"
    assert os.path.exists(sonarqube_dir)
    assert os.path.exists(sonarqube_zip_file)

    remove_directory(sonarqube_dir)
    os.remove(sonarqube_zip_file)


def remove_directory(path):
    try:
        shutil.rmtree(path, ignore_errors=False)
    except Exception as e:
        print(f"Error: {e}")

import os
from zipfile import ZipFile
from sys import platform
import requests

import boomi_cicd
from boomi_cicd import logger


# Detect OS
if platform == "linux" or platform == "linux2":
    # Download linux zip
    # https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.8.0.2856-linux.zip
    sonarqube_version = "sonar-scanner-cli-5.0.1.3006-linux"
    sonarqube_version_unzip = "sonar-scanner-5.0.1.3006-linux"
elif platform == "win32":
    # Download windows zip
    # https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.8.0.2856-windows.zip
    sonarqube_version = "sonar-scanner-cli-4.8.0.2856-windows"
    sonarqube_version_unzip = "sonar-scanner-4.8.0.2856-windows"
else:
    raise OSError("Unsupported OS")

# Download SonarQube
url = "https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/"
sonarqube_version_zip = f"{sonarqube_version}.zip"

r = requests.get(url + sonarqube_version_zip, allow_redirects=True)
with open(sonarqube_version_zip, "wb") as f:
    f.write(r.content)

# Extract SonarQube
with ZipFile(sonarqube_version_zip, "r") as zipObj:
    zipObj.extractall()


base_folder = "\"" + os.path.join(os.getcwd(), boomi_cicd.COMPONENT_REPO_NAME) + "\""
logger.info(f"Boomi Component Repo Directory: {base_folder}")
logger.info(f"Sonar Host URL: {boomi_cicd.SONARQUBE_HOST_URL}")
logger.info(f"Sonar Project Key: {boomi_cicd.SONARQUBE_PROJECT_KEY}")

os.system(
    fr"{sonarqube_version_unzip}\bin\sonar-scanner.bat"
    fr" -Dsonar.projectKey={boomi_cicd.SONARQUBE_PROJECT_KEY}"
    fr" -Dsonar.projectBaseDir={base_folder}"
    fr" -Dsonar.sources={base_folder}"
    fr" -Dsonar.host.url={boomi_cicd.SONARQUBE_HOST_URL}"
    fr" -Dsonar.login={boomi_cicd.SONARQUBE_TOKEN}"
)


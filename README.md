# Boomi CI/CD Reference Implementation

The boomi-cicd-cli-py library is used to automate Boomi deployments through the CICD Pipelines that your are already using. It performs orchestration for deploying and managing Boomi runtimes, components, and metadata required for CI/CD. 


## Overview

To get started, there are two main elements you will need to complete: import this repo and create a release file. This repo contains a sample release pipeline script that will read through your release file. It will create packaged components and will deploy the packaged components to an environment. Those parts involved with setting up  the release pipeline are described below and also described in greater detail in the documentation.


## Pre-requistes

* Python 3
* Additional libraries, which can be installed with `pip install -r requirements.txt`


## Project Structure

The project is broken into three sections.

1. [scripts](boomi_cicd/scripts) - This directory contains the scripts that will be executed within a CI/CD pipeline.
   The release_pipeline.py is the main script. There are additional example scripts that can be used as a starting point
   for your own pipelines.
2. [util](boomi_cicd/util) - This directory contains the utility scripts that are used by the scripts in the scripts
   directory.
3. [templates](boomi_cicd/templates) - This directory contains the release pipeline templates. These templates can be
   used as-is or as a starting point for your own release pipeline.

## Example Scripts

| Name                             | Description                                                                        |
|----------------------------------|------------------------------------------------------------------------------------|
| release_pipeline                 | Create packaged components and deploy to an environment                            |
| release_pipeline_dr              | Turn off schedules and listeners on primary site, and on in disaster recovery site |
| release_pipeline_schedules       | Update schedules on an atom                                                        |
| environment_extensions_update    | Update environment extensions                                                      |
| environment_extensions_templates | Create environment extensions from templates                                       |
| component_xml_git                | Copy component XML files into a git repository                                     |

## Release JSON File

The scripts mentioned above are based on the release.json file. The file includes all components that need to be
deployed and any schedules or listener status that needs to be configured.

| Release JSON Element | Description                                                                                                                                                             | Required |
|----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| processName          | Name of the process. Mainly used for human readability.                                                                                                                 | Yes      |
| packageVersion       | Define the package version. If one isn't specified, the latest version will be used.                                                                                    | Yes      | 
| componentId          | The component ID of the process to deploy.                                                                                                                              | Yes      |
| notes                | The notes that will be added to the packaged components and deployments.                                                                                                | No       |
| schedule             | The schedule that will be used to deploy the process. Each individual schedule is space delimited. Multiple schedules are semi-colon delimited. Additional notes below. | No       |
| listenerStatus       | The status of the listener when deployed. Values: RUNNING or PAUSED. RUNNING is default.                                                                                | No       |

Example Release JSON with a batch process, a listener process, and a custom library.

```json
{
  "pipelines": [
    {
      "processName": "An Example Batch Process",
      "packageVersion": "2.0",
      "componentId": "83d6013f-96f5-4a75-a97b-f4934b0ec2e8",
      "notes": "This is an example set of notes",
      "schedule": "0 0 1 * * * ; 30 0 2-7 * * *"
    },
    {
      "processName": "An Example Listener Process",
      "packageVersion": "1.0",
      "componentId": "b24f310b-6a66-4e0d-97a3-26f1e812b79a",
      "notes": "This is an example set of notes",
      "listenerStatus": "RUNNING"
    },
    {
      "processName": "An Example Custom Library",
      "componentId": "7bd40730-6df3-4ba9-b4b2-ed9153dbca6d",
      "packageVersion": "1.0",
      "notes": "Initial deployment"
    }
  ]
}
```

### Schedule Configuration

The schedule element requires 6 space-delimited values in this order: minutes, hours, days of the week, days of the
month,
month, and year. The example `0 0 1 * * *` would execute the process on every Sunday at midnight.

| Field       | Description                                                                                                           |
|-------------|-----------------------------------------------------------------------------------------------------------------------|
| minutes     | 0 is the first minute of the hour — for example, 1:00 A.M. 59 is the last minute of the hour — for example, 1:59 A.M. |
| hours       | Uses a 24-hour clock. 0 is midnight and 12 is noon.                                                                   |
| daysOfWeek  | 1 is Sunday and 7 is Saturday.                                                                                        |
| daysOfMonth | 1 is the first day of the month and 31 is the last day of the month.                                                  |
| month       | 1 is January and 12 is December. In most cases this is set to an asterisk [*].                                        |
| year        | 4 digit year - for example, 2023.                                                                                     |

## Environment Variables

The following environment variables are required to run the releasePipeline.py script. They can be set by environment
variables or by using a .env file. Not variables are 

| Environment Variable    | boomi_cicd Constant Name | Description                                       | Required                                                                       |  
|-------------------------|--------------------------|---------------------------------------------------|--------------------------------------------------------------------------------|
| BOOMI_BASE_URL          | BASE_URL                 | The base URL of the Boomi account                 | Yes                                                                            |
| BOOMI_ACCOUNT_ID        | ACCOUNT_ID               | The account ID of the Boomi account               | Yes                                                                            |
| BOOMI_USERNAME          | USERNAME                 | The username of the Boomi account                 | Yes                                                                            |
| BOOMI_PASSWORD          | PASSWORD                 | The password of the Boomi account                 | Yes                                                                            |
| BOOMI_ENVIRONMENT_NAME  | ENVIRONMENT_NAME         | The environment name used to deploy to components | Yes                                                                            |
| BOOMI_ATOM_NAME         | ATOM_NAME                | The atom name used to set set schedules           | Yes                                                                            |
| BOOMI_ATOM_NAME_DR      | ATOM_NAME_DR             | The atom name of the disaster recovery atom       | Optional ([release_pipeline_dr.py](boomi_cicd/scripts/release_pipeline_dr.py)) |
| BOOMI_COMPONENT_GIT_URL | COMPONENT_GIT_URL        | git URL of the component repository               | Optional ([component_xml_git.py](boomi_cicd/scripts/component_xml_git.py))     |
| BOOMI_CLI_BASE_DIR      | CLI_BASE_DIR             | Base directory of the boomi_cicd scripts          | Yes                                                                            |
| BOOMI_CLI_RELEASE_DIR   | CLI_RELEASE_DIR          | Base directory of the release.json file           | Yes                                                                            |
| BOOMI_CLI_RELEASE_FILE  | CLI_RELEASE_FILE         | Name of the release.json file                     | Yes                                                                            |

The environment variables can be accessed within the scripts by importing boomi_cicd and use the variable name. The
constant names are the same as above but with 'BOOMI_' removed.

```python
import boomi_cicd

# Read the base URL
print(boomi_cicd.BASE_URL)
```

## Running the Release Pipeline

The release pipeline script is ready to be executed once the release json has been created and the environment variables set.

A release file can be defined by either adding a command line
arguments (-r) or by defining the file with an environment varialble (BOOMI_CLI_RELEASE_FILE).

```bash
# Example of setting a release file with a command line argument
python boomi_cicd/scripts/releasePipeline.py -r <release-file-location>
# or define the release file with an environment variable and do not pass any arguments
python boomi_cicd/scripts/releasePipeline.py
```


## Release Templates

The following release templates are available. Each template has its own README with instructions on how to use it. They
demonstrate how to use a basic release pipeline to deploy processes to a Boomi environment. The release pipelines can be
used as-is or as a starting point for your own release pipeline. Each release pipeline will parse a release.json file,
check if a package has been created, if not create one, and check if the package has been deployed, if not deploy it.

* [Azure DevOps](boomi_cicd/templates/azure_devops/README_azure_devops.md)
* [GitHub Actions](boomi_cicd/templates/github_actions/README_github_actions.md): TODO
* [Jenkins](boomi_cicd/templates/jenkins/README_jenkins.md): TODO

## TODOs

* Script for SonarQube integration.


## Documentation Build

The documentation can be built locally by running the following command from the docs directory. Once build, go to docs/_build/index.html to view the documentation.

```bash
cd docs
sphinx-build -b html . _build 
```


## Ways to Contribute

1. Create PR to submit changes.
2. Update the documenation. The documentation is built using Sphinx. The source files are written in reStructured Text (.rst) and located in the docs/source
   directory. 

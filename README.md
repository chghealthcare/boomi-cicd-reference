# Boomi CI/CD Reference Implementation

The boomi-cicd-cli-py library enables automated Boomi deployments through seamless integration with your existing CI/CD pipelines. It facilitates the orchestration of Boomi runtimes, components, and essential metadata for efficient CI/CD workflows.


## Overview

To get started, there are two main elements you need to complete: importing this repository and creating a release file. This repository includes a sample release pipeline script that reads through your release file, creates packaged components, and deploys them to an environment. The steps involved in setting up the release pipeline are described below and detailed in the documentation.


## Documentation

The documentation for this project is hosted on [boomi-cicd-cli-py Documentation](https://boomi-cicd-cli-py.s3.amazonaws.com/index.html). 


## Pre-requistes

* Python 3
* Additional libraries, which can be installed with `pip install -r requirements.txt`


## Project Structure

The project is broken into three sections.

1. [scripts](boomi_cicd/scripts) - Contains the scripts to be executed within a CI/CD pipeline. The main script is `release_pipeline.py`, and there are additional example scripts that can serve as starting points for your own pipelines.
2. [util](boomi_cicd/util) - Contains utility scripts used by the scripts in the `scripts` directory.
3. [templates](boomi_cicd/templates) - Contains release pipeline templates that can be used as-is or customized for your specific requirements.


## Example Scripts

| Name                             | Description                                                     |
|----------------------------------|-----------------------------------------------------------------|
| release_pipeline                 | Create packaged components and deploy to an environment         |
| release_pipeline_dr              | 	Configures schedules and listeners for disaster recovery site  |
| release_pipeline_schedules       | Update schedules on an atom                                     |
| environment_extensions_update    | Update environment extensions                                   |
| environment_extensions_templates | Create environment extensions from templates                    |
| component_xml_git                | Copy component XML files into a git repository                  |


## Release JSON File

The mentioned scripts rely on the `release.json` file, which includes the components to be deployed and their configuration.

| Release JSON Element | Description                                                                                                                                                             | Required |
|----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| processName          | Name of the process. Mainly used for human readability.                                                                                                                 | Yes      |
| packageVersion       | Define the package version. If one isn't specified, the latest version will be used.                                                                                    | Yes      | 
| componentId          | The component ID of the process to deploy.                                                                                                                              | Yes      |
| notes                | The notes that will be added to the packaged components and deployments.                                                                                                | No       |
| schedule             | The schedule that will be used to deploy the process. Each individual schedule is space delimited. Multiple schedules are semi-colon delimited. Additional notes below. | No       |
| listenerStatus       | The status of the listener when deployed. Values: RUNNING or PAUSED. RUNNING is default.                                                                                | No       |

An example release JSON file with a batch process, a listener process, and a custom library:

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

The environment variables can be accessed within the scripts by importing boomi_cicd and using the variable name. The
constant names are the same as above but with 'BOOMI_' removed.

```python
import boomi_cicd

# Read the base URL
print(boomi_cicd.BASE_URL)
```

## Running the Release Pipeline

Once you have created the release JSON file and set the environment variables, you can execute the release pipeline script.

To define a release file, you can either use a command-line argument (-r) or set the file using an environment variable (BOOMI_CLI_RELEASE_FILE).

Example of setting a release file using an environment variable:

```bash
python boomi_cicd/scripts/releasePipeline.py
```

Alternatively, you can set the release file with a command-line argument:

```bash
python boomi_cicd/scripts/releasePipeline.py -r <release-file-location>
```


## Release Templates

A variety of release templates are at your disposal, each accompanied by comprehensive documentation detailing their usage instructions. These templates serve as practical demonstrations, showcasing the implementation of a fundamental release pipeline for deploying processes to a Boomi environment. You can use the release pipelines as-is or as a starting point for your own release pipeline. Each release pipeline parses a release JSON file, checks if a package has been created, creates one if not, and checks if the package has been deployed, deploys it if not.

* [Azure DevOps](https://boomi-cicd-cli-py.s3.amazonaws.com/pipelines/azure-devops.html)
* [GitHub Actions](https://boomi-cicd-cli-py.s3.amazonaws.com/pipelines/github-actions.html): TODO
* [Jenkins](https://boomi-cicd-cli-py.s3.amazonaws.com/pipelines/jenkins.html): TODO


## TODOs

* Script for SonarQube integration.
* Script for GitHub Actions integration.
* Script for Jenkins integration.


## Documentation Build

You can build the documentation locally by running the following command from the `docs` directory. Once built, navigate to docs/_build/index.html to view the documentation.

```bash
cd docs
sphinx-build -b html . _build 
```


## Ways to Contribute

1. Create a pull request to submit changes.
2. Update the documentation. The documentation is built using Sphinx. The source files are written in reStructuredText (.rst) and located in the docs/source directory.

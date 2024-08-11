# Introduction to boomi-cicd-cli-py

The boomi-cicd-cli-py library enables automated Boomi deployments through seamless integration with your existing CI/CD pipelines. It facilitates the orchestration of Boomi runtimes, components, and essential metadata for efficient CI/CD workflows.


## Overview

To get started, there are two main elements you need to complete: importing this repository and creating a release file. This repository includes a sample release pipeline script that reads through your release file, creates packaged components, and deploys them to an environment. The steps involved in setting up the release pipeline are described below and detailed in the documentation.


## Documentation

The documentation for this project is found at [boomi-cicd-cli-py Documentation](https://boomi-cicd-cli-py.s3.amazonaws.com/index.html).
It includes all the information you need to get started with the library, including installation instructions, usage examples, and release pipeline templates.


## Pre-requistes

* Python 3.6 or higher
* Additional libraries, which can be installed with `pip install -r requirements.txt`
* git v1.7.0 or higher: Optional. Only required when executing the `component_xml_git.py` script.

## Project Structure

The project is organized into three sections:

1. [scripts](boomi_cicd/scripts) - Contains the scripts to be executed within a CI/CD pipeline. The main script is `release_pipeline.py`, and there are additional example scripts that can serve as starting points for your own pipelines.
2. [util](boomi_cicd/util) - Contains the core functionality of the library.
3. [templates](boomi_cicd/templates) - Contains release pipeline templates that can be used as-is or customized for your specific requirements.


## Running Your First Pipeline

We will start with running `release_pipeline.py`.
The pipeline is designed
to check if a package component should be created, and if a process needs to be deployed to a specific environment. 

1. Create a Release JSON
2. Set Environment Variables
3. Run the Release Pipeline script


### Release JSON File

The Release Pipeline script rely on the `release.json` file, which includes the components to be deployed and their configuration.

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


### Environment Variables

The following environment variables are required to run the releasePipeline.py script. They can be set by environment
variables or by using a .env file. 

| Environment Variable   | boomi_cicd Constant Name | Description                                       | Required   |  
|------------------------|----------------------|---------------------------------------------------|------------|
| BOOMI_BASE_URL         | BASE_URL             | The base URL of the Boomi account                 | Yes        |
| BOOMI_ACCOUNT_ID       | ACCOUNT_ID           | The account ID of the Boomi account               | Yes        |
| BOOMI_USERNAME         | USERNAME             | The username of the Boomi account                 | Yes        |
| BOOMI_PASSWORD         | PASSWORD             | The password of the Boomi account                 | Yes        |
| BOOMI_ENVIRONMENT_NAME | ENVIRONMENT_NAME     | The environment name used to deploy to components | Yes        |
| BOOMI_RELEASE_FILE     | RELEASE_FILE         | Full path of the release.json file                | Yes        |


### Running the Release Pipeline

Once you have created the release JSON file and set the environment variables,
you can execute the release pipeline script. To define a release file, you can either use a command-line argument (-r) or set the file using an environment variable
(BOOMI_RELEASE_FILE).

Example of running the release pipeline script:
```bash
python boomi_cicd/scripts/releasePipeline.py
```


## Release Templates

A variety of release templates are at your disposal, each accompanied by comprehensive documentation detailing their usage instructions. These templates serve as practical demonstrations, showcasing the implementation of a fundamental release pipeline for deploying processes to a Boomi environment. You can use the release pipelines as-is or as a starting point for your own release pipeline. Each release pipeline parses a release JSON file, checks if a package has been created, creates one if not, and checks if the package has been deployed, deploys it if not.

* [Azure DevOps](https://boomi-cicd-cli-py.s3.amazonaws.com/pipelines/azure-devops.html)
* [GitHub Actions](https://boomi-cicd-cli-py.s3.amazonaws.com/pipelines/github-actions.html): 
* [Jenkins](https://boomi-cicd-cli-py.s3.amazonaws.com/pipelines/jenkins.html)


## Documentation Build

You can build the documentation locally by running the following command from the `docs` directory. Once built, navigate to docs/_build/index.html to view the documentation.

```bash
cd docs
sphinx-build -b html . _build 
```

[Black](https://black.readthedocs.io/en/stable/index.html) is used for code formatting. To format the code, run the following command:

```bash
pip install black
black .
```



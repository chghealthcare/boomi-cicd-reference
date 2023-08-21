.. _release:

Getting Started
###############

The Boomi CICD python library is used to assist with automated deployments of Boomi components.



Scripts Combinations
----------------------------

The scripts all build upon a `common release file <release.html>`_. Therefore, the example scripts can be used as LEGO blocks and combined in a way that is useful for deployments within your oganization. Below are a few common examples of how the scripts can be used together.

Release Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``release_pipeline.py`` is the main script and will likely be used within all pipelines. The other scripts are examples of what additional functionality can be achived. The `release pipeline section <../pipelines/release-pipeline-configuration.html>`_ reviews how to implement this script within your pipeline.

If you do decide to use the additional functionality, then you can chain the scripts together in this way:

1. ``component_xml_git.py``: Copy the a git repositoy locally and add the component xml files from the release file. Then, commit and push the change.
2. ``component_xml_code_quality.py``: The component xml files will be validated against the /boomi_cicd/util/sonarqube/BoomiSonarRules.xml or a custom rules file. The validate will create a report within the components repository.
3. ``component_xml_sonarqube.py``: Similar to the component_xml_code_quality.py script, but this script will push the results to a SonarQube server.
4. ``release_pipeline.py``: This script will deploy the package components to a specific Boomi environment.
5. ``environment_extensions_update.py``: Update the environment extensions before the process schedules are set.
6. ``release_pipeline_scedules.py``: Set the process schedules for the deployed components.
7. ``release_pipeline_dr.py``: If using an active-active architecture, then this script will enable the packaged components on the disaster recovery runtime.


Release JSON File
----------------------------

The scripts mentioned above are based on the release.json file. The file includes all components that need to be
deployed and any schedules or listener status that needs to be configured. The file is loosely based on Jenkin's pipeline data structure.

.. include:: release.rst


Environment Variables
----------------------------

Environment variables are used the set the variables for the library. Below are a list of the environment variables that ared used within the library and found within the ``boomi_cicd.util.contants.py`` module. Not all are required for all scripts. More details on which script requires which enviornment can be found within the `example script documentation <../example-scripts/example-cicd-scripts.html>`_.

.. table:: Environment Variables
   :align: center
   :width: 100%

   +-----------------------------+--------------------------+---------------------------------------------------------+--------------+
   | Environment Variable        | boomi_cicd Constant Name | Description                                             | Required     |
   +=============================+==========================+=========================================================+==============+
   | BOOMI_BASE_URL              | BASE_URL                 | The base URL of the Boomi account                       | Yes          |
   +-----------------------------+--------------------------+---------------------------------------------------------+--------------+
   | BOOMI_ACCOUNT_ID            | ACCOUNT_ID               | The account ID of the Boomi account                     | Yes          |
   +-----------------------------+--------------------------+---------------------------------------------------------+--------------+
   | BOOMI_USERNAME              | USERNAME                 | The username of the Boomi account                       | Yes          |
   +-----------------------------+--------------------------+---------------------------------------------------------+--------------+
   | BOOMI_PASSWORD              | PASSWORD                 | The password of the Boomi account                       | Yes          |
   +-----------------------------+--------------------------+---------------------------------------------------------+--------------+
   | BOOMI_ENVIRONMENT_NAME      | ENVIRONMENT_NAME         | The environment name used to deploy to components       | Yes          |
   +-----------------------------+--------------------------+---------------------------------------------------------+--------------+
   | BOOMI_ATOM_NAME             | ATOM_NAME                | The atom name used to set set schedules                 | Yes          |
   +-----------------------------+--------------------------+---------------------------------------------------------+--------------+
   | BOOMI_ATOM_NAME_DR          | ATOM_NAME_DR             | The atom name of the disaster recovery atom             | Optional     |
   +-----------------------------+--------------------------+---------------------------------------------------------+--------------+
   | BOOMI_COMPONENT_GIT_URL     | COMPONENT_GIT_URL        | git URL of the component repository                     | Optional     |
   +-----------------------------+--------------------------+---------------------------------------------------------+--------------+
   | BOOMI_CLI_RELEASE_FILE      | CLI_RELEASE_FILE         | Name of the release.json file                           | Yes          |
   +-----------------------------+--------------------------+---------------------------------------------------------+--------------+
   | BOOMI_ENV_RELEASE_FILE      | ENV_RELEASE_FILE         | Name of the release.json file                           | Yes          |
   +-----------------------------+--------------------------+---------------------------------------------------------+--------------+
   | BOOMI_COMPONENT_REPO_NAME   | COMPONENT_REPO_NAME      | Name of the component repository                        | Optional     |
   +-----------------------------+--------------------------+---------------------------------------------------------+--------------+
   | BOOMI_SONARQUBE_HOST_URL    | SONARQUBE_HOST_URL       | URL of the SonarQube server                             | Optional     |
   +-----------------------------+--------------------------+---------------------------------------------------------+--------------+
   | BOOMI_SONARQUBE_PROJECT_KEY | SONARQUBE_PROJECT_KEY    | Project key of the SonarQube project                    | Optional     |
   +-----------------------------+--------------------------+---------------------------------------------------------+--------------+
   | BOOMI_SONARQUBE_TOKEN       | SONARQUBE_TOKEN          | Token of the SonarQube project                          | Optional     |
   +-----------------------------+--------------------------+---------------------------------------------------------+--------------+
   | BOOMI_API_CALLS             | API_CALLS                | Number of API calls to make per minute. Defaults to 10  | Optional     |
   +-----------------------------+--------------------------+---------------------------------------------------------+--------------+



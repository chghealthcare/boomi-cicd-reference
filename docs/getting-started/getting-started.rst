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

1. component_xml_git.py: Copy the a git repositoy locally and add the component xml files from the release file. Then, commit and push the change.
2. component_xml_code_quality.py: The component xml files will be validated against the /boomi_cicd/util/sonarqube/BoomiSonarRules.xml or a custom rules file. The validate will create a report within the components repository.
3. component_xml_sonarqube.py: Similar to the component_xml_code_quality.py script, but this script will push the results to a SonarQube server.
4. release_pipeline.py: This script will deploy the package components to a specific Boomi environment.
5. environment_extensions_update.py: Update the environment extensions before the process schedules are set.
6. release_pipeline_scedules.py: Set the process schedules for the deployed components.
7. release_pipeline_dr.py: If using an active-active architecture, then this script will enable the packaged components on the disaster recovery runtime.


Release JSON File
----------------------------

The scripts mentioned above are based on the release.json file. The file includes all components that need to be
deployed and any schedules or listener status that needs to be configured.

.. include:: release.rst


Environment Variables
----------------------------

Environment variables are used the set the variables for the library. Below are a list of the environment variables that ared used within the library and found within the boomi_cicd.util.contants.py file. Not all are required for all scripts. More details on which script requires which enviornment can be found within the `example script documentation <../example-scripts/example-cicd-scripts.html>`_.

.. table:: Environment Variables
   :align: center
   :width: 100%

   +-------------------------+--------------------------+---------------------------------------------------+--------------------------------------------------------------------------------+
   | Environment Variable    | boomi_cicd Constant Name | Description                                       | Required                                                                       |
   +=========================+==========================+===================================================+================================================================================+
   | BOOMI_BASE_URL          | BASE_URL                 | The base URL of the Boomi account                 | Yes                                                                            |
   +-------------------------+--------------------------+---------------------------------------------------+--------------------------------------------------------------------------------+
   | BOOMI_ACCOUNT_ID        | ACCOUNT_ID               | The account ID of the Boomi account               | Yes                                                                            |
   +-------------------------+--------------------------+---------------------------------------------------+--------------------------------------------------------------------------------+
   | BOOMI_USERNAME          | USERNAME                 | The username of the Boomi account                 | Yes                                                                            |
   +-------------------------+--------------------------+---------------------------------------------------+--------------------------------------------------------------------------------+
   | BOOMI_PASSWORD          | PASSWORD                 | The password of the Boomi account                 | Yes                                                                            |
   +-------------------------+--------------------------+---------------------------------------------------+--------------------------------------------------------------------------------+
   | BOOMI_ENVIRONMENT_NAME  | ENVIRONMENT_NAME         | The environment name used to deploy to components | Yes                                                                            |
   +-------------------------+--------------------------+---------------------------------------------------+--------------------------------------------------------------------------------+
   | BOOMI_ATOM_NAME         | ATOM_NAME                | The atom name used to set set schedules           | Yes                                                                            |
   +-------------------------+--------------------------+---------------------------------------------------+--------------------------------------------------------------------------------+
   | BOOMI_ATOM_NAME_DR      | ATOM_NAME_DR             | The atom name of the disaster recovery atom       | Optional ([release_pipeline_dr.py](boomi_cicd/scripts/release_pipeline_dr.py)) |
   +-------------------------+--------------------------+---------------------------------------------------+--------------------------------------------------------------------------------+
   | BOOMI_COMPONENT_GIT_URL | COMPONENT_GIT_URL        | git URL of the component repository               | Optional ([component_xml_git.py](boomi_cicd/scripts/component_xml_git.py))     |
   +-------------------------+--------------------------+---------------------------------------------------+--------------------------------------------------------------------------------+
   | BOOMI_CLI_BASE_DIR      | CLI_BASE_DIR             | Base directory of the boomi_cicd scripts          | Yes                                                                            |
   +-------------------------+--------------------------+---------------------------------------------------+--------------------------------------------------------------------------------+
   | BOOMI_CLI_RELEASE_DIR   | CLI_RELEASE_DIR          | Base directory of the release.json file           | Yes                                                                            |
   +-------------------------+--------------------------+---------------------------------------------------+--------------------------------------------------------------------------------+
   | BOOMI_CLI_RELEASE_FILE  | CLI_RELEASE_FILE         | Name of the release.json file                     | Yes                                                                            |
   +-------------------------+--------------------------+---------------------------------------------------+--------------------------------------------------------------------------------+



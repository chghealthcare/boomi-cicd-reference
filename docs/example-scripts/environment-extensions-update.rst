.. _environment_extensions_update:

environment_extensions_update
=============================

The environment_extensions_update script is used to update the environment extensions for a given environment. The script is intended to run after the `release_pipeline script <release_pipeline.html>`_ has been ran.

.. warning::
   A word of caution about updating environment extensions. Ensure that partial is set to true. If not, the default action is to reset all environment extensions. Therefore, if you only try to update a few values, then the rest will be set to default.


.. literalinclude:: ../../boomi_cicd/scripts/environment_extensions_update.py
   :language: python
   :linenos:


Required Environment Variables
------------------------------

+-----------------------+-----------------------------------------------------------------------------+
| Environment Variable  | Description                                                                 |
+=======================+=============================================================================+
| BOOMI_ACCOUNT_ID      | The Boomi account ID.                                                       |
+-----------------------+-----------------------------------------------------------------------------+
| BOOMI_ATOM_NAME       | The name of the Boomi Atom.                                                 |
+-----------------------+-----------------------------------------------------------------------------+
| BOOMI_ATOM_NAME_DR    | The name of the Boomi Atom.                                                 |
+-----------------------+-----------------------------------------------------------------------------+
| BOOMI_BASE_URL        | The base URL for the Boomi API. https://api.boomi.com/api/rest/v1           |
+-----------------------+-----------------------------------------------------------------------------+
| BOOMI_CLI_BASE_DIR    | The base directory for the Boomi CLI.                                       |
+-----------------------+-----------------------------------------------------------------------------+
| BOOMI_PASSWORD        | The Boomi password. Atomsphere API Token is recommended                     |
+-----------------------+-----------------------------------------------------------------------------+
| BOOMI_RELEASE_BASE_DIR| The base directory for the release JSON file.                               |
+-----------------------+-----------------------------------------------------------------------------+
| BOOMI_RELEASE_FILE    | The name of the release JSON file to use. The release file contains         |
|                       | the environment extensions to be updated.                                   |
+-----------------------+-----------------------------------------------------------------------------+
| BOOMI_USERNAME        | The Boomi username. Atomsphere API Token is recommended                     |
+-----------------------+-----------------------------------------------------------------------------+


Command Line Arguments
----------------------

* -r, --release_file: The release JSON file to use. If not specified, then the BOOMI_RELEASE_FILE environment variable
  will be used.

Release JSON File
-----------------

The release file contains the environment extensions JSON. Additional information about environment extensions can be found within `Boomi's documention <https://help.boomi.com/bundle/developer_apis/page/int-Environment_extensions_object.html>`_. Below is an example of a environment extensions release file.

.. literalinclude:: ../../boomi_cicd/templates/releaseEnvironmentExtensions.json
   :language: json
   :linenos:


.. _release_pipeline:

Release Pipeline
============================

The ``release_pipeline.py`` script is the main script used within the boomi_cicd library. It will read through a release JSON
file and creating the package, deploy the processes, schedules, and listener status as defined in the file.

If the package version is not created, then the script will create the package component. Then it will deploy the
version of the packaged component to the desired environment. If the process is a listener, then the listener status
will be set to what is within the release JSON file. If nothing is set, then it defaults to RUNNING. Finally, if a
schedule is defined, then the schedule will be set to the desired schedule.

.. literalinclude:: ../../boomi_cicd/scripts/release_pipeline.py
   :language: python
   :linenos:

Required Environment Variables
------------------------------
.. table:: Required Environment Variables
   :width: 100%
   :align: left

   +-----------------------+-----------------------------------------------------------------------------+
   | Environment Variable  | Description                                                                 |
   +=======================+=============================================================================+
   | BOOMI_ACCOUNT_ID      | The Boomi account ID.                                                       |
   +-----------------------+-----------------------------------------------------------------------------+
   | BOOMI_ATOM_NAME       | The name of the Boomi Atom.                                                 |
   +-----------------------+-----------------------------------------------------------------------------+
   | BOOMI_BASE_URL        | The base URL for the Boomi API. https://api.boomi.com/api/rest/v1           |
   +-----------------------+-----------------------------------------------------------------------------+
   | BOOMI_ENVIRONMENT_NAME| The Boomi environment name.                                                 |
   +-----------------------+-----------------------------------------------------------------------------+
   | BOOMI_PASSWORD        | The Boomi password. Atomsphere API Token is recommended                     |
   +-----------------------+-----------------------------------------------------------------------------+
   | BOOMI_RELEASE_FILE    | The name of the release JSON file to use.                                   |
   +-----------------------+-----------------------------------------------------------------------------+
   | BOOMI_USERNAME        | The Boomi username. Atomsphere API Token is recommended                     |
   +-----------------------+-----------------------------------------------------------------------------+








Command Line Arguments
----------------------

* -r, --release_file: The release JSON file to use. If not specified, then the BOOMI_RELEASE_FILE environment variable
  will be used.

Release JSON File
-----------------

.. literalinclude:: ../../boomi_cicd/templates/release.json
   :language: json
   :linenos:


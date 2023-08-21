.. _release_pipeline_dr:

Release Pipeline DR
====================

The ``release_pipeline_dr.py`` script is an example of how to perform a DR failover for two atoms within a single Boomi Environment and with an active-active DR configuration. The script will turn off schedules and listeners in the atom that is down and turn on schedules and listeners on the other atom. When the down atom come back online, it will initially sync with the Boomi platform and the action to turn off schedules and listeners will occur then. The script will loop through the release file that is used within the release_pipeline script. That way, the same processes that are deployed during the initial release will failover.


.. literalinclude:: ../../boomi_cicd/scripts/release_pipeline_dr.py
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


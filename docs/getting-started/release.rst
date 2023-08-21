release json
============

.. literalinclude:: ../../boomi_cicd/templates/release.json
   :language: json
   :linenos:


.. table:: Release JSON Elements
   :align: center
   :width: 100%

   +----------------------+------------------------------------------------------------------------------------------------------------------+
   | Release JSON Element | Description                                                                                                      |
   +======================+==================================================================================================================+
   | processName          | Name of the process. Mainly used for human readability.                                                          |
   +----------------------+------------------------------------------------------------------------------------------------------------------+
   | packageVersion       | Define the package version. If one isn't specified, the latest version will be used.                             |
   +----------------------+------------------------------------------------------------------------------------------------------------------+
   | componentId          | The component ID of the process to deploy.                                                                       |
   +----------------------+------------------------------------------------------------------------------------------------------------------+
   | notes                | The notes that will be added to the packaged components and deployments.                                         |
   +----------------------+------------------------------------------------------------------------------------------------------------------+
   | schedule             | The schedule that will be used to deploy the process. Each individual schedule is space delimited. Multiple      |
   |                      | schedules are semi-colon delimited. Additional notes below.                                                      |
   +----------------------+------------------------------------------------------------------------------------------------------------------+
   | listenerStatus       | The status of the listener when deployed. Values: RUNNING or PAUSED. RUNNING is default.                         |
   +----------------------+------------------------------------------------------------------------------------------------------------------+


The ``schedule`` element requires six space-delimited values in the following order: minutes, hours, days of the week, days of the month, month, and year. For example, ``0 0 1 * * *`` executes the process every Sunday at midnight.


.. table:: Schedule Element Values
   :align: center
   :width: 100%

   +-------------+-----------------------------------------------------------------------------------------------------------------------+
   | Field       | Description                                                                                                           |
   +=============+=======================================================================================================================+
   | minutes     | 0 is the first minute of the hour — for example, 1:00 A.M. 59 is the last minute of the hour — for example, 1:59 A.M. |
   +-------------+-----------------------------------------------------------------------------------------------------------------------+
   | hours       | Uses a 24-hour clock. 0 is midnight and 12 is noon.                                                                   |
   +-------------+-----------------------------------------------------------------------------------------------------------------------+
   | daysOfWeek  | 1 is Sunday and 7 is Saturday.                                                                                        |
   +-------------+-----------------------------------------------------------------------------------------------------------------------+
   | daysOfMonth | 1 is the first day of the month and 31 is the last day of the month.                                                  |
   +-------------+-----------------------------------------------------------------------------------------------------------------------+
   | month       | 1 is January and 12 is December. Often set to an asterisk [*].                                                        |
   +-------------+-----------------------------------------------------------------------------------------------------------------------+
   | year        | 4 digit year - for example, 2023. Often set to an asterisk [*].                                                       |
   +-------------+-----------------------------------------------------------------------------------------------------------------------+

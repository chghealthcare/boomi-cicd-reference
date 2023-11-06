Introduction to boomi-cicd-cli-py
=================================

The boomi-cicd-cli-py library enables automated Boomi deployments through seamless integration with your existing CI/CD pipelines. It facilitates the orchestration of Boomi runtimes, components, and essential metadata for efficient CI/CD workflows.


Project Structure
=================

The project is organized into three sections:

1. scripts: Contains scripts designed to be executed within your CI/CD pipeline. The main script is release_pipeline.py, and there are additional example scripts available as starting points for your own pipelines.
2. util: Contains the core functionality of the library.
3. templates: Contains release pipeline templates that can be used as-is or customized for your specific requirements.


Pre-requisites
==============
* Python 3.6 or higher
* Additional libraries, which can be installed with ``pip install -r requirements.txt``
* git v1.7.0 or higher: Optional. Only required when executing ``component_xml_git.py``


Documemtation Overview
======================

Below is a list of the documentation available:

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   getting-started/getting-started
   example-scripts/example-cicd-scripts
   pipelines/release-pipeline-configuration
   modules/modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. NeuroFlow documentation master file, created by
   sphinx-quickstart on Thu Jan  9 03:03:36 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. |ncm_lab_link| raw:: html

   <a href="https://uwaterloo.ca/neurocognition-mobility-lab/" target="_blank">Neurocognition & Mobility Lab</a>

.. |kedro_link| raw:: html

   <a href="https://kedro.org/" target="_blank">Kedro</a>

.. |neuroflow_link| raw:: html

   <a href="https://github.com/neurocog-mobility/neuroflow" target="_blank">Github</a>

Welcome to NeuroFlow
=======================

NeuroFlow is an open-source package from the |ncm_lab_link|
for running analytics pipelines on experimental data, and is built on the |kedro_link| framework.

The NeuroFlow documentation serves to:

* get started with a scientific computing environment for reseachers.

* provide tutorials for using NeuroFlow on experiment data.

* reference API documentation.


Quickstart
----------
Detailed instructions for getting set up can be found in the :doc:`getting-started/getting-started` section.

To quickly start using NeuroFlow:

1. Clone the NeuroFlow repository from |neuroflow_link|.

.. code-block:: powershell

   git clone git@github.com:neurocog-mobility/neuroflow.git
   
2. Install NeuroFlow from the project root.

.. code-block:: powershell

   pip install -e .
   
3. Test the installation, then create your first NeuroFlow project!

.. code-block:: powershell

   python -m neuroflow --help


.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :hidden:
   
   ./getting-started/getting-started.rst
   ./overview/overview.rst
   ./tutorials/tutorials.rst
   ./source/neuroflow.rst


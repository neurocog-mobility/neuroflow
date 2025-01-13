.. NeuroFlow documentation master file, created by
   sphinx-quickstart on Thu Jan  9 03:03:36 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to NeuroFlow
=======================

NeuroFlow is an open-source package from the `Neurocognition & Mobility Lab <https://uwaterloo.ca/neurocognition-mobility-lab//>`_
for running analytics pipelines on experimental data built on the `Kedro <https://kedro.org/>`_ framework.

The NeuroFlow documentation serves to:

* get started with a scientific computing environment for reseachers.

* provide tutorials for using NeuroFlow on experiment data.

* reference API documentation.


Quickstart
----------

1. Clone the NeuroFlow repository from `GitHub <https://github.com/neurocog-mobility/neuroflow>`_.

.. code-block:: console

   git clone git@github.com:neurocog-mobility/neuroflow.git
   
2. Install the required Python packages.

.. code-block:: console

   pip install requirements.txt
   
3. Visualize the pre-loaded pipelines.

.. code-block:: console

   kedro viz


.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :hidden:
   
   ./onboarding/onboarding.rst
   ./tutorials/tutorials.rst
   ./source/modules


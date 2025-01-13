"""
.. module:: utils

This package provides utility functions to set up a NeuroFlow experiment.

**Modules:**

* `create_experiment`: Create an experiment directory
* `collect`: Collect raw files for the experiment

**Classes:**

* `Sensor`: Class to hold sensor data
    * `load_axivity`: Load Axivity data
    * `load_bittium`: Load Bittium data

**Example Usage:**

.. code-block:: python

	from neuroflow.neuroflow.utils import create_experiment, collect

	# Create a new experiment folder and stage csv files for processing

	new_experiment = "path/to/experiment_folder"

	create_experiment._create_experiment(new_experiment)

	collect._collect("/raw/source/", new_experiment, "*.csv", "csv_files")


"""

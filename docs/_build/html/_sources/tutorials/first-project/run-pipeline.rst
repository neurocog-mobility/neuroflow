Running the pipeline
=================================

Move onto the final code cell (under **5. Run the pipeline**) and run it.

You will see a log of the pipeline run as it proceeds over each node, with
updates as each step in the pipeline completes.

Once the pipeline has completed, you should see the following confirmation in the
cell output:

.. code:: powershell

    INFO     Completed 11 out of 11 tasks                                   sequential_runner.py:93
    INFO     Pipeline execution completed successfully.                               runner.py:115

Let's check the pipeline outputs!

Open the ``data/processed`` subfolder in your project to view the different outputs:

* **output_axivity_rawdata**: The raw accelerometry data split for each trial as a .csv file.
* **output_axivity_rawplots**: Plots of the raw accelerometry data split for each trial.
* **output_axivity_stepdata**: The raw accelerometry data split for each step as a .csv file.
* **output_axivity_stepplots**: Plots of the raw accelerometry data split for each step.
* **output_axivity_stepprofiles**: Plots of the accelerometry step profiles for each step in each trial.
* **output_axivity_stepsummary**: A table of summary metrics describing each step across the entire dataset.
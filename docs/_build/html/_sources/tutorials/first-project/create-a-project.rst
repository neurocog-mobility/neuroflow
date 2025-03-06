.. |open_terminal| raw:: html

    <a href="../../getting-started/useful-info.html#using-the-terminal:">Open a terminal</a>

.. |run_jupyter| raw:: html

    <a href="../../getting-started/useful-info.html#launching-jupyter-on-windows:">Launching Jupyter</a>

.. |neuroflow_init| raw:: html

    <a href="../../getting-started/neurflow-setup.html#initializing-neuroFlow:">Initializing NeuroFlow</a>

.. |neuroflow_create| raw:: html

    <a href="../../overview/creating-a-project.html">creating a project</a>

Initializing a NeuroFlow project
======================================

We will want a **project folder** separate from the data folder for our analysis 
where we can keep all the scripts, data and processed outputs for each analysis
we want to run.

Creating the project folder
------------------------------------

This section will go over |neuroflow_create| folder for the tutorial pipeline:

1. |open_terminal| in the location you want your project folder to be created (e.g. the ``Documents`` folder).

2.
    Enter the following command: ``python -m neuroflow --create tutorial_pipeline``

    .. note::

        Remember to use ``python`` or ``python3`` according to your system.

3.
    You should be the following output in the terminal, indicating the project was created successfully!

    .. code:: powershell

        [03/02/25 02:55:33] INFO     Using                                         __init__.py:270
                             '/usr/local/lib/python3.10/dist-packages/kedr                
                             o/framework/project/rich_logging.yml' as                     
                             logging configuration.                                       
        -> Creating project: /Documents/tutorial_pipeline
        /Documents/tutorial_pipeline
        --> Project folder created successfully: /Documents/tutorial_pipeline
        --> Creating notebook templates...
        --> Successfully created Jupyter notebooks.
        --> Notebook configured successfully.

| A ``tutorial_pipeline`` folder should now appear in your chosen project location.
| Let's look at the project structure:

::

    tutorial_pipeline
    ├── catalogs
    ├── data
    │   ├── processed
    │   └── raw
    ├── tutorial_pipeline.ipynb
    ├── tutorial_pipeline_dev.ipynb


Loading & initializing NeuroFlow
------------------------------------

Let's open ``tutorial_pipeline.ipynb`` (see |run_jupyter| for help) and load up NeuroFlow.

1.
    Ensure that Jupyter is using the ``Kedro (neuroflow)`` kernel (instead of a base Python kernel) by
    checking the label in the right side of the top panel:

    .. figure:: static/kernel.png

    If another kernel is being used, click the label to switch the kernel and select ``Kedro (neuroflow)``
    from the selection menu. If you do not see an option for ``Kedro (neuroflow)``, refer to the |neuroflow_init| instructions.

2.

    With the Notebook open, click in the first code cell under the section **1. Load NeuroFlow** to select it
    and run it by pressing ``Ctrl + Enter`` (or by clicking the Play icon at the top of the Notebook).

    .. figure:: static/run_1.png

3.
    You should see the following cell output, with a message of ``Neuroflow loaded successfully.``

    .. figure:: static/out_1.png

We can now move on to exploring the NeuroFlow pipelines!
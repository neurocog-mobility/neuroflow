Creating a project
=======================

.. |open_terminal| raw:: html

    <a href="../../getting-started/useful-info.html#using-the-terminal:">Open a terminal</a>

.. |run_jupyter| raw:: html

    <a href="../../getting-started/useful-info.html#launching-jupyter-on-windows:">Launching Jupyter</a>

.. |neuroflow_init| raw:: html

    <a href="../../getting-started/neurflow-setup.html#initializing-neuroFlow:">Initializing NeuroFlow</a>

A NeuroFlow project is a folder where we can keep all the scripts,
data, and processed outputs for each analysis
we want to run.

The ``neuroflow --create`` command
------------------------------------

This section will go over the buil-in NeuroFlow commands to create a project folder for you:

1. |open_terminal| in the location you want your project folder to be created (e.g. the ``Documents`` folder).

2.
    Enter the following command (replacing ``<project_name>`` with the name of your project):
    
    .. code:: powershell

        python -m neuroflow --create <project_name>

    .. note::

        Remember to use ``python`` or ``python3`` according to your system.

3.
    You should see the following output in the terminal, indicating the project was created successfully!

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

| A ``<project_name>`` folder should now appear in your chosen project location with the following structure:

::

    project_name
    ├── catalogs
    ├── data
    │   ├── processed
    │   └── raw
    ├── <project_name>.ipynb
    ├── <project_name>_dev.ipynb


* ``catalogs`` contains data and parameter **Catalog** files to run project pipelines.
* ``data`` contains both ``raw`` and ``processed`` subfolders, where the pipeline inputs & outputs will be loaded from.

Finally, ``<project_name>.ipynb`` and ``<project_name>_dev.ipynb`` are Jupyter notebooks with program templates
for runing existing NeuroFlow pipelines and developing using the NeuroFlow package, respectively.
| Have a look at :doc:`../tutorials/first-project/first-project` or :doc:`../tutorials/dev-notebook/dev-notebook` for
tutorials on how to use these Notebooks!


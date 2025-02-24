.. |neuroflow_link| raw:: html

    <a href="https://github.com/neurocog-mobility/neuroflow" target="_blank">Github</a>

.. |jupyter_link| raw:: html

    <a href="https://jupyter.org/" target="_blank">Jupyter</a>

NeuroFlow setup
======================

Downloading NeuroFlow
-----------------------

To download NeuroFlow:

1.  Navigate to the NeuroFlow |neuroflow_link| page.

2.  Click the ``<> Code`` dropdown button and then select ``Download ZIP`` to download the source files.

    .. image:: static/nf_github.png

3. Extract the **neuroflow-main.zip** folder to your preferred installation location.

.. note::

    Alternatively, you can clone the source files directly using git commands:

    .. code-block:: powershell

        git clone git@github.com:neurocog-mobility/neuroflow.git

Installing NeuroFlow
-----------------------

1. Navigate to extracted folder (default **neuroflow-main**).

2. Open a terminal in the folder (e.g. by right-clicking in the folder and selecting *Open in terminal*).

3.
    Enter the following command into the terminal:
    
    .. code-block:: powershell
        
        pip -vvv install -e .

    .. note::
        If you have a fresh Python installation, this may take some time.

    Once complete, the terminal should say ``Successfully installed neuroflow``.

4.
    To test the installation enter the following command into the terminal:
    
    .. code-block:: powershell
    
        python -m neuroflow --help

    .. note::

        Some systems may use ``python3`` instead of ``python``. If you get a message ``Command 'python' not found.``
        then try again using: ``python3 -m neuroflow --help``.

    The response should be:

    .. code-block:: powershell

        Usage: python -m neuroflow [OPTIONS]

        Create a new project.

        Options:
        -cr, --create TEXT  Create a new NeuroFlow project in the given directory.
                            Example: neuroflow --create [DIRECTORY] where
                            [DIRECTORY] is the project directory
        --help              Show this message and exit.


Initializing NeuroFlow
-----------------------

With a terminal open in the NeuroFlow root folder (i.e. the installation folder from above, default **neuroflow-main**),
enter the following command:

.. code-block:: powershell
    
    kedro jupyter notebook


The terminal will start a server, then open a browser window with the |jupyter_link| file explorer
in the NeuroFlow root folder:


.. image:: static/nf_jupyter.png


You can now shutdown the Notebook by clicking *File > Shut Down* and close the browser window.

You are now ready to use NeuroFlow on your system!
Proceed to :doc:`../overview/overview` to learn more about the components of NeuroFlow or
check out the :doc:`../tutorials/tutorials` to learn how to run your first pipeline.

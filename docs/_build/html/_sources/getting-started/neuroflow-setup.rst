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

2.  Click the ``<> Code`` menu button.

3.
    Click ``Download ZIP`` to download the source files.

    .. image:: static/nf_github.png

4. Extract the **neuroflow-main.zip** folder to your preferred installation location.

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


You can close the browser window and stop the server in the terminal window using ``Ctrl-C``.

If you have already used Jupyter notebooks on your system, you are ready to run your first pipeline!
Proceed to :doc:`../tutorials/tutorials`.

Optionally, you can follow the guide below if needed on how to launch Jupyter notebooks for Windows systems.

(Optional) Launching Jupyter on Windows
---------------------------------------

.. note::

    The following steps are to setup how Jupyter Notebooks are started on your system.
    If you can already open Jupyter Notebooks on your system
    (by double-clicking **.ipynb** files or by using the terminal), you can skip these steps!

If Windows does not recognize the **.ipynb** file type, then you have two options to launch Notebooks:

* **Option A:**
    If you want to launch a Notebook by double-clicking on the file:

    1.
        Open a terminal and enter the following command:

        .. code-block:: powershell

            python -m nbopen.install_win

    2.
        Back in the **neuroflow-main** folder, you should now be able to double-click on **nf-test.ipynb** to open it.

* **Option B:**
    You can also launch Notebooks using terminal commands. Open a terminal in the folder containing the Notebook (in this case the **neuroflow-main** folder) and enter the following command:

    .. code-block:: powershell

        jupyter notebook nf-test.ipynb

    In general, replace ``nf-test.ipynb`` with the name of the Notebook you want to open.

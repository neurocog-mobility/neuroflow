Useful Information
=====================

.. _using-terminal:

Using the Terminal
-----------------------

A terminal is a text-based interface that lets you communicate with a computer's operating system.
It's also known as a command-line interface (CLI).

To launch a terminal on Windows, enter "Terminal" into the program search bar.
Closing the terminal window will also stop any processes currently running in the terminal.

To open a terminal in a specific folder, you can:

* **Option A:**
    Use the command: ``cd <path_to_folder>``

    Where you can replace ``<path_to_folder>`` with the folder path you would like to execute terminal commands in.

* **Option B:**
    Open the folder using File Explorer, then right-click in the folder and select **Open in Terminal**.


When copying/pasting text into the terminal, you can use the keyboard shortcuts
``Ctrl + Shift + C`` / ``Ctrl + Shift + V`` for copy/paste, respectively.

.. _checking_python:

Checking Python version
--------------------------

You can check which version of Python is installed by opening a :ref:`Terminal <using-terminal>` and entering
the command ``python -V``.

.. note::

    Some systems may use ``python3`` instead of ``python``. If you get a message ``Command 'python' not found.``
    then try again using: ``python3 -V``.


.. _running-jupyter:

Launching Jupyter on Windows
-------------------------------

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
        You should now be able to double-click on **.ipynb** to open it.

* **Option B:**
    You can also launch Notebooks using terminal commands. Open a terminal in the folder containing the Notebook (in this case the **neuroflow-main** folder) and enter the following command:

    .. code-block:: powershell

        jupyter notebook <notebook.ipynb>

    In general, replace ``<notebook.ipynb>`` with the name of the Notebook you want to open.

When closing a Jupyter Notebook, it is important to also close the Jupyter server being run with the Notebook.
| The simplest way to do so is to click ``File > Shut Down`` from the navigation menu.
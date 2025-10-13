# Useful Information

## Using the Terminal

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


## Checking Python version

You can check which version of Python is installed by opening a [Terminal](#using-the-terminal) and entering
the command ``python -V``.

!!! note "Important"

    Some systems may use ``python3`` instead of ``python``. If you get a message ``Command 'python' not found.``
    then try again using: ``python3 -V``.

## Using virtual environments

Creating and using a virtual environment in Python is a crucial step for managing project dependencies. It ensures that each project has its own isolated set of packages, preventing conflicts between different projects.

1. **Create**: First, navigate to your project's root directory in your terminal. We'll name the virtual environment folder ```.venv``` (this is a common convention).

    ```
    python -m venv .venv
    ```

2. **Activate**: Before installing any packages for your project, you must activate the virtual environment. Activation changes your terminal's shell so that the ```python``` command points to the version inside the ```.venv``` folder, and ```pip``` installs packages there.

    * Windows (Powershell): ```.\.venv\Scripts\Activate.ps1```
    * Windows (Command Prompt): ```.\.venv\Scripts\activate.bat```
    * Mac/Linux: ```source .venv/bin/activate```

Once activated, your terminal prompt will usually be prefixed with the name of the environment (e.g., (.venv)):
```
(.venv) $
```


## Launching Jupyter on Windows

!!! note "Important"

    The following steps are to setup how Jupyter Notebooks are started on your system.
    If you can already open Jupyter Notebooks on your system
    (by double-clicking **.ipynb** files or by using the terminal), you can skip these steps!

If Windows does not recognize the **.ipynb** file type, then you have two options to launch Notebooks:

* **Option A:**
    If you want to launch a Notebook by double-clicking on the file:

    1.
        Open a terminal and enter the following command:

        ```
        python -m nbopen.install_win
        ```

    2.
        You should now be able to double-click on **.ipynb** to open it.

* **Option B:**
    You can also launch Notebooks using terminal commands. Open a terminal in the folder containing the Notebook (in this case the **neuroflow-main** folder) and enter the following command:

    ```
    jupyter notebook <notebook.ipynb>
    ```

    In general, replace ``<notebook.ipynb>`` with the name of the Notebook you want to open.

When closing a Jupyter Notebook, it is important to also close the Jupyter server being run with the Notebook.
The simplest way to do so is to click ``File > Shut Down`` from the navigation menu.
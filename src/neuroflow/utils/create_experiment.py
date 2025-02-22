"""
Module to create template experiment folder for running pipeline analysis. \n

Parameters
----------
folderpath : str
    The path to create the root experiment directory in.

"""

import os
import shutil
import sys
import nbformat
import textwrap

def _create_experiment(folderpath: str):
    # make folder path absolute
    folderpath = os.path.realpath(os.path.expanduser(folderpath))

    print(folderpath)

    # check if experiment folder exists
    is_valid = True
    if os.path.exists(folderpath):
        val = input("Experiment folder exists. Would you like to overwrite it? (y/n) [n]: ") or "n"
        print(val)

        if val == "n":
            is_valid = False
        else:
            # remove existing directory before continuing
            shutil.rmtree(folderpath)

    # create experiment folder
    if is_valid:
        os.mkdir(folderpath)
        os.mkdir(os.path.join(folderpath, "catalogs"))
        os.mkdir(os.path.join(folderpath, "data"))
        os.mkdir(os.path.join(folderpath, "data", "raw"))
        os.mkdir(os.path.join(folderpath, "data", "processed"))

        print("--> Project folder created successfully: " + folderpath)


def configure_notebook_templates(notebook_path):
    """Configures Jupyter Notebook templates.

    Args:
        notebook_path: Path to the Jupyter Notebook file (.ipynb).
    """

    try:
        with open(notebook_path, 'r') as f:
            nb = nbformat.read(f, as_version=4) # Important to specify version 4

        # Set path definitions
        neuroflow_root = \
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(__file__))))
        cell_content = f'''
        # SET PATH DEFINITIONS
        NEUROFLOW_ROOT = "{neuroflow_root}"
        PROJECT_ROOT = "{os.path.dirname(notebook_path)}"
        print("Path definitions set.")
        '''
        
        nb.cells[0].source = textwrap.dedent(cell_content)    

        with open(notebook_path, 'w') as f:
            nbformat.write(nb, f)

    except FileNotFoundError:
        print(f"Error: Notebook file not found at {notebook_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    folderpath = sys.argv[1]

    _create_experiment(folderpath)
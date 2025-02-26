import os
import shutil
import sys
import nbformat

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
    """
    
    :meta private:
    
    Configures Jupyter Notebook templates.

    Args:
        notebook_path: Path to the Jupyter Notebook file (.ipynb).
    """

    try:
        neuroflow_root = \
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(__file__))))
        project_root = os.path.dirname(notebook_path)
        with open(notebook_path, 'r') as f:
            nb = nbformat.read(f, as_version=4) # Important to specify version 4

        # find first code cell
        cell_type = [cell["cell_type"] for cell in nb["cells"]]
        cell_init_idx = cell_type.index("code")
        cell_init = nb["cells"][cell_init_idx]

        source_init = cell_init["source"]

        # find ROOT substrings
        source_lines = source_init.split("\n")
        nf_sub = "NEUROFLOW_ROOT = "
        line_nf = [nf_sub in line for line in source_lines]
        line_nf = [i for i, x in enumerate(line_nf) if x][0]

        pr_sub = "PROJECT_ROOT = "
        line_pr = [pr_sub in line for line in source_lines]
        line_pr = [i for i, x in enumerate(line_pr) if x][0]

        # update ROOT substrings
        source_lines[line_nf] = f'{nf_sub}r"{neuroflow_root}"'
        source_lines[line_pr] = f'{pr_sub}r"{project_root}"'

        source_new = "\n".join(source_lines)
        
        nb.cells[cell_init_idx].source = source_new

        # reset all code outputs
        for c, cell in enumerate(nb["cells"]):
            if cell["cell_type"] == "code":
                cell["outputs"] = []

                nb["cells"][c] = cell

        with open(notebook_path, 'w') as f:
            nbformat.write(nb, f)

    except FileNotFoundError:
        print(f"Error: Notebook file not found at {notebook_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    folderpath = sys.argv[1]

    _create_experiment(folderpath)

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
        os.mkdir(os.path.join(folderpath, "01_raw"))
        os.mkdir(os.path.join(folderpath, "02_processed"))
        os.mkdir(os.path.join(folderpath, "03_output"))

        print("Experiment folder created successfully: " + folderpath)


if __name__ == "__main__":
    folderpath = sys.argv[1]

    _create_experiment(folderpath)
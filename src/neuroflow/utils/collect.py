"""

Module to collect all files matching a filepattern from an experiment directory
into a single data folder for loading into a Kedro catalog. \n

Parameters
----------
source_dir : str
    The source directory to search for data files.
target_dir : str
    The target experiment root directory.
filepattern : str
    The filepattern to match data files with.
sub_dir (optional): str
    The subdirectory within the experiment/01_raw to copy files into.

"""

import pandas as pd
import os
import glob
from functools import reduce
import sys
import shutil

def adjust_name(filepath, filename):
    prefix = os.path.basename(filepath)

    return f"{prefix}_{filename}"

def _copy_matching_files(source_dir: str, target_dir: str, filepattern: str,
                         expand = False):
    for root, _, files in os.walk(source_dir, topdown=False):
        for file in files:
            if glob.fnmatch.fnmatch(file, filepattern):
                filepath = os.path.join(root, file)

                # adjust name
                if expand:
                    file = adjust_name(root, file)

                print(f"Copying {file}")
                shutil.copyfile(filepath,
                                os.path.join(target_dir, file))


def _collect(source_dir : str, target_dir : str, filepattern : str, sub_dir : str = None,
             expand = False):
    # make path absolute
    source_dir = os.path.realpath(os.path.expanduser(source_dir))
    target_dir = os.path.realpath(os.path.expanduser(target_dir))

    # check if target folder exists
    try:
        os.listdir(target_dir)
    except:
        print("\n")
        print(f"Target folder {target_dir} does not exist. \n")
        sys.exit(1)

    # check if target folder was root of experiment folder
    if "01_raw" in os.listdir(target_dir):
        target_dir_raw = os.path.join(target_dir, "01_raw")
        if sub_dir:
            target_dir_raw = os.path.join(target_dir_raw, sub_dir)

        # check if sub directory exists already, otherwise create it
        os.makedirs(target_dir_raw, exist_ok=True)

        _copy_matching_files(source_dir, target_dir_raw, filepattern, expand)
        print("\n")
        print(f"{len(os.listdir(target_dir_raw))} files collected.")
        print(f"Raw files ready for processing. Use {target_dir_raw} in pipeline catalog.yml \n")
    else:
        print("\n")
        print(f"Target folder {target_dir} is not a valid experiment directory root. Use the create_experiment.py function to create a experiment directory \n")


if __name__ == "__main__":
    # check number of arguments
    try:
        source_dir = sys.argv[1]
        target_dir = sys.argv[2]
        filepattern = sys.argv[3]
    except:
        print("Provide --source_directory --target_directory --filepattern")
        sys.exit(1)
    
    if len(sys.argv) == 5:
        sub_dir = sys.argv[4]
    else:
        sub_dir = None
    
    _collect(source_dir, target_dir, filepattern, sub_dir)
    
    



from neuroflow.pipeline_registry import get_pipeline_registry
from neuroflow.utils.utils import _format_text
from neuroflow.utils.collect import _collect
from IPython.display import clear_output
import os

def input_axivity_dataset():
    """ Axivity dataset.
    """
    return {
        "requires_input": True,
        "pathtype": "directory",
        "modality": "axivity",
        "filepattern": "*.cwa",
        "catalog": {
            "type": "partitions.IncrementalDataset",
            "path": "",
            "dataset": "neuroflow.datasets.axivity_dataset.AxivityDataset"
        },
    }

def input_sync_dataset():
    """ Sync dataset.
    """
    return {
        "requires_input": True,
        "pathtype": "directory",
        "modality": "sync",
        "filepattern": "*.csv",
        "catalog": {
            "type": "partitions.IncrementalDataset",
            "path": "",
            "dataset": "kedro_datasets.pandas.CSVDataset"
        },
    }

def input_nimbal_pushoff():
    """ Nimbal pushoff data.
    """
    return {
        "requires_input": False,
        "catalog": {
            "type": "kedro_datasets.pandas.CSVDataset",
            "filepath": "data/nimbal_pushoff.csv",
        },
    }

def _get_input_registry(pipeline_name: str):
    dict_inputs = {
        "input_axivity_dataset": input_axivity_dataset(),
        "input_sync_dataset": input_sync_dataset(),
        "input_nimbal_pushoff": input_nimbal_pushoff(),
    }

    list_inputs = get_pipeline_registry()[pipeline_name]["input"]
    input_registry = {}
    for input in list_inputs:
        input_registry[input] = dict_inputs[input]

    return input_registry

def _collect_inputs(input_registry, project_root):
    for ikey, imeta in input_registry.items():
        if imeta["requires_input"]:
            source_dir = imeta["catalog"]["path"]
            target_dir = os.path.join(project_root, "data")
            sub_dir = imeta["modality"]
            filepattern = imeta["filepattern"]
    
            _collect(source_dir, target_dir, sub_dir, filepattern)
            # update path in catalog
            input_registry[ikey]["catalog"]["path"] = os.path.join(target_dir, "raw", sub_dir)

    clear_output(wait=False)
    print(f"Data copy {_format_text('successful', bold=True, color='green')}.")

    return input_registry


def register_inputs(pipeline_name: str, project_root: str):
    input_registry = _get_input_registry(pipeline_name)
    
    is_complete = True
    for ikey, imeta in input_registry.items():
        if imeta["requires_input"]:
            print(f"\nInput the data {_format_text(imeta['pathtype'], bold=True)} for {_format_text(ikey, bold=True, color='blue')} below:")
            path_val = input("")
            path_val = os.path.expanduser(path_val)
    
            # check if input is valid and matches path type
            is_file = os.path.isfile(path_val)
            is_valid = os.path.exists(path_val)
    
            if is_valid: # file or folder exists
                if is_file: # path is file
                    if imeta["pathtype"] != "file":
                        is_complete = False
                        print(f"A {_format_text('file', bold=True)} is required.")
                        break
                else: # path is directory
                    if imeta["pathtype"] != "directory":
                        is_complete = False
                        print(f"A {_format_text('directory', bold=True)} is required.")
                        break
            else:
                is_complete = False
                print(f"Valid {_format_text(imeta['pathtype'], bold=True)} is required.")
                break
    
            # update catalog with path if valid
            if is_complete:
                if imeta["pathtype"] == "file":
                    input_registry[ikey]["catalog"]["filepath"] = path_val
                elif imeta["pathtype"] == "directory":
                    input_registry[ikey]["catalog"]["path"] = path_val
    
    if is_complete:
        input_registry = _collect_inputs(input_registry, project_root)
        print(f"\nInput catalog registration {_format_text('successful', bold=True, color='green')}.")
    else:
        print(f"\nInput catalog registration {_format_text('incomplete', bold=True, color='red')}. Please re-run registration.\n")

    return input_registry
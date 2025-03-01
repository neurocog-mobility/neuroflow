from neuroflow.pipeline_registry import _get_pipeline_registry
from neuroflow.utils.utils import _format_text
from neuroflow.utils.collect import _collect
from neuroflow.utils.folder_select import SelectFolderButton
from IPython.display import clear_output, display
import os
import ipywidgets as widgets

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
            "dataset": "neuroflow.datasets.axivity_dataset.AxivityDataset",
            "metadata": { "kedro-viz": {"layer": "input"} }
        },
    }

def input_sync_dataset():
    """ Sync dataset.
    """
    return {
        "requires_input": True,
        "pathtype": "directory",
        "modality": "sync",
        "filepattern": "*sync*.csv",
        "catalog": {
            "type": "partitions.IncrementalDataset",
            "path": "",
            "dataset": "kedro_datasets.pandas.CSVDataset",
            "metadata": { "kedro-viz": {"layer": "input"} }
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
            "metadata": { "kedro-viz": {"layer": "detect-steps"} }
        },
    }

def _get_input_registry(pipeline_name: str = None):
    dict_inputs = {
        "input_axivity_dataset": input_axivity_dataset(),
        "input_sync_dataset": input_sync_dataset(),
        "input_nimbal_pushoff": input_nimbal_pushoff(),
    }

    if pipeline_name:
        list_keys = _get_pipeline_registry()[pipeline_name]["input"]
        input_registry = {}
        for key in list_keys:
            input_registry[key] = dict_inputs[key]
    else:
        input_registry = dict_inputs

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

def _display_input_registry_header(input_registry, i):
    print(_format_text("\nGenerating input registry", bold=True, underline=True))
    print(_format_text("Setting inputs for: ", bold=True))
    for j, (jkey, jmeta) in enumerate(input_registry.items()):
        if jmeta["requires_input"]:
            if j < i:
                print(_format_text(f"\t{j+1}: {jkey}", bold=True, color='green'))
            elif j == i:
                print(_format_text(f"\t{j+1}: {jkey}", bold=True, underline=True, color='blue'))
            else:
                print(_format_text(f"\t{j+1}: {jkey}", bold=False, color='blue'))
    print("____________________________")

            
def _register_inputs(pipeline_name: str, project_root: str):
    input_registry = _get_input_registry(pipeline_name)
    
    is_complete = True
    for i, (ikey, imeta) in enumerate(input_registry.items()):
        clear_output(wait=False)
        _display_input_registry_header(input_registry, i)
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

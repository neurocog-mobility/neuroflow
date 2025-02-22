from typing import Dict, Any
import os
from pathlib import Path
from IPython.display import clear_output
from neuroflow.utils.utils import _format_text
from neuroflow.pipeline_registry import get_pipeline_registry
from neuroflow.definitions import define_filepattern

def params_axivity_filepattern():
    """ Axivity dataset filepattern.
    """
    return {
        "requires_input": True,
        "type": "filepattern",
        "catalog": {
            "dataset": "input_axivity_dataset",
            "pattern": ""
        },
    }

def params_sync_filepattern():
    """ Sync dataset filepattern.
    """
    return {
        "requires_input": True,
        "type": "filepattern",
        "catalog": {
            "dataset": "input_sync_dataset",
            "pattern": ""
        },
    }

def params_step_parameters():
    """ Nimbal detector step parameters.
    """
    return {
        "requires_input": True,
        "type": "dict",
        "catalog": {
            "pushoff_threshold": 0.75, "pushoff_time": 0.4, "swing_phase_time": 0.2,
            "heel_strike_detect_time": 0.5, "heel_strike_threshold": -5, "foot_down_time": 0.05
        },
    }

def params_plot_imu():
    """ Columns for IMU plotting.
    """
    return {
        "requires_input": False,
        "type": "list",
        "catalog": {
            "columns": ["accel_x", "accel_y", "accel_z"]
        },
    }


def _get_param_registry(pipeline_name: str):
    dict_inputs = {
        "axivity_filepattern": params_axivity_filepattern(),
        "sync_filepattern": params_sync_filepattern(),
        "step_parameters": params_step_parameters(),
        "plot_imu": params_plot_imu(),
    }

    list_inputs = get_pipeline_registry()[pipeline_name]["params"]
    param_registry = {}
    for input in list_inputs:
        param_registry[input] = dict_inputs[input]

    return param_registry


def _get_integer_input(prompt, list_fields):
    while True:
        try:
            user_input = input(prompt)
            integer_value = int(user_input)

            try:
                fieldval = list_fields[integer_value]
                return fieldval
            except:
                print(f"Input not in range [0-{len(list_fields)}]")
        except ValueError:
            print("Invalid input. Please enter an integer.")


def generate_filepattern(dataset: str, input_registry: Dict[str, Any]):
    filepattern_fields = {"misc": "[misc]", **define_filepattern()}
    sample_file_raw = os.listdir(input_registry[dataset]["catalog"]["path"])[0]
    sample_file = Path(sample_file_raw).stem
    
    field_string = ""
    for f, field in enumerate(filepattern_fields.keys()):
        field_string += f"{f}: {field} \t"
    
    sample_parts = sample_file.split("_")
    pattern = sample_file
    
    # create prompt
    list_prompt = []
    for f, field in enumerate(sample_parts):
        list_prompt.append(field)
    
    for p, part in enumerate(sample_parts):
        print(f"\nGenerating file pattern for {_format_text(dataset, bold=True, color='blue', underline=True)}\n")
        print("File pattern key:")
        print(field_string)
        print("")

        prompt = list_prompt.copy()
        for f, field in enumerate(list_prompt):
            if f < p:
                prompt[f] = f"{_format_text(field, bold=True, color='green')}"
            elif f == p:
                prompt[f] = f"{_format_text(field, bold=True, underline=True, color='blue')}"
        prompt = "_".join(prompt)
        
        print(prompt)
        input_prompt = f"--> Label the highighted field [0-{len(filepattern_fields.keys())}]?"
        key_val = _get_integer_input(input_prompt, list(filepattern_fields.keys()))
        print("")
        clear_output(wait=False)
        
        list_prompt[p] = f"[{key_val}]"

    generated_filepattern = "_".join(list_prompt) + os.path.splitext(sample_file_raw)[1]

    return generated_filepattern


def _validate_dict(dict_name, dict_params):
    print(f"\nDefault values for {_format_text(dict_name, bold=True, color='blue')}:")
    for pkey, pval in dict_params.items():
        print(f"{_format_text(pkey, bold=True)}: {pval}", end=", ")
    print("\n")
    accept_vals = input("Accept default values? (y/n) [y]: ") or "y"
    
    if accept_vals == "n":
        clear_output(wait=False)
        
        for pkey, pval in dict_params.items():
            print(f"\nValues for {_format_text(dict_name, bold=True, color='blue')}:")
            for key, val in dict_params.items():
                print(f"{_format_text(key, bold=True)}: {val}", end=", ")
            print("\n")
            
            print(f"{_format_text(pkey, bold=True)}: {pval}")
            new_val = input(f"--> New value: ")
            dict_params[pkey] = float(new_val)
            
            clear_output(wait=False)
    clear_output(wait=False)
    
    return dict_params


def register_params(pipeline_name: str, input_registry):
    param_registry = _get_param_registry(pipeline_name)
    
    for ikey, imeta in param_registry.items():
        if imeta["requires_input"]:
            if imeta["type"] == "filepattern":
                imeta["catalog"]["pattern"] = generate_filepattern(imeta["catalog"]["dataset"], input_registry)
            elif imeta["type"] == "dict":
                imeta["catalog"] = _validate_dict(ikey, imeta["catalog"])
            elif imeta["type"] == "list":
                print("Need list")

    print(f"\nParameter registration {_format_text('successful', bold=True, color='green')}.")

    return param_registry
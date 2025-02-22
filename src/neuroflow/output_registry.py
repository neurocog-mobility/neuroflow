import os
from neuroflow.pipeline_registry import get_pipeline_registry
from neuroflow.utils.utils import _format_text

def output_axivity_rawdata():
    """ Raw axivity dataset.
    """
    return {
        "type": "path",
        "catalog": {
            "type": "partitions.IncrementalDataset",
            "path": "",
            "dataset": "pandas.CSVDataset",
            "filename_suffix": ".csv",
        },
    }

def output_axivity_rawplots():
    """ Raw axivity plots.
    """
    return {
        "type": "path",
        "catalog": {
            "type": "matplotlib.MatplotlibWriter",
            "filepath": "",
            "save_args": { "format": "png" }
        },
    }

def output_axivity_stepdata():
    """ Step axivity dataset.
    """
    return {
        "type": "path",
        "catalog": {
            "type": "partitions.IncrementalDataset",
            "path": "",
            "dataset": "pandas.CSVDataset",
            "filename_suffix": ".csv",
        },
    }

def output_axivity_stepplots():
    """ Step axivity plots.
    """
    return {
        "type": "path",
        "catalog": {
            "type": "matplotlib.MatplotlibWriter",
            "filepath": "",
            "save_args": { "format": "png" }
        },
    }

def output_axivity_stepsummary():
    """ Step axivity summaries.
    """
    return {
        "type": "file",
        "filename": "axivity_step_summary.csv",
        "catalog": {
            "type": "kedro_datasets.pandas.CSVDataset",
            "filepath": "",
        },
    }

def _get_output_registry(pipeline_name: str):
    dict_inputs = {
        "output_axivity_rawdata": output_axivity_rawdata(),
        "output_axivity_rawplots": output_axivity_rawplots(),
        "output_axivity_stepdata": output_axivity_stepdata(),
        "output_axivity_stepplots": output_axivity_stepplots(),
        "output_axivity_stepsummary": output_axivity_stepsummary(),
    }

    list_inputs = get_pipeline_registry()[pipeline_name]["output"]
    output_registry = {}
    for input in list_inputs:
        output_registry[input] = dict_inputs[input]

    return output_registry


def register_outputs(pipeline_name: str, project_root: str):
    output_registry = _get_output_registry(pipeline_name)

    for okey, ometa in output_registry.items():
        output_path = os.path.join(project_root, "data", "processed", okey)

        if ometa["type"] == "path":
            # set filepath or path key in catalog
            if "filepath" in ometa["catalog"].keys():
                output_registry[okey]["catalog"]["filepath"] = output_path
            elif "path" in ometa["catalog"].keys():
                output_registry[okey]["catalog"]["path"] = output_path
        elif ometa["type"] == "file":
            output_filepath = os.path.join(output_path, ometa["filename"])
            output_registry[okey]["catalog"]["filepath"] = output_filepath

    print(f"\nOutput catalog registration {_format_text('successful', bold=True, color='green')}.")

    return output_registry
from neuroflow.pipeline_registry import _get_pipeline_registry
import os

def _inter_axivity_data_trials():
    """ Nimbal pushoff data.
    """
    return {
        "catalog": {
            "type": "MemoryDataset",
            "metadata": { "kedro-viz": {"layer": "process-raw"} }
        },
    }

def _inter_bittium_data_trials():
    """ Nimbal pushoff data.
    """
    return {
        "catalog": {
            "type": "MemoryDataset",
            "metadata": { "kedro-viz": {"layer": "process-raw"} }
        },
    }

def _inter_bittium_processed_trials():
    """ Nimbal pushoff data.
    """
    return {
        "catalog": {
            "type": "MemoryDataset",
            "metadata": { "kedro-viz": {"layer": "process-rr"} }
        },
    }

def _inter_step_state_data():
    """ Nimbal pushoff data.
    """
    return {
        "catalog": {
            "type": "MemoryDataset",
            "metadata": { "kedro-viz": {"layer": "detect-steps"} }
        },
    }

def _inter_table_step_times():
    """ Nimbal pushoff data.
    """
    return {
        "catalog": {
            "type": "MemoryDataset",
            "metadata": { "kedro-viz": {"layer": "detect-steps"} }
        },
    }

def _inter_axivity_data_steps():
    """ Nimbal pushoff data.
    """
    return {
        "catalog": {
            "type": "MemoryDataset",
            "metadata": { "kedro-viz": {"layer": "process-steps"} }
        },
    }

def _inter_table_step_summaries():
    """ Nimbal pushoff data.
    """
    return {
        "catalog": {
            "type": "MemoryDataset",
            "metadata": { "kedro-viz": {"layer": "process-steps"} }
        },
    }

def _inter_table_rr_peaks():
    """ Nimbal pushoff data.
    """
    return {
        "catalog": {
            "type": "MemoryDataset",
            "metadata": { "kedro-viz": {"layer": "process-rr"} }
        },
    }

def _get_inter_registry(pipeline_name: str = None):
    dict_inputs = {
        "axivity_data_trials": _inter_axivity_data_trials(),
        "bittium_data_trials": _inter_bittium_data_trials(),
        "bittium_processed_trials": _inter_bittium_processed_trials(),
        "step_state_data": _inter_step_state_data(),
        "table_step_times": _inter_table_step_times(),
        "axivity_data_steps": _inter_axivity_data_steps(),
        "table_step_summaries": _inter_table_step_summaries(),
        "table_rr_peaks": _inter_table_rr_peaks(),
    }

    if pipeline_name:
        list_keys = _get_pipeline_registry()[pipeline_name]["intermed"]
        inter_registry = {}
        for key in list_keys:
            inter_registry[key] = dict_inputs[key]
    else:
        inter_registry = dict_inputs

    return inter_registry


def _register_intermed(pipeline_name: str):
    inter_registry = _get_inter_registry(pipeline_name)

    return inter_registry

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline
import neuroflow.pipes.ppl_default as ppl
import neuroflow.pipes.imu.ppl_imu as ppl_imu
from neuroflow.utils.utils import _format_text


def register_pipelines() -> dict[str, Pipeline]:
    """
    
    :meta private:

    Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipeline_registry = _get_pipeline_registry()
    pipeline_functions = {key: pipe["pipeline"] for key, pipe in pipeline_registry.items()}

    return {
        "__default__": ppl.ppl_default(), **pipeline_functions
    }


def _get_pipeline_registry():
    dict_pipelines = {
        "process_raw_axivity": {
            "description": "Exports raw data from Axivity IMU data.",
            "pipeline": ppl_imu.ppl_export_raw_axivity(),
            "input": ["input_axivity_dataset", "input_sync_dataset"],
            "params": ["axivity_filepattern", "sync_filepattern", "plot_imu"],
            "output": ["output_axivity_rawdata", "output_axivity_rawplots"],
            "intermed": ["axivity_data_trials"]
        },
        "process_step_data": {
            "description": "Exports raw step data from Axivity IMU data.",
            "pipeline": ppl_imu.ppl_detect_steps_axivity() +\
            ppl_imu.ppl_process_steps_axivity(),
            "input": ["input_axivity_dataset", "input_sync_dataset", "input_nimbal_pushoff"],
            "params": ["axivity_filepattern", "sync_filepattern", "step_parameters", "plot_imu"],
            "output": ["output_axivity_stepdata", "output_axivity_stepplots"],
            "intermed": ["axivity_data_trials",
                         "step_state_data", "table_step_times", "axivity_data_steps"]
        },
        "summarize_step_data": {
            "description": "Creates a step summary from Axivity IMU data.",
            "pipeline": ppl_imu.ppl_detect_steps_axivity() +\
            ppl_imu.ppl_summarize_steps_axivity(),
            "input": ["input_axivity_dataset", "input_sync_dataset", "input_nimbal_pushoff"],
            "params": ["axivity_filepattern", "sync_filepattern", "step_parameters"],
            "output": ["output_axivity_stepsummary"],
            "intermed": ["axivity_data_trials",
                         "step_state_data", "table_step_times", "axivity_data_steps",
                         "table_step_summaries"]
        },
        "project_naps": {
            "description": "NAPS project pipeline.\n\tProcesses Axivity IMU data, extracts steps, and creates a step summary.",
            "pipeline": ppl_imu.ppl_export_raw_axivity() + \
            ppl_imu.ppl_detect_steps_axivity() + \
            ppl_imu.ppl_process_steps_axivity() + \
            ppl_imu.ppl_summarize_steps_axivity(),
            "input": ["input_axivity_dataset", "input_sync_dataset", "input_nimbal_pushoff"],
            "params": ["axivity_filepattern", "sync_filepattern", "step_parameters", "plot_imu"],
            "output": ["output_axivity_rawdata", "output_axivity_rawplots",
                       "output_axivity_stepdata", "output_axivity_stepplots",
                       "output_axivity_stepsummary"],
            "intermed": ["axivity_data_trials",
                         "step_state_data", "table_step_times", "axivity_data_steps",
                         "table_step_summaries"]
        },
    }

    return dict_pipelines

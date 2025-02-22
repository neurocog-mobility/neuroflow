"""Project pipelines."""
from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline
import neuroflow.pipes.ppl_default as ppl
import neuroflow.pipes.imu.ppl_imu as ppl_imu


def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """

    return {
        "__default__": ppl.ppl_default(),
        "process_raw_axivity": ppl_imu.ppl_export_raw_axivity(),
        "process_step_data": ppl_imu.ppl_detect_steps_axivity() +\
            ppl_imu.ppl_process_steps_axivity(),
        "summarize_step_data": ppl_imu.ppl_detect_steps_axivity() +\
            ppl_imu.ppl_summarize_steps_axivity(),
        "project_naps": ppl_imu.ppl_export_raw_axivity() + \
            ppl_imu.ppl_detect_steps_axivity() + \
            ppl_imu.ppl_process_steps_axivity() + \
            ppl_imu.ppl_summarize_steps_axivity(),
    }


def get_pipeline_registry():
    dict_pipelines = {
        "process_raw_axivity": {
            "pipeline": ppl_imu.ppl_export_raw_axivity(),
            "input": ["input_axivity_dataset", "input_sync_dataset"],
            "params": ["axivity_filepattern", "sync_filepattern", "plot_imu"],
            "output": ["output_axivity_rawdata", "out_axivity_rawplots"]
        },
        "process_step_data": {
            "pipeline": ppl_imu.ppl_detect_steps_axivity() +\
            ppl_imu.ppl_process_steps_axivity(),
            "input": ["input_axivity_dataset", "input_sync_dataset", "input_nimbal_pushoff"],
            "params": ["axivity_filepattern", "sync_filepattern", "step_parameters", "plot_imu"],
            "output": ["output_axivity_stepdata", "output_axivity_stepplots"]
        },
        "summarize_step_data": {
            "pipeline": ppl_imu.ppl_detect_steps_axivity() +\
            ppl_imu.ppl_summarize_steps_axivity(),
            "input": ["input_axivity_dataset", "input_sync_dataset", "input_nimbal_pushoff"],
            "params": ["axivity_filepattern", "sync_filepattern", "step_parameters"],
            "output": ["output_axivity_stepsummary"]
        },
        "project_naps": {
            "pipeline": ppl_imu.ppl_export_raw_axivity() + \
            ppl_imu.ppl_detect_steps_axivity() + \
            ppl_imu.ppl_process_steps_axivity() + \
            ppl_imu.ppl_summarize_steps_axivity(),
            "input": ["input_axivity_dataset", "input_sync_dataset", "input_nimbal_pushoff"],
            "params": ["axivity_filepattern", "sync_filepattern", "step_parameters", "plot_imu"],
            "output": ["output_axivity_rawdata", "output_axivity_rawplots",
                       "output_axivity_stepdata", "output_axivity_stepplots",
                       "output_axivity_stepsummary"]
        },
    }

    return dict_pipelines


def display_pipelines():
    pipeline_registry = get_pipeline_registry()
    
    print("Registered pipelines:\n")
    for pipename, pipeline in pipeline_registry.items():
        print(pipename)
        print("\tInputs: ", pipeline["input"])
        print("\tParameters: ", pipeline["params"])
        print("\tOutputs: ", pipeline["output"])
        print("")

from kedro.pipeline import Pipeline, node, pipeline
from neuroflow.nodes.template_node import node_template
from neuroflow.nodes.utils.axivity import parse_axivity
from neuroflow.nodes.utils.export import plot_partitions, export_partitions, plot_partitions_swing
from neuroflow.nodes.imu.step_detection import detect_steps_nimbal
from neuroflow.nodes.imu.arm_swing import compute_arm_swing, extract_swing_features
from neuroflow.nodes.imu.gait_analysis import (
    extract_steps, split_axivity_into_steps,
    summarize_steps, compile_step_summary, create_step_profiles)


def ppl_export_raw_axivity(**kwargs) -> Pipeline:
    """ Plot and export raw axivity data.
    """
    return pipeline(
        [
            node(
                func=parse_axivity,
                inputs=["input_axivity_dataset",
                        "input_sync_dataset",
                        "params:axivity_filepattern",
                        "params:sync_filepattern"
                        ],
                outputs="axivity_data_trials",
                name="parse_axivity",
            ),
            node(
                func=plot_partitions,
                inputs=["axivity_data_trials",
                        "params:plot_imu"],
                outputs="output_axivity_rawplots",
                name="plot_raw_data",
            ),
            node(
                func=export_partitions,
                inputs="axivity_data_trials",
                outputs="output_axivity_rawdata",
                name="export_raw_data",
            ),
        ],
    )


def ppl_detect_steps_axivity(**kwargs) -> Pipeline:
    """ Use ankle axivity IMUs to detect steps.
    """
    return pipeline(
        [
            node(
                func=parse_axivity,
                inputs=["input_axivity_dataset",
                        "input_sync_dataset",
                        "params:axivity_filepattern",
                        "params:sync_filepattern"
                        ],
                outputs="axivity_data_trials",
                name="parse_axivity",
            ),
            node(
                func=detect_steps_nimbal,
                inputs=["axivity_data_trials",
                        "input_nimbal_pushoff",
                        "params:step_parameters"
                        ],
                outputs="step_state_data",
                name="nimbal_step_state_detection",
            ),
            node(
                func=extract_steps,
                inputs="step_state_data",
                outputs="table_step_times",
                name="extract_step_times",
            ),
            node(
                func=split_axivity_into_steps,
                inputs=["step_state_data", "table_step_times"],
                outputs="axivity_data_steps",
                name="split_into_steps",
            ),
        ],
    )


def ppl_process_steps_axivity(**kwargs) -> Pipeline:
    """ Split raw axivity IMU data into individual steps.
    """
    return pipeline(
        [
            node(
                func=plot_partitions,
                inputs=["axivity_data_steps",
                        "params:plot_imu"],
                outputs="output_axivity_stepplots",
                name="plot_step_data",
            ),
            node(
                func=export_partitions,
                inputs="axivity_data_steps",
                outputs="output_axivity_stepdata",
                name="export_step_data",
            ),
            node(
                func=create_step_profiles,
                inputs=["table_step_times",
                        "axivity_data_steps"],
                outputs="output_axivity_stepprofiles",
                name="create_step_profiles",
            ),
        ],
    )


def ppl_summarize_steps_axivity(**kwargs) -> Pipeline:
    """ Create step summary tables.
    """
    return pipeline(
        [
            node(
                func=summarize_steps,
                inputs=["table_step_times",
                        "axivity_data_steps"],
                outputs="table_step_summaries",
                name="summarize_step_data",
            ),
            node(
                func=compile_step_summary,
                inputs="table_step_summaries",
                outputs="output_axivity_stepsummary",
                name="compile_step_info",
            ),
        ],
    )


def ppl_process_armswing(**kwargs) -> Pipeline:
    """ Compute armswing from wrist IMUs.
    """
    return pipeline(
        [
            node(
                func=parse_axivity,
                inputs=["input_axivity_dataset",
                        "input_sync_dataset",
                        "params:axivity_filepattern",
                        "params:sync_filepattern"
                        ],
                outputs="axivity_data_trials",
                name="parse_axivity",
            ),
            node(
                func=compute_arm_swing,
                inputs="axivity_data_trials",
                outputs="axivity_data_swing",
                name="compute_swing_data",
            ),
            node(
                func=extract_swing_features,
                inputs="axivity_data_swing",
                outputs="table_swing_summaries",
                name="compile_swing_info",
            ),
            node(
                func=export_partitions,
                inputs="axivity_data_swing",
                outputs="output_axivity_rawdata",
                name="export_raw_data",
            ),
            node(
                func=export_partitions,
                inputs="table_swing_summaries",
                outputs="output_swing_data",
                name="export_swing_data",
            ),
            node(
                func=plot_partitions_swing,
                inputs=["axivity_data_swing"],
                outputs="output_axivity_rawplots",
                name="plot_swing_data",
            ),
        ],
    )
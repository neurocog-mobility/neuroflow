from kedro.pipeline import Pipeline, node, pipeline
from neuroflow.nodes.template_node import node_template
from neuroflow.nodes.utils.bittium import parse_bittium
from neuroflow.nodes.utils.export import (
    plot_partitions,
    export_partitions,
    plot_partitions_rr,
)
from neuroflow.nodes.ecg.detect_rr import filter_ecg, detect_rr_peaks


def ppl_export_raw_bittium(**kwargs) -> Pipeline:
    """Plot and export raw Bittium data."""
    return pipeline(
        [
            node(
                func=parse_bittium,
                inputs=[
                    "input_bittium_dataset",
                    "input_sync_dataset",
                    "params:bittium_filepattern",
                    "params:sync_filepattern",
                ],
                outputs="bittium_data_trials",
                name="parse_bittium",
            ),
            node(
                func=plot_partitions,
                inputs=["bittium_data_trials", "params:plot_ecg"],
                outputs="output_bittium_rawplots",
                name="plot_raw_data",
            ),
            node(
                func=export_partitions,
                inputs="bittium_data_trials",
                outputs="output_bittium_rawdata",
                name="export_raw_data",
            ),
        ],
    )


def ppl_detect_rr(**kwargs) -> Pipeline:
    """Use ECG to detect RR peaks."""
    return pipeline(
        [
            node(
                func=parse_bittium,
                inputs=[
                    "input_bittium_dataset",
                    "input_sync_dataset",
                    "params:bittium_filepattern",
                    "params:sync_filepattern",
                ],
                outputs="bittium_data_trials",
                name="parse_bittium",
            ),
            node(
                func=filter_ecg,
                inputs=[
                    "bittium_data_trials",
                ],
                outputs="bittium_processed_trials",
                name="filter_ecg",
            ),
            node(
                func=detect_rr_peaks,
                inputs="bittium_processed_trials",
                outputs="table_rr_peaks",
                name="detect_rr_peaks",
            ),
            node(
                func=export_partitions,
                inputs="table_rr_peaks",
                outputs="output_rr_data",
                name="export_rr_data",
            ),
            node(
                func=plot_partitions_rr,
                inputs=["bittium_processed_trials", "table_rr_peaks"],
                outputs="output_rr_plots",
                name="export_rr_plots",
            ),
        ],
    )

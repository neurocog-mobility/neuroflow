from kedro.pipeline import Pipeline, node, pipeline
from neuroflow.nodes.template_node import node_template


def ppl_preprocess_ecg(**kwargs) -> Pipeline:
    """ Load and preprocess ECG data
    """
    return pipeline(
        [
            node(
                func=node_template,
                inputs="bittium_dataset",
                outputs="preproc_bittium",
                name="select_ecg_channel",
            ),
            node(
                func=node_template,
                inputs="preproc_bittium",
                outputs="filtered_bittium",
                name="filter_ecg",
            ),
        ]
    )


def ppl_compute_hrv(**kwargs) -> Pipeline:
    """ Load and preprocess ECG data
    """
    return pipeline(
        [
            node(
                func=node_template,
                inputs="filtered_bittium",
                outputs="rr_intervals",
                name="pan_tompkin_detector",
            ),
            node(
                func=node_template,
                inputs=["rr_intervals", "params:hrv_params"],
                outputs="hrv_values",
                name="compute_hrv",
            ),
        ]
    )


def ppl_plot_rr_segments(**kwargs) -> Pipeline:
    """ Load and preprocess ECG data
    """
    return pipeline(
        [
            node(
                func=node_template,
                inputs="filtered_bittium",
                outputs="rr_intervals",
                name="pan_tompkin_detector",
            ),
            node(
                func=node_template,
                inputs="rr_intervals",
                outputs="plots_rr",
                name="plot_rr_intervals",
            ),
        ]
    )


def ppl_compute_hrv_frequency(**kwargs) -> Pipeline:
    """ Load and preprocess ECG data
    """
    return pipeline(
        [
            node(
                func=node_template,
                inputs=["rr_intervals", "params:hrv_params"],
                outputs="hrv_values",
                name="compute_hrv",
            ),
            node(
                func=node_template,
                inputs="hrv_values",
                outputs="concat_hrv_values",
                name="concatenate_hrv_series",
            ),
            node(
                func=node_template,
                inputs="concat_hrv_values",
                outputs="hrv_frequency_spectrum",
                name="fft_hrv_series",
            ),
        ]
    )

from kedro.pipeline import Pipeline, node, pipeline

from neuroflow.pipelines.nodes.calc.calc_composite_metrics import calc_accel_magnitude
from neuroflow.pipelines.nodes.plot.plot_timeseries import plot_partitions


def ppl_default(**kwargs) -> Pipeline:
    """
    default pipeline
    """
    return pipeline(
        [
            node(
                func=calc_accel_magnitude,
                inputs="axivity_dataset",
                outputs="preproc_axivity",
                name="calculate accel mag",
            ),
            node(
                func=plot_partitions,
                inputs="preproc_axivity",
                outputs="output_plot",
                name="plot_data",
                confirms="axivity_dataset"
            ),
        ]
    )

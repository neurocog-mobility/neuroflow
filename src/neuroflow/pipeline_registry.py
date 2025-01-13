"""Project pipelines."""

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline
import neuroflow.pipelines.pipes.ppl_default as ppl
import neuroflow.pipelines.pipes.imu.ppl_imu as ppl_imu


def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipeline = ppl.create_pipeline()
    pipeline2 = ppl.create_pipeline2()

    return {
        "__default__": ppl.ppl_default(),
        "ppl_imu_plot_export": ppl_imu.ppl_plot_and_export_csv,
        "ppl_imu_export": ppl_imu.ppl_export_csv,
    }

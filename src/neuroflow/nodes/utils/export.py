from typing import Any, Callable, Dict, List
import matplotlib.pyplot as plt
from pathlib import Path


def plot_partitions(
    data_partitions: Dict[str, Callable[[], Any]],
    plot_params: Dict[str, Callable[[], Any]] = {},
) -> Dict:
    """Plots raw data for the sensor.

    Args:
        data_partitions: Raw data partitions
    Returns:
        dict_plots: Dictionary of plots.
    """
    plots_dict = {}
    for partition_key, partition_value in sorted(data_partitions.items()):
        partition_data = partition_value["data"]
        # print(partition_key)

        if not plot_params:
            data_columns = [
                col for col in partition_value["data"].columns if col != "time"
            ]
        else:
            data_columns = plot_params["columns"]

        fig, ax = plt.subplots()
        plots_dict[f"{Path(partition_key).stem}.png"] = fig
        partition_data[data_columns].plot(
            title=partition_key,
            subplots=True,
            figsize=(8, 8),
            legend={"reverse"},
            ax=ax,
        )

    plt.close("all")
    print("Data plotting complete.")
    return plots_dict


def export_partitions(data_partitions: Dict[str, Callable[[], Any]]) -> Dict:
    """Exports raw data for the sensor.

    Args:
        data_partitions: Raw data partitions
    Returns:
        data_dict: Dictionary of data for export.
    """
    data_dict = {}
    for partition_key, partition_value in sorted(data_partitions.items()):
        partition_data = partition_value["data"]
        # print(partition_key)

        data_dict[f"{Path(partition_key).stem}"] = partition_data

    print("Data export complete.")
    return data_dict


def plot_partitions_rr(
    data_partitions: Dict[str, Callable[[], Any]],
    data_partitions_rr: Dict[str, Callable[[], Any]],
) -> Dict:
    """Plots raw data for the sensor.

    Args:
        data_partitions: Raw data partitions
        data_partitions_rr: Detected RR peaks
    Returns:
        dict_plots: Dictionary of plots.
    """
    plots_dict = {}

    for partition_key, partition_value in sorted(data_partitions.items()):
        partition_data = partition_value["data"]
        partition_data_rr = data_partitions_rr[partition_key]["data"]

        fig, ax = plt.subplots()
        plots_dict[f"{Path(partition_key).stem}_rr.png"] = fig

        # plot ecg
        ax.plot(partition_data["time"], partition_data["voltage_filt"])
        # plot rr event lines
        ax_rr = ax.twinx()
        ax_rr.vlines(partition_data_rr["r_peaks"], 0, 1, color="r", lw=0.5)
        
        ax.set_title(partition_key)
        ax.set_xlabel("time (seconds)")

    plt.close("all")
    print("Data plotting complete.")
    return plots_dict


def plot_partitions_swing(
    data_partitions: Dict[str, Callable[[], Any]],
) -> Dict:
    """Plots raw data for the sensor.

    Args:
        data_partitions: Raw data partitions
    Returns:
        dict_plots: Dictionary of plots.
    """
    plots_dict = {}

    for partition_key, partition_value in sorted(data_partitions.items()):
        partition_data = partition_value["data"]

        fig, ax = plt.subplots()
        plots_dict[f"{Path(partition_key).stem}_swing.png"] = fig

        # plot ecg
        ax.plot(partition_data["time"], partition_data["arm_angle"])
        
        ax.set_title(partition_key)
        ax.set_xlabel("time (seconds)")
        ax.set_ylabel("arm angle (degrees)")

    plt.close("all")
    print("Data plotting complete.")
    return plots_dict

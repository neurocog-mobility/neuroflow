from typing import Any, Callable, Dict, List
import matplotlib.pyplot as plt
from pathlib import Path

def plot_partitions(data_partitions: Dict[str, Callable[[], Any]],
                    plot_params: Dict[str, Callable[[], Any]] = {}) -> Dict:
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
            data_columns = [col for col in partition_value["data"].columns if col != "time"]
        else:
            data_columns = plot_params["columns"]

        fig, ax = plt.subplots() 
        plots_dict[f"{Path(partition_key).stem}.png"] = fig
        partition_data[data_columns].plot(
            title=partition_key,
            subplots=True,
            figsize=(8,8),
            legend={'reverse'},
            ax=ax
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

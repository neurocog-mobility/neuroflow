from typing import Any, Callable, Dict
import matplotlib.pyplot as plt

def plot_partitions(partitioned_input: Dict[str, Callable[[], Any]]) -> Dict:
    """Plots IMU data for the sensor.

    Args:
        sensor: Raw data.
    Returns:
        Preprocessed data, with `accel_mag` computed from components.
    """
    plots_dict = {}
    for partition_key, partition_data in sorted(partitioned_input.items()):
        print(partition_key)
        plots_dict[f"{partition_key}.png"] = plt.figure()
        plt.plot(partition_data["time"], partition_data["accel_mag"])
    
    plt.close("all")

    return plots_dict
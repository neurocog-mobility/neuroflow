from typing import Any, Callable, Dict
import numpy as np

def calc_accel_magnitude(partitioned_input: Dict[str, Callable[[], Any]]) -> Dict:
    """Preprocesses the IMU data for the sensor.

    Args:
        sensor: Raw data.
    Returns:
        Preprocessed data, with `accel_mag` computed from components.
    """
    for partition_key, partition_data in sorted(partitioned_input.items()):
        x = partition_data["accel_x"].values
        y = partition_data["accel_y"].values
        z = partition_data["accel_z"].values

        partition_data["accel_mag"] = np.sqrt(x**2 + y**2 + z**2)
        

    return partitioned_input

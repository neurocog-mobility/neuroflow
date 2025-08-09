from typing import Dict, Callable, Any
import numpy as np
import pandas as pd
from paradigma.feature_extraction import (
    pca_transform_gyroscope,
    compute_angle,
    remove_moving_average_angle,
    extract_angle_extremes,
    compute_range_of_motion,
    compute_peak_angular_velocity,
)
from neuroflow.nodes.utils.parse import get_sample_rate


def compute_arm_swing(
    data_axivity: Dict[str, Callable[[], Any]],
) -> Dict[str, Callable[[], Any]]:
    """Transforms wrist IMU time-series into arm-swing angle (flex/ext).
    See <https://github.com/biomarkersParkinson/paradigma/> for more details.

    Args:
        data_axivity: Raw axivity files.
    Returns:
        data_processed: Arm swing angle + angular velocity array for each trial.
    """
    data_processed = {}
    for partition_key, partition_value in sorted(data_axivity.items())[:]:
        partition_data = partition_value["data"]

        if "wrist" in partition_value["metadata"]["sensor"]:
            # print(partition_key)

            vel = pca_transform_gyroscope(partition_data, "gyro_x", "gyro_z")
            fs = get_sample_rate(partition_data)
            dt = 1 / fs
            time_array = np.linspace(0, len(vel) / fs, len(vel))
            angle = compute_angle(time_array, vel)
            angle = remove_moving_average_angle(angle, fs)

            processed_data = partition_data.copy()
            processed_data["arm_velocity"] = vel
            processed_data["arm_angle"] = angle
            data_processed[partition_key] = {
                "metadata": partition_value["metadata"].copy(),
                "data": processed_data,
            }

    print("Arm swing computation complete.")
    return data_processed


def extract_swing_features(
    data_swing: Dict[str, Callable[[], Any]],
) -> Dict[str, Callable[[], Any]]:
    """Extracts arm swing ROM + peak swing velocity.
    See <https://github.com/biomarkersParkinson/paradigma/> for more details.

    Args:
        data_swing: Processed armswing data.
    Returns:
        data_processed: Arm swing angle + angular velocity array for each trial.
    """
    data_processed = {}
    for partition_key, partition_value in sorted(data_swing.items())[:]:
        partition_data = partition_value["data"]

        vel = partition_data["arm_velocity"].values
        angle = partition_data["arm_angle"].values
        fs = get_sample_rate(partition_data)

        idx_swing, _, _ = extract_angle_extremes(angle, fs)
        num_swing = list(range(1, len(idx_swing)))
        rom_swing = compute_range_of_motion(angle, idx_swing)
        pav_swing = compute_peak_angular_velocity(vel, idx_swing)

        data_processed[partition_key] = {
            "metadata": partition_value["metadata"].copy(),
            "data": pd.DataFrame(
                {
                    "swing_number": num_swing,
                    "swing_start": idx_swing[:-1],
                    "swing_end": idx_swing[1:],
                    "rom": rom_swing,
                    "peakvel": pav_swing,
                }
            ),
        }

    print("Arm swing feature extraction complete.")
    return data_processed

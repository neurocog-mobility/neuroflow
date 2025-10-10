# %%
from nimbalwear.gait_accel import detect_steps
from nimbalwear.gait import detect_vert
import pandas as pd
import matplotlib.pyplot as plt
from neuroflow.utils.signals import get_sampling_info, detect_wrist_axes
from importlib.resources import files
from pathlib import Path
import numpy as np
from paradigma.feature_extraction import (
    pca_transform_gyroscope,
    compute_angle,
    remove_moving_average_angle,
)


def gaitevents2csv(file_data, detector, detector_params={}, output_file=None):
    df = pd.read_csv(file_data)
    df["time"] = pd.to_datetime(df["time"])

    match detector:
        case "nimbalwear-ankles":
            df_events = steps_nimbalwear(df, nimbalwear_params=detector_params)
        case "paradigma-wrists":
            df_events = armswing_paradigma(df, paradigma_params=detector_params)

    if output_file is None:
        output_file = (
            Path(file_data).parent / f"{file_data.stem}_events_gait_{detector}.csv"
        )
    df_events.to_csv(output_file, index=False)

    return output_file


def steps_nimbalwear(df_data, nimbalwear_params={}):
    """
    Detect steps using nimbalwear algorithm: https://github.com/nimbal/nimbalwear/

    Args:
        df_data (pd.DataFrame): Standardized DataFrame of IMU data
        nimbalwear_params (dict): Key/value pairs of detector parameters;
            pushoff_threshold = 0.85,
            pushoff_time: float = 0.4,
            swing_phase_time: float = 0.2,
            heel_strike_detect_time: float = 0.5,
            heel_strike_threshold: int = -5,
            foot_down_time: float = 0.05

    Returns:
        pd.DataFrame of data with appended column named
        gait_nimbalwear_<left/right>ankle
        coding gait "state" array.
    """

    for side in ["right", "left"]:
        sensor_location = f"{side}ankle"
        if sum([sensor_location in col for col in df_data.columns]):
            a_vrt = detect_vert(
                df_data[
                    [f"{sensor_location}_a{axis}" for axis in ["x", "y", "z"]]
                ].values.T
            )

            # get nimbalwear pushoff_df.csv
            data_path = files("nimbalwear")
            pushoff_path = data_path.joinpath("data/pushoff_df.csv")
            df_pushoff = pd.read_csv(pushoff_path)
            # get sampling rate
            fs = get_sampling_info(df_data["time"])["frequency"]
            # check if vertical needs to be flipped to positive
            if np.mean(a_vrt) < 0:
                a_vrt *= -1
            # run nimbalwear step detector
            state_arr, _, _, _ = detect_steps(
                a_vrt, fs, df_pushoff, **nimbalwear_params
            )

            # append event array to sensor dataframe
            df_data[f"gait_nimbalwear_{sensor_location}"] = state_arr

    return df_data


def armswing_paradigma(df_data, paradigma_params={}):
    """
    Detect armswing using the paradigma implementation: https://github.com/biomarkersParkinson/paradigma

    Args:
        df_data (pd.DataFrame): Standardized DataFrame of IMU data
        paradigma_params (dict): Key/value pairs of detector parameters;
            yz_columns = ["y", "z"],

    Returns:
        pd.DataFrame of data with appended column named
        gait_paradigma_<left/right>wrist
        coding arm swing angle (degrees).
    """

    for side in ["right", "left"]:
        sensor_location = f"{side}wrist"
        if sum([sensor_location in col for col in df_data.columns]):
            if not paradigma_params:
                a_arm = df_data[
                    [f"{sensor_location}_a{axis}" for axis in ["x", "y", "z"]]
                ].values
                g_arm = df_data[
                    [f"{sensor_location}_g{axis}" for axis in ["x", "y", "z"]]
                ].values
                wrist_columns = detect_wrist_axes(*a_arm.T)
                df_arm = pd.DataFrame(g_arm[:, wrist_columns], columns=["y", "z"])
            else:
                df_arm = df_data[
                    [
                        f"{sensor_location}_g{axis}"
                        for axis in paradigma_params["yz_columns"]
                    ]
                ]
                df_arm.columns = ["y", "z"]

            vel = pca_transform_gyroscope(df_arm, "y", "z")
            fs = get_sampling_info(df_data["time"])["frequency"]

            time_array = np.linspace(0, len(vel) / fs, len(vel))
            angle = compute_angle(time_array, vel)
            angle = remove_moving_average_angle(angle, fs)

            # append event array to sensor dataframe
            df_data[f"gait_paradigma_{sensor_location}"] = angle

    return df_data

import pandas as pd
from openmovement.load import CwaData
from pyedflib import highlevel
import numpy as np
from pathlib import Path
from functools import reduce
from neuroflow.io.read_sensor_location import autodetect_sensor_location


def convert2csv(file_list, output_file=None, device=None):
    """
    Convert raw file into standardized wide format CSV/DataFrame.
    """
    # Load raw
    print("... Reading and standardizing data")
    df = load_raw(file_list, device)

    print("... Writing DataFrame to .csv")
    # Save CSV
    if output_file is None:
        output_file = (
            Path(file_list[0]).parent
            / f"nf_standard_{device.lower().split(" (")[0]}.csv"
        )
    df.to_csv(output_file, index=False)

    return output_file


def load_raw(file_list, device=None):
    """
    Load raw device files and return a standardized DataFrame.

    Args:
        file_list (list of str/Path): paths to device files for a single collection
        device (str): "Axivity (IMU)", "Bittium (ECG)"

    Returns:
        pd.DataFrame: standardized data
    """

    dict_devices = {
        "Axivity (IMU)": {"loader": _axivity_cwa_files, "input": "multiple"},
        "Bittium (ECG)": {"loader": _bittium_edf, "input": "single"},
    }

    try:
        if dict_devices[device]["input"] == "single":
            df = dict_devices[device]["loader"](str(file_list[0]))
        elif dict_devices[device]["input"] == "multiple":
            df = dict_devices[device]["loader"](file_list)
    except Exception as e:
        print(e)
        raise ValueError(
            f"Unsupported device/modality {device}. Currently supported options are: {dict_devices.keys()}"
        )

    return df


def _axivity_cwa_files(file_list, sensor_names=None):
    """
    Load multiple Axivity .cwa files and return a wide DataFrame.

    Args:
        file_list (list of str/Path): paths to .cwa files
        sensor_names (list of str): optional names for each sensor; defaults to file stem

    Returns:
        pd.DataFrame: wide-format IMU data with columns:
                      time, <sensor>_ax, <sensor>_ay, <sensor>_az, <sensor>_gx, <sensor>_gy, <sensor>_gz
    """
    if not isinstance(file_list, list):
        file_list = [file_list]

    if sensor_names is None:
        sensor_names = [autodetect_sensor_location(Path(f).stem) for f in file_list]

    sensor_dfs = []

    for f, name in zip(file_list, sensor_names):
        with CwaData(
            f,
            include_gyro=True,
            include_temperature=True,
            include_accel=True,
            include_light=True,
        ) as cwa_data:
            df = cwa_data.get_samples()
            # format cwa times
            df["time"] = pd.to_datetime(df["time"])
            df = df[
                [
                    "time",
                    "accel_x",
                    "accel_y",
                    "accel_z",
                    "gyro_x",
                    "gyro_y",
                    "gyro_z",
                ]
            ]
            df.columns = [
                "time",
                f"{name}_ax",
                f"{name}_ay",
                f"{name}_az",
                f"{name}_gx",
                f"{name}_gy",
                f"{name}_gz",
            ]

            sensor_dfs.append(df)

    df_wide = reduce(
        lambda left, right: pd.merge_asof(
            left.sort_values("time"), right.sort_values("time"), on="time"
        ),
        sensor_dfs,
    )

    return df_wide


def _bittium_edf(file: str):
    """
    Load a Bittium .EDF file and return a DataFrame.

    Args:
        file (str): path to .EDF file

    Returns:
        pd.DataFrame: ECG data with columns:
                      time, ecg_<channel_number>, chest_ax, chest_ay, chest_az
    """
    signals, signal_headers, header = highlevel.read_edf(file)
    channel_ecg = [s["label"] for s in signal_headers if "ecg" in s["label"].lower()]
    signals_ecg = [
        signals[s]
        for s, head in enumerate(signal_headers)
        if "ecg" in head["label"].lower()
    ]
    fs_ecg = [
        s["sample_frequency"] for s in signal_headers if "ecg" in s["label"].lower()
    ][0]

    channel_imu = [
        s["label"] for s in signal_headers if "accelerometer" in s["label"].lower()
    ]
    signals_imu = [
        signals[s]
        for s, head in enumerate(signal_headers)
        if "accelerometer" in head["label"].lower()
    ]
    fs_imu = [
        s["sample_frequency"]
        for s in signal_headers
        if "accelerometer" in s["label"].lower()
    ][0]

    time_ecg = np.linspace(0, (len(signals_ecg[0]) - 1) / fs_ecg, len(signals_ecg[0]))
    time_imu = np.linspace(0, (len(signals_imu[0]) - 1) / fs_imu, len(signals_imu[0]))

    # create ecg + imu dfs
    df_ecg = pd.DataFrame(np.array(signals_ecg).T, columns=channel_ecg)
    df_imu = pd.DataFrame(np.array(signals_imu).T, columns=channel_imu)
    df_ecg.insert(0, "time", time_ecg)
    df_imu.insert(0, "time", time_imu)

    # merge on ecg df
    df = pd.merge(df_ecg, df_imu, on="time", how="left")

    # time correction
    df["time"] = pd.to_datetime(header["startdate"]) + pd.to_timedelta(
        df["time"], unit="s"
    )

    # standardize column names
    is_ecg_channel = [i for i in df.columns if "ecg" in i.lower()]
    column_names = (
        ["time"]
        + [f"ecg_{i}" for i in range(len(is_ecg_channel))]
        + ["chest_ax", "chest_ay", "chest_az"]
    )
    df.columns = column_names

    return df

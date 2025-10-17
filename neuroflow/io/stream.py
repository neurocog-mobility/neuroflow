import pandas as pd
import numpy as np
import pyedflib
import os
from pathlib import Path
from functools import reduce
from openmovement.load.cwa_load import SECTOR_SIZE
from neuroflow.utils.cwa import parse_cwa_data
from neuroflow.io.read_sensor_location import autodetect_sensor_location

def stream_bittium_window(
    edf_path: str, timestamp: np.datetime64, duration_seconds: int
):
    """
    Stream a Bittium .EDF file and return a DataFrame.

    Args:
        edf_path (str): path to .EDF file
        timestamp (np.datetime64): start time of streaming window
        duration_seconds (int): duration of streaming window

    Returns:
        pd.DataFrame: ECG data with columns:
                      time, ecg_<channel_number>, chest_ax, chest_ay, chest_az
    """
    with pyedflib.EdfReader(edf_path) as f:
        header = f.getHeader()
        signal_headers = f.getSignalLabels()
        sample_frequencies = f.getSampleFrequencies()

        channel_ecg = [s for s in signal_headers if "ecg" in s.lower()]
        channel_imu = [s for s in signal_headers if "accelerometer" in s.lower()]

        fs_ecg = [
            sample_frequencies[i]
            for i, lbl in enumerate(signal_headers)
            if "ecg" in lbl.lower()
        ][0]
        fs_imu = [
            sample_frequencies[i]
            for i, lbl in enumerate(signal_headers)
            if "accelerometer" in lbl.lower()
        ][0]

        # get samples
        start_sec = (timestamp - pd.to_datetime(header["startdate"])).total_seconds()

        # ecg
        start_sample_ecg = int(start_sec * fs_ecg)
        n_samples_ecg = int(duration_seconds * fs_ecg)
        signals_ecg = [
            f.readSignal(signal_headers.index(ch), start_sample_ecg, n_samples_ecg)
            for ch in channel_ecg
        ]

        # imu
        start_sample_imu = int(start_sec * fs_imu)
        n_samples_imu = int(duration_seconds * fs_imu)
        signals_imu = [
            f.readSignal(signal_headers.index(ch), start_sample_imu, n_samples_imu)
            for ch in channel_imu
        ]

    df_ecg = pd.DataFrame(np.array(signals_ecg).T, columns=channel_ecg)
    df_imu = pd.DataFrame(np.array(signals_imu).T, columns=channel_imu)

    # insert time
    time_ecg = np.linspace(0, (len(signals_ecg[0]) - 1) / fs_ecg, len(signals_ecg[0]))
    time_imu = np.linspace(0, (len(signals_imu[0]) - 1) / fs_imu, len(signals_imu[0]))
    df_ecg.insert(0, "time", time_ecg)
    df_imu.insert(0, "time", time_imu)

    # merge on ecg df
    df = pd.merge(df_ecg, df_imu, on="time", how="left")

    # time correction
    df["time"] = (
        pd.to_datetime(header["startdate"])
        + pd.DateOffset(seconds=start_sec)
        + pd.to_timedelta(df["time"], unit="s")
    )

    # standardize column names
    is_ecg_channel = [i for i in df.columns if "ecg" in i.lower()]
    column_names = (
        ["time"]
        + [f"ecg{i}" for i in range(len(is_ecg_channel))]
        + ["chest_ax", "chest_ay", "chest_az"]
    )
    df.columns = column_names

    return df


def stream_bittium_timestamps(
    edf_path: str, time_start: np.datetime64, time_end: np.datetime64
):
    """
    Stream a Bittium .EDF file and return a DataFrame.

    Args:
        edf_path (str): path to .EDF file
        time_start (np.datetime64): start time of streaming window
        time_end (np.datetime64): end time of streaming window

    Returns:
        pd.DataFrame: ECG data with columns:
                      time, ecg_<channel_number>, chest_ax, chest_ay, chest_az
    """
    window = (time_end - time_start) / np.timedelta64(1, "s")

    df = stream_bittium_window(edf_path, time_start, window)

    return df


def _blocks2dataframe(data_blocks):
    list_dataframes = []
    for data_block in data_blocks:
        data_acc = np.array(data_block[-1]["samplesAccel"])
        data_gyro = np.array(data_block[-1]["samplesGyro"])
        data_seconds = np.arange(0, data_acc.shape[0], 1) / data_block[-2]
        data_time = np.array(
            [data_block[0] + pd.DateOffset(seconds=sec) for sec in data_seconds]
        )

        data_arr = np.column_stack([data_time, data_acc, data_gyro])

        df_block = pd.DataFrame(
            data_arr,
            columns=[
                "time",
                "ax",
                "ay",
                "az",
                "gx",
                "gy",
                "gz",
            ],
        )

        list_dataframes.append(df_block)

    df_data = pd.concat(list_dataframes)
    df_data.reset_index(inplace=True, drop=True)

    return df_data


def _sensor_column_names(df_data, cwa_path, sensor=None):
    if sensor is None:
        sensor = autodetect_sensor_location(Path(cwa_path).stem)

    columns = [
        f"{sensor}_{cname}" if not cname == "time" else cname
        for cname in df_data.columns
    ]
    df_data.columns = columns

    return df_data


def stream_cwa_file(
    cwa_path: str, time_start: np.datetime64, time_end: np.datetime64, sensor=None
):
    """
    Stream an Axivity .CWA file and return a DataFrame.

    Args:
        cwa_path (str): path to .CWA file
        time_start (np.datetime64): start time of streaming window
        time_end (np.datetime64): end time of streaming window

    Returns:
        pd.DataFrame: IMU data with columns:
                      time, ax, ay, az, gx, gy, gz
    """
    with open(cwa_path, "rb") as f:
        # get file size to know when to stop
        file_size = os.fstat(f.fileno()).st_size
        current_position = SECTOR_SIZE

        list_datablocks = []
        # iterate through each data block
        while current_position < file_size:
            data_block = f.read(SECTOR_SIZE)
            current_position += SECTOR_SIZE

            # parse the data block to get its timestamp
            data = parse_cwa_data(data_block)

            # skip invalid blocks
            if not data or "timestamp" not in data:
                continue

            # convert the UNIX timestamp to a datetime object
            data_duration = data["sampleCount"] / data["frequency"]
            block_stop = np.datetime64(pd.to_datetime(data["timestampTime"]))
            block_start = np.datetime64(
                block_stop - pd.DateOffset(seconds=data_duration)
            )

            # check if the block is within the desired time range
            if block_stop < time_start:
                # still before the start time, continue to the next block
                continue
            elif block_start > time_end:
                # past the end time, stop streaming
                break
            else:
                data_samples = parse_cwa_data(data_block, extractData=True)
                # Yield the data for blocks within the range
                list_datablocks.append(
                    (
                        block_start,
                        block_stop,
                        data_duration,
                        data["frequency"],
                        data_samples,
                    )
                )

    # convert datablocks to DataFrame
    df_data = _blocks2dataframe(list_datablocks)

    return df_data


def stream_axivity_timestamps(file_list, time_start, time_stop, sensor_names=None):
    """
    Load multiple Axivity .cwa files and return a wide DataFrame.

    Args:
        file_list (list of str/Path): paths to .cwa files
        time_start (np.datetime64): start time of streaming window
        time_end (np.datetime64): end time of streaming window
        sensor_names (list of str): optional names for each sensor; defaults to file stem

    Returns:
        pd.DataFrame: wide-format IMU data with columns:
                      time, <sensor>_ax, <sensor>_ay, <sensor>_az, <sensor>_gx, <sensor>_gy, <sensor>_gz
    """
    if sensor_names is None:
        sensor_names = [autodetect_sensor_location(Path(f).stem) for f in file_list]

        sensor_dfs = []

        for f, name in zip(file_list, sensor_names):
            print(f"Streaming {name} ...")
            df_data = stream_cwa_file(f, time_start, time_stop)
            df_data = _sensor_column_names(df_data, f, sensor=name)

            sensor_dfs.append(df_data)

        df_wide = reduce(
            lambda left, right: pd.merge_asof(
                left.sort_values("time"), right.sort_values("time"), on="time"
            ),
            sensor_dfs,
        )

    return df_wide
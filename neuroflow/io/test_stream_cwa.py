#%%
import pandas as pd
import numpy as np


# %%
import os
import numpy as np
from openmovement.load.cwa_load import SECTOR_SIZE
from neuroflow.utils.cwa import parse_cwa_data
import pandas as pd
from neuroflow.utils.signals import convert_timestamps
from pathlib import Path
from neuroflow.io.read_sensor_location import autodetect_sensor_location
from functools import reduce


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
                "accel_x",
                "accel_y",
                "accel_z",
                "gyro_x",
                "gyro_y",
                "gyro_z",
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
            print(f"Streaming {f} ...")
            df_data = stream_cwa_file(f, time_start, time_stop)
            df_data = _sensor_column_names(df_data, cwa_path, sensor=name)

            sensor_dfs.append(df_data)

        df_wide = reduce(
            lambda left, right: pd.merge_asof(
                left.sort_values("time"), right.sort_values("time"), on="time"
            ),
            sensor_dfs,
        )

    return df_wide


df_times = pd.read_csv("../../test-data/fogcoa_meds/S002_FI_off_sync_time_form.csv")
df_times = convert_timestamps(df_times)

event = 1
event_start = df_times.loc[
    (df_times["trial"] == event) & (df_times["type"] == "start"), "time"
].values[0]
event_stop = df_times.loc[
    (df_times["trial"] == event) & (df_times["type"] == "stop"), "time"
].values[0]

cwa_path = "../../test-data/fogcoa_meds/C7_sub002_FR_7day.cwa"
file_list = ["../../test-data/fogcoa_meds/C7_sub002_FR_7day.cwa",
             "../../test-data/fogcoa_meds/l5_sub002_FR_7day.cwa"]

df_wide = stream_axivity_timestamps(file_list, event_start, event_stop)
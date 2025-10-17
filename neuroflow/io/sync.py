# %%
import pandas as pd
import numpy as np
from pathlib import Path
import os
from neuroflow.utils.signals import convert_timestamps
from neuroflow.io.stream import stream_bittium_timestamps, stream_axivity_timestamps


def split_csv(df_data, df_sync):
    """
    Split standardized data DataFrames using event sync timestamps.

    Args:
        df_data (pd.DataFrame): DataFrame of data to split
        df_sync (pd.DataFrame): DataFrame of timestamps for sync start/end events

    Returns:
        list[pd.DataFrame]: list of DataFrames, one for each sync event
    """
    df_data = convert_timestamps(df_data)
    df_sync = convert_timestamps(df_sync)

    list_trial_data = []
    for e, event in enumerate(df_sync["trial"].unique()):
        event_start = df_sync.loc[
            (df_sync["trial"] == event) & (df_sync["type"] == "start"), "time"
        ].values[0]
        event_stop = df_sync.loc[
            (df_sync["trial"] == event) & (df_sync["type"] == "stop"), "time"
        ].values[0]

        mask_data = np.logical_and(
            df_data["time"] >= event_start, df_data["time"] < event_stop
        )
        df_data_event = df_data.loc[mask_data].copy()
        df_data_event.attrs["label"] = event

        list_trial_data.append(df_data_event)

    return list_trial_data


def split_bittium(edf_path, df_sync):
    """
    Stream .EDF file and split using event sync timestamps.

    Args:
        edf_path (str): path to .EDF file
        df_sync (pd.DataFrame): DataFrame of timestamps for sync start/end events

    Returns:
        list[pd.DataFrame]: list of DataFrames, one for each sync event
    """

    df_sync = convert_timestamps(df_sync)

    list_trial_data = []
    for e, event in enumerate(df_sync["trial"].unique()):
        event_start = df_sync.loc[
            (df_sync["trial"] == event) & (df_sync["type"] == "start"), "time"
        ].values[0]
        event_stop = df_sync.loc[
            (df_sync["trial"] == event) & (df_sync["type"] == "stop"), "time"
        ].values[0]

        df_data_event = stream_bittium_timestamps(edf_path, event_start, event_stop)
        df_data_event.attrs["label"] = event
        list_trial_data.append(df_data_event)

    return list_trial_data


def split_axivity(file_list, df_sync, sensor_names=None):
    """
    Stream .CWA files and split using event sync timestamps.

    Args:
        file_list (list): list of paths to .CWA files
        df_sync (pd.DataFrame): DataFrame of timestamps for sync start/end events
        sensor_names (list of str): optional names for each sensor; defaults to file stem
    Returns:
        list[pd.DataFrame]: list of DataFrames, one for each sync event
    """
    if not isinstance(file_list, list):
        file_list = [file_list]

    df_sync = convert_timestamps(df_sync)

    list_trial_data = []
    for e, event in enumerate(df_sync["trial"].unique()):
        print("Processing event: ", e + 1)
        event_start = df_sync.loc[
            (df_sync["trial"] == event) & (df_sync["type"] == "start"), "time"
        ].values[0]
        event_stop = df_sync.loc[
            (df_sync["trial"] == event) & (df_sync["type"] == "stop"), "time"
        ].values[0]

        df_data_event = stream_axivity_timestamps(
            file_list, event_start, event_stop, sensor_names
        )
        df_data_event.attrs["label"] = event
        list_trial_data.append(df_data_event)

    return list_trial_data


def split2csv(file_list, file_sync, source="NeuroFlow (CSV)", output_dir=None):
    """
    Split standardized data DataFrames using event sync timestamps, and writes each file to .csv.

    Args:
        file_list (list): list of file paths of standardized data .csv (or raw)
        file_sync (Path): file path of sync timestamps .csv

    Returns:
        output_dir: Path to output directory
    """

    print(" ... Reading data and sync files")
    df_sync = pd.read_csv(file_sync)
    match source:
        case "NeuroFlow (CSV)":
            df_data = pd.read_csv(file_list[0])
            print(" ... Splitting data.")
            list_trial_data = split_csv(df_data, df_sync)
        case "Axivity (CWA)":
            print(" ... Streaming data.")
            list_trial_data = split_axivity(file_list, df_sync)
        case "Bittium (EDF)":
            print(" ... Streaming data.")
            list_trial_data = split_bittium(str(file_list[0]), df_sync)
        case _:
            return False

    print(" ... Writing split DataFrames to .csv")
    if output_dir is None:
        output_dir = file_list[0].parent / "events"
    os.makedirs(output_dir, exist_ok=True)

    for t, trial in enumerate(list_trial_data):
        output_file = (
            Path(output_dir) / f"{file_list[0].stem}_event-{trial.attrs["label"]}.csv"
        )
        trial.to_csv(output_file, index=False)

    return output_dir

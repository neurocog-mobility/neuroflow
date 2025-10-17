# %%
import numpy as np
import pandas as pd
from neuroflow.utils.signals import convert_timestamps
from neuroflow.io.stream import stream_bittium_window, stream_axivity_timestamps
import os
from pathlib import Path


def window_csv(df_data, df_times, duration_window, number_window):
    df_data = convert_timestamps(df_data)
    df_times = convert_timestamps(df_times)

    list_window_data = []

    for _, ref in df_times.iterrows():
        ref_label = ref["label"]
        ref_ts = ref["time"]
        for w in range(-number_window, number_window):
            win_start = ref_ts + pd.DateOffset(seconds=w * duration_window)
            win_end = ref_ts + pd.DateOffset(seconds=(w + 1) * duration_window)
            win_lbl = str(win_start).replace(" ", "T").replace(":", "").replace("-", "")
            print(w, ref_label + "_" + win_lbl)

            try:
                mask_data = np.logical_and(
                    df_data["time"] >= win_start, df_data["time"] < win_end
                )
                df_window = df_data.loc[mask_data].copy()

                df_window.attrs["label"] = (
                    ref_label
                    + "_"
                    + str(win_start).replace(" ", "T").replace(":", "").replace("-", "")
                )
                list_window_data.append(df_window)
            except Exception as e:
                print(e)

    return list_window_data


def window_axivity(
    file_list, df_times, duration_window, number_window, sensor_names=None
):
    """
    Stream .CWA files and window using timestamps.

    Args:
        file_list (list): list of paths to .CWA files
        df_times (pd.DataFrame): DataFrame of timestamps for window center
        duration_window (int): Seconds
        number_window (int): Number of pre/post windows
        sensor_names (list of str): optional names for each sensor; defaults to file stem
    Returns:
        list[pd.DataFrame]: list of DataFrames, one for each sync event
    """
    if not isinstance(file_list, list):
        file_list = [file_list]

    df_times = convert_timestamps(df_times)

    list_window_data = []
    for _, ref in df_times.iterrows():
        ref_label = ref["label"]
        ref_ts = ref["time"]
        for w in range(-number_window, number_window):
            win_start = ref_ts + pd.DateOffset(seconds=w * duration_window)
            win_end = win_start + pd.DateOffset(seconds=duration_window)
            win_lbl = str(win_start).replace(" ", "T").replace(":", "").replace("-", "")
            print(w, ref_label + "_" + win_lbl)

            try:
                df_window = stream_axivity_timestamps(
                    file_list, win_start, win_end, sensor_names
                )

                df_window.attrs["label"] = (
                    ref_label
                    + "_"
                    + str(win_start).replace(" ", "T").replace(":", "").replace("-", "")
                )
                list_window_data.append(df_window)
            except Exception as e:
                print(e)

    return list_window_data


def window_bittium(edf_path, df_times, duration_window, number_window):
    df_times = convert_timestamps(df_times)

    list_window_data = []

    for _, ref in df_times.iterrows():
        ref_label = ref["label"]
        ref_ts = ref["time"]
        for w in range(-number_window, number_window):
            win_start = ref_ts + pd.DateOffset(seconds=w * duration_window)
            win_lbl = str(win_start).replace(" ", "T").replace(":", "").replace("-", "")
            print(w, ref_label + "_" + win_lbl)

            try:
                df_window = stream_bittium_window(
                    edf_path, win_start.to_numpy(), duration_window
                )

                df_window.attrs["label"] = (
                    ref_label
                    + "_"
                    + str(win_start).replace(" ", "T").replace(":", "").replace("-", "")
                )
                list_window_data.append(df_window)
            except Exception as e:
                print(e)

    return list_window_data


def window2csv(
    file_list,
    file_times,
    duration_window,
    number_window,
    source="NeuroFlow (CSV)",
    output_dir=None,
):
    """
    Split standardized data DataFrames using event sync timestamps, and writes each file to .csv.

    Args:
        file_list (list): list of file paths of standardized data .csv (or raw)
        file_times (Path): file path of timestamps .csv

    Returns:
        output_dir: Path to output directory
    """

    print(" ... Reading data and sync files")
    df_times = pd.read_csv(file_times)
    match source:
        case "NeuroFlow (CSV)":
            df_data = pd.read_csv(file_list[0])
            print(" ... Windowing data.")
            list_trial_data = window_csv(
                df_data, df_times, duration_window, number_window
            )
        case "Axivity (CWA)":
            print(" ... Windowing data.")
            list_trial_data = window_axivity(
                file_list, df_times, duration_window, number_window
            )
        case "Bittium (EDF)":
            print(" ... Windowing data.")
            file_path = str(file_list[0])
            list_trial_data = window_bittium(
                file_path, df_times, duration_window, number_window
            )
        case _:
            return False

    print(" ... Writing split DataFrames to .csv")
    if output_dir is None:
        output_dir = file_list[0].parent / "windows"
    os.makedirs(output_dir, exist_ok=True)

    for t, trial in enumerate(list_trial_data):
        output_file = (
            Path(output_dir) / f"{file_list[0].stem}_window-{trial.attrs["label"]}.csv"
        )
        trial.to_csv(output_file, index=False)

    return output_dir

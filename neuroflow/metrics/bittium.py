import pandas as pd
import numpy as np


def _find_bittium_rr_columns(df):
    col_nw = [col for col in df.columns if "ecg_bittium" in col]

    return col_nw


def compute_rr_intervals(time, rpeaks):
    rpeaks_idx = np.where(rpeaks > 0)[0]
    rpeaks_time = time.values[rpeaks_idx]

    rr_intervals = np.diff(rpeaks_time) / np.timedelta64(1, "s")

    return rr_intervals


def compute_hrv(rr_intervals, method="rmssd"):
    match method:
        case "rmssd":
            # compute successive differences in RR intervals
            rr_sd = np.diff(rr_intervals)
            # compute RMS of successive differences
            hrv = np.sqrt(np.mean(rr_sd**2))
        case "sdnn":
            # compute stdev of rr intervals
            hrv = np.std(rr_intervals)
        case "pnn50":
            # compute successive differences in RR intervals
            rr_sd = np.diff(rr_intervals)
            # get number of successive differences > 50ms
            nn50 = np.sum(rr_sd > 0.05)
            # compute percentage
            hrv = 100 * (nn50 / len(rr_sd))

    return hrv


def summarize_hrv(df):
    list_hrv_summary = []

    for col in _find_bittium_rr_columns(df):
        rpeaks = df[col]
        rr_intervals = compute_rr_intervals(df["time"], rpeaks)

        hrv_info = {
            "label": df.attrs["label"],
            "ecg_channel": col.replace("ecg_bittium_", ""),
            "hrv_rmssd": compute_hrv(rr_intervals, method="rmssd"),
            "hrv_sdnn": compute_hrv(rr_intervals, method="sdnn"),
            "hrv_pnn50": compute_hrv(rr_intervals, method="pnn50"),
        }

        list_hrv_summary.append(hrv_info)

    return pd.DataFrame(list_hrv_summary)

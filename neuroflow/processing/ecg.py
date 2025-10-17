# %%
import pandas as pd
from neuroflow.utils.signals import get_sampling_info
from pathlib import Path
import numpy as np
from scipy import signal

def ecgevents2csv(file_data, detector, detector_params={}, output_file=None):
    df = pd.read_csv(file_data)
    df["time"] = pd.to_datetime(df["time"])

    match detector:
        case "pan-tompkins":
            df_events = rr_pantompkins(df, **detector_params)

    if output_file is None:
        output_file = (
            Path(file_data).parent / f"{file_data.stem}_events-ecg_detector-{detector}.csv"
        )
    df_events.to_csv(output_file, index=False)

    return output_file


def _filter_ecg(ecg, fs):
    """Preprocesses ECG timestamps.

    Args:
        ecg (np.array): 1-D time series of ECG data.
        fs (np.float): Sampling frequency of ECG data.
    Returns:
        ecg_filtered: Filtered ECG data.
    """
    f1 = 5 / fs
    f2 = 15 / fs

    b, a = signal.butter(1, [f1 * 2, f2 * 2], btype="bandpass")

    ecg_filtered = signal.lfilter(b, a, ecg)

    return ecg_filtered


def _moving_window_average(signal, window_size):
    ret = np.cumsum(signal, dtype=float)
    ret[window_size:] = ret[window_size:] - ret[:-window_size]

    for i in range(1, window_size):
        ret[i - 1] = ret[i - 1] / i
    ret[window_size - 1 :] = ret[window_size - 1 :] / window_size

    return ret


def pan_tompkins_detector(fs, ecg):
    """
    Jiapu Pan and Willis J. Tompkins.
    A Real-Time QRS Detection Algorithm.
    In: IEEE Transactions on Biomedical Engineering
    BME-32.3 (1985), pp. 230-236.
    """

    maxQRSduration = 0.150  # sec
    f1 = 5 / fs
    f2 = 15 / fs

    b, a = signal.butter(1, [f1 * 2, f2 * 2], btype="bandpass")

    filtered_ecg = signal.lfilter(b, a, ecg)

    diff = np.diff(filtered_ecg)

    squared = diff * diff

    N = int(maxQRSduration * fs)
    mwa = _moving_window_average(squared, N)
    mwa[: int(maxQRSduration * fs * 2)] = 0

    pks, _ = signal.find_peaks(mwa, distance=0.3 * fs, height=np.mean(mwa))
    # pks -= int(np.round(N/2))
    pks -= N

    return mwa, pks


def rr_pantompkins(df_data, ecg_channel="ecg0"):
    """Detect RR peaks from ECG.

    Args:
        df_data (pd.DataFrame): Standardized DataFrame of IMU data
    Returns:
        df_data: DataFrame with RR events column.
    """
    fs = get_sampling_info(df_data["time"])["frequency"]
    voltage_filt = _filter_ecg(df_data[ecg_channel], fs)

    _, pks = pan_tompkins_detector(fs, voltage_filt)

    # create an RR event column
    rr_events = np.zeros(len(voltage_filt))
    rr_events[pks] = 100

    df_data[f"ecg_bittium_{ecg_channel}"] = rr_events

    return df_data

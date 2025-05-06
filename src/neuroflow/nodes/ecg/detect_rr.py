import numpy as np
import pandas as pd
from scipy import signal
from typing import Any, Callable, Dict
import copy


def filter_ecg(
    data_ecg: Dict[str, Callable[[], Any]],
) -> Dict[str, Callable[[], Any]]:
    """Preprocesses ECG timestamps.

    Args:
        data_ecg: Raw Bittium files.
    Returns:
        data_filtered: Filtered Bittium files.
    """

    data_filtered = copy.deepcopy(data_ecg)
    for i, (key, item) in enumerate(sorted(data_ecg.items())[:]):
        print(key)
        data = item["data"]
        fs = data["sampling_frequency"].values[0]

        f1 = 5 / fs
        f2 = 15 / fs

        b, a = signal.butter(1, [f1 * 2, f2 * 2], btype="bandpass")

        filtered_ecg = signal.lfilter(b, a, data["voltage"])
        data["voltage_filt"] = filtered_ecg.copy()

        data_filtered[key]["data"] = data.copy()

    return data_filtered


def moving_window_average(signal, window_size):
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
    BME-32.3 (1985), pp. 230–236.
    """

    maxQRSduration = 0.150  # sec
    f1 = 5 / fs
    f2 = 15 / fs

    b, a = signal.butter(1, [f1 * 2, f2 * 2], btype="bandpass")

    filtered_ecg = signal.lfilter(b, a, ecg)

    diff = np.diff(filtered_ecg)

    squared = diff * diff

    N = int(maxQRSduration * fs)
    mwa = moving_window_average(squared, N)
    mwa[: int(maxQRSduration * fs * 2)] = 0

    pks, _ = signal.find_peaks(mwa, distance=0.3 * fs, height=np.mean(mwa))

    return mwa, pks


def detect_rr_peaks(
    data_ecg: Dict[str, Callable[[], Any]],
) -> Dict[str, Callable[[], Any]]:
    """Detect RR peaks from ECG.

    Args:
        data_ecg: Filtered Bittium files.
    Returns:
        data_rr: DataFrame of RR peak times.
    """
    data_rr = copy.deepcopy(data_ecg)
    for i, (key, item) in enumerate(sorted(data_ecg.items())[:]):
        print(key)

        data = item["data"]
        fs = data["sampling_frequency"].values[0]

        _, pks = pan_tompkins_detector(fs, data["voltage_filt"])
        df_rr = pd.DataFrame({"r_peaks": data["time"].values[pks]})
        df_rr["sampling_frequency"] = fs

        data_rr[key]["data"] = df_rr.copy()

    return data_rr

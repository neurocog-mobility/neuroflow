import numpy as np
import pandas as pd


def convert_timestamps(df):
    try:
        df["time"] = df["time"].str.split("(").str[0].str.strip()
        df["time"] = df["time"].str.replace("GMT", "", regex=False).str.strip()
        df["time"] = pd.to_datetime(
            df["time"],
            format="%a %b %d %Y %H:%M:%S %z",
        ).dt.tz_localize(None)
    except Exception as e:
        try:
            df["time"] = pd.to_datetime(df["time"])
        except Exception as e:
            print(e)
            raise ValueError(
                "Sync timestamps unreadable. Check formatting to be UNIX/ISO/UTC."
            )

    return df


def get_sampling_info(time):
    """
    Compute sampling period and frequency.

    Args:
        time (numpy array or pd.Series): Array or Series of timestamps (dtype <M8[ns]).

    Returns:
        dict: {"period": sampling period, "frequency": sampling frequency}
    """
    dt = np.mean(np.diff(time) / np.timedelta64(1, "s"))  # seconds
    fs = 1 / dt

    return {"period": dt, "frequency": fs}


def detect_wrist_axes(x, y, z):
    r_x = np.mean(np.abs(x))
    r_y = np.mean(np.abs(y))
    r_z = np.mean(np.abs(z))

    candidates = {"data": [[0, 1], [0, 2], [1, 2]], "r": [r_z, r_y, r_x]}
    id_data = np.argmax(candidates["r"])

    return candidates["data"][id_data]

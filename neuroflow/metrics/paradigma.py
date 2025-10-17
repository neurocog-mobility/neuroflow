# %%
import pandas as pd
import numpy as np
from paradigma.feature_extraction import (
    compute_peak_angular_velocity,
    compute_range_of_motion,
    extract_angle_extremes,
)
from neuroflow.utils.signals import get_sampling_info


def _find_paradigma_armswing_columns(df):
    col_nw = [col for col in df.columns if "gait_paradigma" in col]

    return col_nw


def summarize_armswing(df):
    list_armswing_summary = []

    for col in _find_paradigma_armswing_columns(df):
        angle = df[col].values
        fs = get_sampling_info(pd.to_datetime(df["time"]))["frequency"]
        vel = np.gradient(angle) * fs

        idx_swing, _, _ = extract_angle_extremes(angle, fs)
        num_swing = list(range(1, len(idx_swing)))
        rom_swing = compute_range_of_motion(angle, idx_swing)
        pav_swing = compute_peak_angular_velocity(vel, idx_swing)

        armswing_info = [
            {
                "swing_number": num_swing[s],
                "swing_start": idx_swing[s],
                "swing_end": idx_swing[s + 1],
                "rom": rom_swing[s],
                "peakvel": pav_swing[s],
            }
            for s in range(len(num_swing))
        ]

        list_armswing_summary += armswing_info

    return pd.DataFrame(list_armswing_summary)

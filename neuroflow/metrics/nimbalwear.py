# %%
from scipy.ndimage import label
import pandas as pd
import numpy as np
from neuroflow.utils.signals import get_sampling_info


def _find_nimbalwear_state_columns(df):
    col_nw = [col for col in df.columns if "gait_nimbalwear" in col]

    return col_nw


def extract_steps(data_step_state, state_column):
    """Extracts step phases from nimbalwear state array into a table.

    Args:
        data_step_state (pd.DataFrame): Standardized DataFrame of IMU data with step state column.
        state_column (str): Name of step state column.
    Returns:
        data_steps: Table of step information (phase start and end).
    """
    data = data_step_state[state_column].values
    list_step_phases = ["pushoff", "early-swing", "late-swing", "heelstrike"]
    dict_phases = {
        phase: {"arr": label(data == p + 1)[0], "num": label(data == p + 1)[1]}
        for p, phase in enumerate(list_step_phases)
    }

    # assert only complete step cycles exist
    assert dict_phases["pushoff"]["num"] == dict_phases["early-swing"]["num"]
    assert dict_phases["pushoff"]["num"] == dict_phases["late-swing"]["num"]
    assert dict_phases["pushoff"]["num"] == dict_phases["heelstrike"]["num"]
    n_steps = dict_phases["pushoff"]["num"]

    steps = []
    for s in range(1, n_steps + 1):
        for p, (pkey, pdata) in enumerate(dict_phases.items()):
            pidx = np.where(pdata["arr"] == s)[0]

            steps.append(
                {
                    "step_number": s,
                    "step_phase": p + 1,
                    "phase_label": pkey,
                    "phase_start": pidx[0],
                    "phase_end": pidx[-1],
                }
            )

    data_steps = pd.DataFrame(steps)

    print("Step extraction complete.")
    return data_steps


def summarize_steps(df):
    list_step_summaries = []
    for col in _find_nimbalwear_state_columns(df):
        print(col)
        df_steps = extract_steps(df, col)
        sampling_info = get_sampling_info(df["time"])

        # determine foot
        if "left" in col:
            step_foot = "left"
        else:
            step_foot = "right"

        list_step_info = []
        
        if len(df_steps) > 0:
            for s, step in enumerate(df_steps["step_number"].unique()):
                df_step = df_steps[df_steps["step_number"] == step].copy()
                raw_step = df.iloc[
                    df_step["phase_start"].values[0] : df_step["phase_end"].values[0], :
                ].copy()

                if len(df_step) == 4:  # Ensure step validity
                    step_duration = (
                        df_step["phase_end"].values[-1] - df_step["phase_start"].values[0]
                    ) * sampling_info["period"]
                    toff_duration = (
                        df_step["phase_end"].values[0] - df_step["phase_start"].values[0]
                    ) * sampling_info["period"]
                    eswing_duration = (
                        df_step["phase_end"].values[1] - df_step["phase_start"].values[1]
                    ) * sampling_info["period"]
                    lswing_duration = (
                        df_step["phase_end"].values[2] - df_step["phase_start"].values[2]
                    ) * sampling_info["period"]
                    hstrike_duration = (
                        df_step["phase_end"].values[3] - df_step["phase_start"].values[3]
                    ) * sampling_info["period"]
                    accel_mag = np.sqrt(
                        raw_step[f"{step_foot}ankle_ax"].values ** 2
                        + raw_step[f"{step_foot}ankle_ay"].values ** 2
                        + raw_step[f"{step_foot}ankle_az"].values ** 2
                    )
                    accel_avg = np.nanmean(accel_mag)
                    accel_max = np.nanmax(accel_mag)

                    step_info = {
                        "step_foot": step_foot,
                        "step_start": df_step["phase_start"].values[0],
                        "step_end": df_step["phase_end"].values[-1],
                        "step_duration": step_duration,
                        "pushoff_duration": toff_duration,
                        "early-swing_duration": eswing_duration,
                        "late-swing_duration": lswing_duration,
                        "heelstrike_duration": hstrike_duration,
                        "step_accel_max": accel_max,
                        "step_accel_avg": accel_avg,
                    }

                    list_step_info.append(step_info)

            list_step_summaries.append(pd.DataFrame(list_step_info))

    return pd.concat(list_step_summaries).sort_values(by="step_start")

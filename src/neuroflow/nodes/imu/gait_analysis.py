from typing import Any, Callable, Dict
from scipy import ndimage
import numpy as np
import pandas as pd
from pathlib import Path

def extract_steps(data_step_state: Dict[str, Callable[[], Any]]) -> Dict[str, Callable[[], Any]]:
    """Extracts step phases from state array into a table.

    Args:
        data_step_state: Step states from raw data.
    Returns:
        data_steps: Table of step information (phase start and end).
    """
    data_steps = {}
    for key, value_state in sorted(data_step_state.items())[:]:
        data_state = value_state["data"]
        data = data_state["step_state"].values
        list_step_phases = ["pushoff", "early-swing", "late-swing", "heelstrike"]
        dict_phases = { phase: { "arr": ndimage.label(data == p + 1)[0],
                                "num": ndimage.label(data == p + 1)[1]}
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
                    {"step_number": s,
                    "step_phase": p + 1,
                    "phase_label": pkey,
                    "phase_start": pidx[0],
                    "phase_end": pidx[-1],
                    }
                )
        
        data_steps[key] = pd.DataFrame(steps)

    print("Step extraction complete.")
    return data_steps


def split_axivity_into_steps(data_step_state: Dict[str, Callable[[], Any]],
                             data_step_times: Dict[str, Callable[[], Any]]) -> Dict[str, Callable[[], Any]]:
    """Splits each axivity trial into individual steps.

    Args:
        data_step_state: Raw axivity trials with step state column.
        data_step_times: Table of detected step times.
    Returns:
        data_steps: Axivity files split by steps.
    """
    data_steps = {}
    for partition_key, partition_steps in sorted(data_step_times.items())[:]:
        partition_data = data_step_state[partition_key]["data"]

        # segment into steps
        for s in partition_steps["step_number"].unique():
            step_info = partition_steps.loc[partition_steps["step_number"] == s].copy()
            
            step_start = step_info["phase_start"].values[0]
            step_end = step_info["phase_end"].values[-1]

            data_step = partition_data.iloc[step_start:step_end].copy()
            metadata = data_step_state[partition_key]["metadata"].copy()
            metadata.update({"step": s})
            
            step_key = f"{Path(partition_key).stem}_Step{s}{Path(partition_key).suffix}"
            data_steps[step_key] = {
                "metadata": metadata,
                "data": data_step.copy()
            }

    print("Split Axivity into steps complete.")
    return data_steps


def summarize_steps(data_step_times: Dict[str, Callable[[], Any]],
                    data_steps: Dict[str, Callable[[], Any]]) -> Dict[str, Callable[[], Any]]:
    """Summarizes the step characteristics for each trial and sensor.

    Args:
        data_step_times: Table of detected step times.
        data_steps: Axivity files split by steps.
    Returns:
        data_step_summaries: Tables of step summaries for each trial and ankle sensor.
    """
    data_step_summaries = {}
    for key, data in sorted(data_step_times.items())[:]:
        step_summary = []
        for s in data["step_number"].unique():
            data_step = data.loc[data["step_number"] == s].copy()

            step_key = f"{Path(key).stem}_Step{s}{Path(key).suffix}"
            metadata = data_steps[step_key]["metadata"]
            raw_step = data_steps[step_key]["data"]
            ds = np.mean(np.diff(raw_step["time_seconds"]))

            if "left" in key:
                step_foot = "left"
            else:
                step_foot = "right"

            step_duration = (
                data_step["phase_end"].values[-1] - \
                data_step["phase_start"].values[0]
                ) * ds
            toff_duration = (
                data_step["phase_end"].values[0] - \
                data_step["phase_start"].values[0]
                ) * ds
            eswing_duration = (
                data_step["phase_end"].values[1] - \
                data_step["phase_start"].values[1]
                ) * ds
            lswing_duration = (
                data_step["phase_end"].values[2] - \
                data_step["phase_start"].values[2]
                ) * ds
            hstrike_duration = (
                data_step["phase_end"].values[3] - \
                data_step["phase_start"].values[3]
                ) * ds
            
            accel_mag = np.sqrt(
                raw_step["accel_x"].values ** 2 +\
                raw_step["accel_x"].values ** 2 +\
                raw_step["accel_x"].values ** 2
                )
            accel_avg = np.nanmean(accel_mag)
            accel_max = np.nanmax(accel_mag)

            step = metadata.copy()
            step_info = {
                "step_foot": step_foot,
                "step_start": data_step["phase_start"].values[0],
                "step_end": data_step["phase_end"].values[-1],
                "step_duration": step_duration,
                "pushoff_duration": toff_duration,
                "early-swing_duration": eswing_duration,
                "late-swing_duration": lswing_duration,
                "heelstrike_duration": hstrike_duration,
                "step_accel_max": accel_max,
                "step_accel_avg": accel_avg,
            }
            step.update(step_info)

            step_summary.append(step.copy())

        df_step_summary = pd.DataFrame(step_summary)
        data_step_summaries[key] = df_step_summary

    print("Step summary complete.")
    return data_step_summaries


def compile_step_summary(data_step_summaries: Dict[str, Callable[[], Any]]) -> pd.DataFrame:
    """Compiles step summaries across all trials into a single table for export.

    Args:
        data_step_summaries: Tables of step summaries for each trial and ankle sensor.
    Returns:
        compiled_summary: Compiled summary of all steps across all trials.
    """
    step_summaries = [summary for summary in data_step_summaries.values()]
    df_summary = pd.concat(step_summaries)

    # correct step number between left and right feet for each unique trial
    df_keys = df_summary.groupby(["site", "subject", "session", "trial"]).count().reset_index()
    updated_summaries = []
    for k, key in df_keys.iterrows():
        df = df_summary.loc[
            (df_summary["site"] == key["site"]) &
            (df_summary["subject"] == key["subject"]) &
            (df_summary["session"] == key["session"]) &
            (df_summary["trial"] == key["trial"])
        ].copy()
        df = df.sort_values(['step_start'])
        df.reset_index(inplace=True)

        df.insert(
            df.columns.get_loc("step"),
            "step_in_trial",
            df.index + 1
            )
        df.insert(
            df.columns.get_loc("step"),
            "footstep",
            df["step"]
            )
        df.drop("step", axis=1, inplace=True)

        updated_summaries.append(df.copy())

    compiled_summary = pd.concat(updated_summaries)

    print("Step summary compilation complete.")
    return compiled_summary
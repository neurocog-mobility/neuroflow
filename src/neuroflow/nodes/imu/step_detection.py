"""Step detection functions adapted from the nimbalwear package.
Link to nimbalwear github repository: <https://github.com/nimbal/nimbalwear>
"""

from typing import Any, Callable, Dict, List
import pandas as pd
import numpy as np
from tqdm import tqdm
from scipy.signal import find_peaks, peak_widths
from scipy import ndimage
from neuroflow.nodes.utils.parse import _get_sample_rate


def _window_correlate(sig1, sig2):
    sig1 = sig1 if type(sig1) is np.ndarray else np.array(sig1)
    sig2 = sig2 if type(sig2) is np.ndarray else np.array(sig2)

    sig = max([sig1, sig2], key=len)
    window = min([sig1, sig2], key=len)

    engine = 'cython' if len(sig) < 100000 else 'numba'
    cc = pd.Series(sig).rolling(window=len(window)).apply(lambda x: np.corrcoef(x, window)[0, 1], raw=True,
                                                          engine=engine).shift(-len(window) + 1).fillna(0).to_numpy()

    return cc


def _push_off_detection(vert_accel, pushoff_avg, freq, pushoff_threshold=0.85):
    cc_list = _window_correlate(vert_accel, pushoff_avg)

    # TODO: Postponed -- DISTANCE CAN BE ADJUSTED FOR THE LENGTH OF ONE STEP RIGHT NOW ASSUMPTION IS THAT A PERSON
    # CANT TAKE 2 STEPS WITHIN 0.5s
    pushoff_ind, _ = find_peaks(cc_list, height=pushoff_threshold, distance=max(0.2 * freq, 1))

    return pushoff_ind


def _mid_swing_peak_detect(data, pushoff_ind, freq, swing_phase_time=0.2):
    swing_detect_len = int(freq * swing_phase_time)  # length to check for swing
    detect_window = data[pushoff_ind:pushoff_ind + swing_detect_len]
    peaks, prop = find_peaks(-detect_window,
                             distance=max(swing_detect_len * 0.25, 1),
                             prominence=0.2, wlen=swing_detect_len,
                             width=[0 * freq, swing_phase_time * freq], rel_height=0.75)
    if len(peaks) == 0:
        return None

    results = peak_widths(-detect_window, peaks)
    prop['widths'] = results[0]

    return pushoff_ind + peaks[np.argmax(prop['widths'])]


def _heel_strike_detect(data, window_ind, freq, heel_strike_detect_time=0.5):
    heel_detect = int(freq * heel_strike_detect_time)
    detect_window = data[window_ind:window_ind + heel_detect]
    accel_t_plus1 = np.append(
        detect_window[1:detect_window.size], detect_window[-1])
    accel_t_minus1 = np.insert(detect_window[:-1], 0, detect_window[0])
    accel_derivative = (accel_t_plus1 - accel_t_minus1) / (2 / freq)

    return accel_derivative


def _get_vertical_acceleration(raw_data):
    columns_accel = ["accel_x", "accel_y", "accel_z"]
    idx_vertical = np.argmax(raw_data[columns_accel].abs().mean())
    column_vertical = columns_accel[idx_vertical]

    return raw_data[column_vertical].values


def _filter_state_array(state_array):
    pushoffs, n_pushoffs = ndimage.label(state_array == 1)
    heelstrikes, n_heelstrikes = ndimage.label(state_array == 4)

    # get start of each pushoff
    pushoff_start = []
    for p in range(1, n_pushoffs + 1):
        idx_po = np.where(pushoffs == p)[0][0]
        pushoff_start.append(idx_po)

    # for each heelstrike, find the closest preceding pushoff
    steps = []
    for h in range(1, n_heelstrikes + 1):
        idx_hs = np.where(heelstrikes == h)[0][-1]
        idx_hs_po = np.where(idx_hs - pushoff_start > 0)[0][-1]

        steps.append((pushoff_start[idx_hs_po], idx_hs))

    filtered_state_array = np.zeros(state_array.shape)
    for step in steps:
        filtered_state_array[step[0]:step[1] + 1] = state_array[step[0]:step[1] + 1].copy()

    return filtered_state_array


def detect_steps_nimbal(data_axivity: Dict[str, Callable[[], Any]],
                        data_pushoff: pd.DataFrame,
                        step_params: Dict[str, float]) -> Dict[str, Callable[[], Any]]:
    """Detects steps from ankle accelerometers - adapted from nimbalwear algorithm.
    See <https://github.com/nimbal/nimbalwear/> for more details.

    Args:
        data_axivity: Raw axivity files.
        data_pushoff: Nimbal pushoff data.
        step_params: Parameters for step detection.
    Returns:
        data_processed: Step state array for each trial (1: pushoff, 2: early-swing, 3: late-swing, 4: heelstrike).
    """
    data_step_state = {}
    for partition_key, partition_value in sorted(data_axivity.items())[:]:
        partition_data = partition_value["data"]
        
        if "ankle" in partition_value["metadata"]["sensor"]:
            # print(partition_key)

            vertical_accel = _get_vertical_acceleration(partition_data)
            sample_rate = _get_sample_rate(partition_data)

            # Detect pushoff
            pushoff_ind = _push_off_detection(vertical_accel,
                                            data_pushoff['avg'],
                                            sample_rate,
                                            pushoff_threshold=step_params["pushoff_threshold"])
            pushoff_len = int(step_params["pushoff_time"] * sample_rate)
            end_pushoff_ind = pushoff_ind + pushoff_len

            # initialize detection structures
            end_i = None
            state_arr = np.zeros(vertical_accel.size)
            time_seconds = np.linspace(0, len(state_arr), len(state_arr)) / sample_rate

            # run step detection loop
            for count, i in enumerate(end_pushoff_ind):
                # mean/std check for pushoff, state = 1
                pushoff_mean = np.mean(vertical_accel[i - pushoff_len:i])
                upper = (data_pushoff['avg'] + data_pushoff['std'])
                lower = (data_pushoff['avg'] - data_pushoff['std'])
                if not np.any((np.abs(pushoff_mean) < upper) & (np.abs(pushoff_mean) > lower)):
                    continue

                # detect mid-swing
                mid_swing_i = _mid_swing_peak_detect(
                    vertical_accel, i, sample_rate,
                    swing_phase_time=step_params["swing_phase_time"])
                if mid_swing_i is None:
                    continue

                # detect heel strike
                accel_derivatives = _heel_strike_detect(
                    vertical_accel, mid_swing_i, sample_rate,
                    heel_strike_detect_time=step_params["heel_strike_detect_time"])
                accel_threshold_list = np.where(
                    accel_derivatives < step_params["heel_strike_threshold"])[0]
                if len(accel_threshold_list) == 0:
                    continue
                accel_ind = accel_threshold_list[0] + mid_swing_i + 1
                end_i = accel_ind + int(step_params["foot_down_time"] * sample_rate)

                # update state array, indices, and step lengths
                state_arr[i - pushoff_len:i] = 1        # pushoff
                state_arr[i:mid_swing_i] = 2            # early-swing
                state_arr[mid_swing_i:accel_ind] = 3    # late-swing
                state_arr[accel_ind:end_i] = 4          # heelstrike

            filtered_state_array = _filter_state_array(state_arr)

            # data_step_state[partition_key] = state_arr
            state_data = partition_data.copy()
            state_data["step_state"] = filtered_state_array
            state_data["time_seconds"] = time_seconds
            data_step_state[partition_key] = {
                "metadata": partition_value["metadata"].copy(),
                "data": state_data
            }

    print("Step detection complete.")
    return data_step_state
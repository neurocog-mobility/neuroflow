from typing import Any, Callable, Dict, List
from neuroflow.nodes.utils.parse import (
    get_metadata_from_filename,
    get_metadata_indices_from_filepattern,
)
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np
import copy


def _timestring_to_datetime(timestring: str):
    timestring = timestring.split(" GMT")[0]
    datetime_object = datetime.strptime(timestring, "%a %b %d %Y %H:%M:%S")
    return datetime_object


def parse_bittium(
    data_ecg: Dict[str, Callable[[], Any]],
    data_sync: Dict[str, Callable[[], Any]],
    ecg_filepattern: Dict[str, str],
    sync_filepattern: Dict[str, str],
) -> Dict[str, Callable[[], Any]]:
    """Splits each axivity session into individual trials based on provided timestamps.

    Args:
        data_ecg: Raw Bittium files.
        data_sync: Trial sync timestamps.
        ecg_filepattern: Filepattern for extracting metadata for each Bittium file.
        sync_filepattern: Filepattern for extracting metadata for each sync file.
    Returns:
        data_processed: Bittium files split by trial.
    """

    metadata_index = get_metadata_indices_from_filepattern(ecg_filepattern["pattern"])

    data_processed = {}
    for p, (partition_key, partition_data) in enumerate(sorted(data_ecg.items())[:]):
        print(partition_key)

        # get partition metadata
        partition_metadata = get_metadata_from_filename(partition_key, metadata_index)
        # get edf time info
        session_start = partition_data.info["meas_date"]
        sampling_freq = partition_data.info["sfreq"]
        partition_times = partition_data.times

        if data_sync:
            # get corresponding sync file
            found_sync_file = False
            for s, (sync_key, sync_data) in enumerate(sorted(data_sync.items())):
                sync_metadata_index = get_metadata_indices_from_filepattern(
                    sync_filepattern["pattern"]
                )
                sync_metadata = get_metadata_from_filename(
                    sync_key, sync_metadata_index
                )
                subset_partition_meta = {
                    k: partition_metadata[k] for k in list(sync_metadata.keys())
                }

                if sync_metadata == subset_partition_meta:
                    found_sync_file = True
                    # proceed to split intp trials
                    sync_data["datetime"] = sync_data["time"].apply(
                        lambda x: _timestring_to_datetime(x)
                    )
                    sync_data["datetime"] = pd.to_datetime(sync_data["datetime"])

                    for t, tnum in enumerate(np.unique(sync_data["trial"])[:]):
                        trial_timestamp = sync_data.loc[
                            sync_data["trial"] == tnum
                        ].copy()
                        trial_start = trial_timestamp.loc[
                            trial_timestamp["type"] == "start", "datetime"
                        ].values[0]
                        trial_stop = trial_timestamp.loc[
                            trial_timestamp["type"] == "stop", "datetime"
                        ].values[0]

                        trial_start = trial_start.astype("datetime64[s]").astype("int")
                        trial_stop = trial_stop.astype("datetime64[s]").astype("int")

                        sec_start = trial_start - session_start.timestamp()
                        sec_stop = trial_stop - session_start.timestamp()

                        idx_start = np.argmin(np.abs(partition_times - sec_start))
                        idx_stop = np.argmin(np.abs(partition_times - sec_stop))

                        try:
                            ch_idx = partition_data.ch_names.index("ECG")
                            trial_data, trial_times = partition_data[
                                ch_idx, idx_start:idx_stop
                            ]
                            trial_times -= trial_times[0]
                            trial_data = trial_data.flatten()

                            partition_trial = pd.DataFrame(
                                {
                                    "time": trial_times.copy(),
                                    "voltage": trial_data.copy(),
                                    "sampling_frequency": sampling_freq,
                                }
                            )

                            processed_key = f"{Path(partition_key).stem}_Trial{tnum}{Path(partition_key).suffix}"

                            processed_metadata = partition_metadata.copy()
                            processed_metadata["trial"] = tnum

                            data_processed[processed_key] = {
                                "metadata": processed_metadata,
                                "data": partition_trial,
                            }
                        except Exception as e:
                            print(e)

            print("Axivity loading and split into trials complete.")
        else:
            processed_metadata = partition_metadata.copy()
            processed_metadata["trial"] = 1

            ch_idx = partition_data.ch_names.index("ECG")
            trial_data, trial_times = partition_data[ch_idx, :]
            trial_times -= trial_times[0]
            trial_data = trial_data.flatten()

            processed_data = pd.DataFrame(
                {
                    "time": trial_times.copy(),
                    "voltage": trial_data.copy(),
                    "sampling_frequency": sampling_freq,
                }
            )
            data_processed[partition_key] = {
                "metadata": processed_metadata,
                "data": processed_data,
            }

            print("Axivity loading complete.")

    return data_processed

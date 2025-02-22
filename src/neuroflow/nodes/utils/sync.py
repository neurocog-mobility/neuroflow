from typing import Any, Callable, Dict, List
import pandas as pd
from datetime import datetime
import numpy as np
from pathlib import Path
from neuroflow.nodes.utils.parse import (_get_metadata_from_filename, _get_metadata_indices_from_filepattern)


def _timestring_to_datetime(timestring: str):
    timestring = timestring.split(" GMT")[0]
    datetime_object = datetime.strptime(timestring, "%a %b %d %Y %H:%M:%S")
    return datetime_object


def split_axivity_by_trial_timestamps(data_axivity: Dict[str, Callable[[], Any]],
                                      data_sync: Dict[str, Callable[[], Any]],
                                      axivity_filepattern: Dict[str, str],
                                      sync_filepattern: Dict[str, str],) -> Dict[str, Callable[[], Any]]:
    """Splits each axivity session into individual trials based on provided timestamps.

    Args:
        data_axivity: Raw axivity files.
        data_sync: Trial sync timestamps.
        axivity_filepattern: Filepattern for extracting metadata for each axivity file.
        sync_filepattern: Filepattern for extracting metadata for each sync file.
    Returns:
        data_processed: Axivity files split by trial.
    """

    metadata_index = _get_metadata_indices_from_filepattern(axivity_filepattern["pattern"])
    
    data_processed = {}
    for p, (partition_key, partition_data) in enumerate(sorted(data_axivity.items())):
    
        # get partition metadata
        partition_metadata = _get_metadata_from_filename(partition_key, metadata_index)
        
        # get corresponding sync file
        found_sync_file = False
        for s, (sync_key, sync_data) in enumerate(sorted(data_sync.items())):
            sync_metadata_index = _get_metadata_indices_from_filepattern(sync_filepattern["pattern"])
            sync_metadata = _get_metadata_from_filename(sync_key, sync_metadata_index)
            subset_partition_meta = {k: partition_metadata[k] for k in list(sync_metadata.keys())}
    
            if sync_metadata == subset_partition_meta:
                found_sync_file = True
                # proceed to split intp trials
                sync_data["datetime"] = sync_data["time"].apply(lambda x: _timestring_to_datetime(x))
                sync_data["datetime"] = pd.to_datetime(sync_data["datetime"])
                
                for t, tnum in enumerate(np.unique(sync_data["trial"])[:]):
                    trial_timestamp = sync_data.loc[sync_data["trial"] == tnum].copy()
                    time_start = trial_timestamp.loc[trial_timestamp["type"] == "start", "datetime"].values[0]
                    time_stop = trial_timestamp.loc[trial_timestamp["type"] == "stop", "datetime"].values[0]
    
                    mask_trial = np.logical_and(
                        partition_data["time"] >= time_start,
                        partition_data["time"] <= time_stop,
                    )
                    partition_trial = partition_data.loc[mask_trial].copy()
    
                    processed_key = f"{Path(partition_key).stem}_Trial{tnum}{Path(partition_key).suffix}"
    
                    processed_metadata = partition_metadata.copy()
                    processed_metadata["trial"] = tnum
    
                    data_processed[processed_key] = { "metadata": processed_metadata, "data": partition_trial }
    
    print("Split into trials complete.")
    return data_processed

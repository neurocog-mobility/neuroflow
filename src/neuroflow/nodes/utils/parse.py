from typing import Dict, List
from pathlib import Path
import numpy as np
from neuroflow.definitions import _define_filepattern

def _get_metadata_indices_from_filepattern(filepattern: str):
    filepattern_fields = _define_filepattern()
    fileparts = Path(filepattern).stem.split("_")

    metadata_index = {}
    for key, val in filepattern_fields.items():
        if val in fileparts:
            id_filepart = [f for f, filepart in enumerate(fileparts) if val in filepart][0]
            metadata_index[key] = id_filepart

    return metadata_index


def _get_metadata_from_filename(filename: str,
                                metadata_index: Dict[str, int]):
    keyparts = Path(filename).stem.split("_")
    metadata = { metakey: keyparts[metadata_index[metakey]] for metakey in metadata_index.keys() }

    return metadata


def _get_sample_rate(raw_data):
    dt_nanoseconds = np.mean(np.diff(raw_data["time"]))
    dt_seconds = int(dt_nanoseconds) / 1000000000.

    return 1 / dt_seconds
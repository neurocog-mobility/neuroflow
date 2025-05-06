from pathlib import PurePosixPath
from typing import Any, Dict
import numpy as np

import fsspec
import mne
import os
from kedro.io import AbstractDataset
from kedro.io.core import get_filepath_str, get_protocol_and_path


class BittiumDataset(AbstractDataset[np.ndarray, np.ndarray]):
    """``BittiumDataset`` loads / save .edf data from a given filepath as a dict of ECG data.

    Example:
    ::

        >>> BittiumDataset(filepath='/bittium/file/path.edf')
    """

    def __init__(self, filepath: str):
        """Creates a new instance of BittiumDataset to load / save .edf data at the given filepath.

        Args:
            filepath: The location of the .edf file to load / save data.
        """
        protocol, path = get_protocol_and_path(filepath)
        self._protocol = protocol
        self._filepath = PurePosixPath(path)
        self._fs = fsspec.filesystem(self._protocol)

    def load(self) -> dict:
        """Loads data from the .edf file.

        Returns:
            Data from the .edf file as a pandas dataframe.
        """
        load_path = get_filepath_str(self._filepath, self._protocol)
        print(load_path)
        f = mne.io.read_raw_edf(load_path)

        return f

    def save(self, data: dict) -> None:
        """Saves .edf data to the specified filepath"""
        save_path = get_filepath_str(self._filepath, self._protocol)
        npy_save_path = f"{os.path.splitext(save_path)[0]}_ecg.npy"
        with self._fs.open(npy_save_path, "wb") as f:
            np.save(f, data["ecg"])

    def _describe(self) -> Dict[str, Any]:
        """Returns a dict that describes the attributes of the dataset"""
        return dict(filepath=self._filepath, protocol=self._protocol)

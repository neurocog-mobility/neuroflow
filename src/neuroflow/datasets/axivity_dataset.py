from pathlib import PurePosixPath
from typing import Any, Dict

import numpy as np
import pandas as pd
from openmovement.load import CwaData

import fsspec
import os
from kedro.io import AbstractDataset
from kedro.io.core import get_filepath_str, get_protocol_and_path


class AxivityDataset(AbstractDataset[np.ndarray, np.ndarray]):
    """``AxivityDataset`` loads / save .cwa data from a given filepath as `pandas` Dataframe.

    Example:
    ::

        >>> AxivityDataset(filepath='/axivity/file/path.cwa')
    """

    def __init__(self, filepath: str):
        """Creates a new instance of OpalDataset to load / save .cwa data at the given filepath.

        Args:
            filepath: The location of the .cwa file to load / save data.
        """
        protocol, path = get_protocol_and_path(filepath)
        self._protocol = protocol
        self._filepath = PurePosixPath(path)
        self._fs = fsspec.filesystem(self._protocol)

    def load(self) -> pd.DataFrame:
        """Loads data from the .cwa file.

        Returns:
            Data from the .wa file as a pandas dataframe.
        """
        load_path = get_filepath_str(self._filepath, self._protocol)
        with CwaData(load_path, include_gyro=True, include_temperature=True, include_accel=True, include_light=True) as cwa_data:
            df_cwa = cwa_data.get_samples()
            # format cwa times
            df_cwa["time"] = pd.to_datetime(df_cwa["time"])

            return df_cwa

    def save(self, data: pd.DataFrame) -> None:
        """Saves .cwa data to the specified filepath"""
        save_path = get_filepath_str(self._filepath, self._protocol)
        csv_save_path = f"{os.path.splitext(save_path)[0]}.csv"
        with self._fs.open(csv_save_path, "wb") as f:
            data.to_csv(
                f,
                index=False
            )

    def _describe(self) -> Dict[str, Any]:
        """Returns a dict that describes the attributes of the dataset"""
        return dict(filepath=self._filepath, protocol=self._protocol)
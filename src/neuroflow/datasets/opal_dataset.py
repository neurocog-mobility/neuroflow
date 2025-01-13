from pathlib import PurePosixPath
from typing import Any, Dict

import numpy as np
import pandas as pd
import h5py

import fsspec
import os
from kedro.io import AbstractDataset
from kedro.io.core import get_filepath_str, get_protocol_and_path


class OpalDataset(AbstractDataset[np.ndarray, np.ndarray]):
    """``OpalDataset`` loads / save Opal .h5 data from a given filepath as `pandas` Dataframe.

    Example:
    ::

        >>> OpalDataset(filepath='/opal/file/path.h5')
    """

    def __init__(self, filepath: str):
        """Creates a new instance of OpalDataset to load / save opal .h5 data at the given filepath.

        Args:
            filepath: The location of the .h5 file to load / save data.
        """
        protocol, path = get_protocol_and_path(filepath)
        self._protocol = protocol
        self._filepath = PurePosixPath(path)
        self._fs = fsspec.filesystem(self._protocol)

    def load(self) -> pd.DataFrame:
        """Loads data from the .h5 file.

        Returns:
            Data from the .h5 file as a pandas dataframe.
        """
        load_path = get_filepath_str(self._filepath, self._protocol)
        with self._fs.open(load_path) as f:
            h5 = h5py.File(f, "r")
            list_channels = ["Accelerometer", "Gyroscope"]

            for k, key in enumerate(list(h5["Sensors"].keys())[:]):
                # get time channel
                h5_dataset = h5["Sensors"][key]["Time"]
                df_h5 = pd.DataFrame(np.array(h5_dataset))
                df_h5.columns = ["time"]
                df_h5["device_id"] = key

                # get requested channels
                for c, channel in enumerate(list_channels):
                    h5_dataset = h5["Sensors"][key][channel]
                    print(h5_dataset)
                    df_h5_channel = pd.DataFrame(np.array(h5_dataset))
                    df_h5_channel.columns = [f"{channel.lower()}_{dim}" for dim in ["x", "y", "z"]]
                    df_h5 = pd.concat([df_h5, df_h5_channel.copy()], axis=1)

                # create master dataframe
                if k==0:
                    df_opal = df_h5.copy()
                else:
                    df_opal = pd.concat([df_opal, df_h5.copy()], axis=0)
            
            # close HDF5
            h5.close()

            return df_opal

    def save(self, data: pd.DataFrame) -> None:
        """Saves .h5 data to the specified filepath"""
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
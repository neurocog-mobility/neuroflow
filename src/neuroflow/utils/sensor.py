"""
Sensor module.
"""
import pandas as pd
from openmovement.load import CwaData

class Sensor():
    """
	A class used to represent wearable sensor IMU/ECG data for use with the
	Neurocognition & Mobility Lab analytics pipeline. Adapted from the Device
	class in the nimbalwear package: https://github.com/nimbal/nimbalwear

	This class contains methods for importing data from various file types,
	timestamping data, and cropping data.
    
	Attributes
	----------
	meta : dict
		dictionary containing all sensor attributes
	signal_headers : list
		list containing a dictionary with header attributes for each signal
	signals : list
		list of arrays of data for each signal
    """

    def __init__(self):
        """ Initialize attributes on object construction."""

        # initialize attributes
        self.meta = {
            'device_type': '',
            'device_id': ''
            }
        self.signal_headers = []
        self.signals = []

    
    def load_axivity(filepath: str):
        """
        Load Axivity data from file.

        Args:
            filepath: The location of the .cwa file to load / save data.
        """
        
        with CwaData(filepath, include_gyro=True, include_temperature=False, include_accel=True, include_light=False) as cwa_data:
            df_cwa = cwa_data.get_samples()

            # format cwa times
            df_cwa["time"] = pd.to_datetime(df_cwa["time"])


class SensorSet():
    """
	A class used to represent a set of Sensors worn by a study participant.

	This class contains methods for adding and removing Sensors, filtering
	Sensors by attributes.

	Attributes
	----------
	    
	meta : dict
		dictionary containing all subject attributes
        sensors : list
        	list of Sensor objects
    """

    def __init__(self):
        """ Initialize attributes on object construction."""

        # initialize attributes
        self.meta = {
            'study_id': '',
            'subject_id': ''
            }
        self.sensors = []

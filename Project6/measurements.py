import os
import pandas as pd
import numpy as np
from timeseries import TimeSeries
import SeriesValidators

# aggregates multiple .csv files representing timeseries for a single compund/freq
class Measurements:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        # identify .csv files containing data
        self.files = [
            f for f in os.listdir(folder_path)
            if f.endswith(".csv") and "_" in f
        ]
        # cache for lazily loaded timeseries
        self._timeseries_cache = {}

    # returns total number of possible timeseries objects across all files
    def __len__(self):
        return sum([self._count_stations_in_file(f) for f in self.files])

    # returns true if any file contains the given parameter name (e.g. NO2)
    def __contains__(self, parameter_name):
        return any(parameter_name in f for f in self.files)

    # returns a list of timeseries objects matching the given parameter name
    def get_by_parameter(self, param_name):
        return [
            ts for ts in self._load_all()
            if ts.compound == param_name
        ]
    
    # returns a list of timeseries objects for a specific station code
    def get_by_station(self, station_code):
        return [
            ts for ts in self._load_all()
            if ts.station_code == station_code
        ]

    # counts how many stations are represented in the given file
    def _count_stations_in_file(self, filename):
        path = os.path.join(self.folder_path, filename)
        df = pd.read_csv(path, nrows=6, header=None)
        return len(df.columns) - 1

    # loads all timeseries from all files into the cache
    def _load_all(self):
        if not self._timeseries_cache:
            for f in self.files:
                self._load_file(f)
        return list(self._timeseries_cache.values())

    # loads a single file and populates the cache with timeseires objects
    def _load_file(self, filename):
        path = os.path.join(self.folder_path, filename)
        df = pd.read_csv(path, skiprows=6)
        meta = pd.read_csv(path, nrows=6, header=None)

        # station code, compound, averaging time, unit
        stations = meta.iloc[1, 1:]
        compounds = meta.iloc[2, 1:]
        averaging = meta.iloc[3, 1:]
        units = meta.iloc[4, 1:]

        # first column = timestamp, parse timestamps with a fixed format to avoid warnings
        # format: "m/d/yy H:M"
        timestamps = pd.to_datetime(df.iloc[:, 0], format="%m/%d/%y %H:%M", errors="coerce")
        invalid = df.iloc[:, 0][timestamps.isna()]
        if not invalid.empty:
            print(f"\n⚠️ Invalid timestamps found in file {filename}:")
            print(invalid.head(10))  # możesz też dać .tolist() albo bez .head() jeśli chcesz wszystkie

        for idx, col in enumerate(df.columns[1:]):
            values = pd.to_numeric(df[col], errors='coerce').tolist()
            ts = TimeSeries(
                compound=compounds.iloc[idx],
                station_code=stations.iloc[idx],
                averaging_time=averaging.iloc[idx],
                timestamps=timestamps.tolist(),
                values=values,
                unit=units.iloc[idx]
            )
            key = f"{ts.compound}-{ts.station_code}-{ts.averaging_time}"
            self._timeseries_cache[key] = ts

        return self._timeseries_cache


    def detect_all_anomalies(self, validators: list, preload: bool = False):
        """
        Analyze all loaded TimeSeries using provided validators.

        :param validators: list of SeriesValidator instances
        :param preload: if True, preload all data from files
        :return: dict mapping keys to lists of anomaly messages
        """
        if preload:
            self._load_all()

        result = {}

        for key, series in self._timeseries_cache.items():
            messages = []
            for validator in validators:
                messages.extend(validator.analyze(series))
            if messages:
                result[key] = messages

        return result

def test():
    folder = "measurements"
    m = Measurements(folder)

    print(f"Number of available time series: {len(m)}")

    
    # check if any file contains a specific compound
    if "NO2" in m:
        print("At least one file contains NO2")

    # get all timeseries for a given parameter
    no2_series = m.get_by_parameter("NO2")
    print(f"Found {len(no2_series)} series with parameter NO2")

    # get all time series for a given station
    series = m.get_by_station("DsGlogWiStwo")
    print(f"Found {len(series)} series for station DsGlogWiStwo")

    # example: print some info about one series
    if series:
        example = series[0]
        print(f"{example.station_code} ({example.compound}): {len(example.timestamps)} timestamps, unit = {example.unit}")


if __name__ == "__main__":
    test()


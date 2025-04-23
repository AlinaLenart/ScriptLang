from datetime import datetime, date
import numpy as np

class TimeSeries:
    def __init__(self, compound, station_code, averaging_time, timestamps, values, unit):
        self.compound = compound
        self.station_code = station_code
        self.averaging_time = averaging_time
        # list of datetime objects
        self.timestamps = timestamps 
        # list of float values
        self.values = np.array(values, dtype=float)
        self.unit = unit
        
    def __getitem__(self, key):
        # case: int index 
        if isinstance(key, int):
            if key < 0 or key >= len(self.timestamps):
                raise IndexError("Index out of range")
            return (self.timestamps[key], self.values[key])

        # case: slice (extract portion of indexes)
        elif isinstance(key, slice):
            return list(zip(self.timestamps, self.values))[key]

        # case: datetime.datetime
        elif isinstance(key, datetime):
            for ts, val in zip(self.timestamps, self.values):
                if ts == key:
                    return val
            raise KeyError(f"No value found for timestamp: {key}")

        # case: datetime.date
        elif isinstance(key, date):
            result = [val for ts, val in zip(self.timestamps, self.values) if ts.date() == key]
            if not result:
                raise KeyError(f"No values found for date: {key}")
            return result

        else:
            raise TypeError("Key must be int, slice, datetime or date")

    @property
    def mean(self):
        if np.isnan(self.values).all():
            return None
        return float(np.nanmean(self.values))

    @property
    def stddev(self):
        if np.isnan(self.values).all():
            return None
        return float(np.nanstd(self.values))    

    def __str__(self):
        return f"TimeSeries<{self.indicator}> for {self.station_code}, {len(self.values)} points"

    def __repr__(self):
        return f"TimeSeries(indicator={self.indicator!r}, station_code={self.station_code!r}, unit={self.unit!r})"
    
    
    


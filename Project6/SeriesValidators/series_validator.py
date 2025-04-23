import abc
import numpy as np

class SeriesValidator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    # returns a list of messages about detected anomalies or an empty list
    def analyze(self, series) -> list:
        # if not implemented pass
        pass

# this class checks outliers in data, outlier means any value that is more than k standard deviations away from the mean
class OutlierDetector(SeriesValidator):
    def __init__(self, k = 5):
        self.k = k

    def analyze(self, series) -> list:
        messages = []
        mean = series.mean
        std = series.stddev

        if mean is None or std is None or std == 0:
            return []

        for ts, val in zip(series.timestamps, series.values):
            if np.isnan(val):
                continue
            distance = abs(val - mean)
            if distance > self.k * std:
                messages.append(
                    f"Outlier at {ts}: value {val} deviates more than {self.k} stddevs from mean {mean:.2f}"
                )
        return messages

# detects sequences of at least 3 consecutive zeroes or missing values (NaN) in Timeseries
# helps to detect data gaps, sensor failures or readings iterrupted
# each sequence is reported with its time range and length
class ZeroSpikeDetector(SeriesValidator):
    # no need for init, because there are no parameters to set/remember
    def analyze(self, series) -> list:
        messages = []
        count = 0
        i = 0

        while i < len(series.values):
            val = series.values[i]
            if np.isnan(val) or val == 0:
                count += 1
                if count >= 3:
                    ts_start = series.timestamps[i - count + 1]
                    ts_end = series.timestamps[i]
                    messages.append(f"Zero/missing spike from {ts_start} to {ts_end} ({count} values)")
            else:
                count = 0
            i += 1

        return messages
    

# detects values that exceed a given threshold, spotting critical peaks or limit violations
class ThresholdDetector(SeriesValidator):
    def __init__(self, threshold):
        self.threshold = threshold

    def analyze(self, series) -> list:
        messages = []
        for ts, val in zip(series.timestamps, series.values):
            if not np.isnan(val) and val > self.threshold:
                messages.append(f"Threshold exceeded at {ts}: value {val} > {self.threshold}")
        return messages


# combines multiple validators into a single one using OR or AND logic
class CompositeValidator(SeriesValidator):
    def __init__(self, validators, mode):
        if mode not in ('OR', 'AND'):
            raise ValueError("mode must be 'OR' or 'AND'")
        self.validators = validators
        self.mode = mode

    def analyze(self, series) -> list:
        all_messages = []
        all_results = []

        for validator in self.validators:
            result = validator.analyze(series)
            all_results.append(result)
            all_messages.extend(result)

        if self.mode == 'OR':
            if any(all_results):
                # avoiding duplicates
                return list(set(all_messages))  
            else:
                return []

        elif self.mode == 'AND':
            if all(all_results):
                return list(set(all_messages))
            else:
                return []




def report_anomalies(series, validator, print_output = True, target_list = None):
    """
    Analyze a series using the given validator and either print or collect messages.

    :param series: TimeSeries object to analyze
    :param validator: a SeriesValidator (e.g. OutlierDetector)
    :param print_output: if True, prints messages to stdout
    :param target_list: if provided, appends messages to this list instead of printing
    """
    messages = validator.analyze(series)

    if print_output:
        print(f"[{validator.__class__.__name__}]")
        if messages:
            for msg in messages:
                print(" -", msg)
        else:
            print(" No anomalies detected.")
    elif target_list is not None:
        target_list.extend(messages)



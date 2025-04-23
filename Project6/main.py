from measurements import Measurements
from SeriesValidators.series_validator import OutlierDetector, ZeroSpikeDetector, ThresholdDetector, SimpleReporter
from timeseries import TimeSeries
from datetime import datetime

def test_measurements():
    folder = "measurements"
    m = Measurements(folder)

    validators = [
        OutlierDetector(k=30),
        #ZeroSpikeDetector(),
        ThresholdDetector(threshold=700)
    ]

    anomalies = m.detect_all_anomalies(validators, preload=True)

    with open("anomalies_report.txt", "w", encoding="utf-8") as f:
        f.write("--- Anomaly Report ---\n")
        for key, messages in anomalies.items():
            f.write(f"\n[{key}]\n")
            for msg in messages:
                f.write(f" - {msg}\n")

def test_duck_typing():   
    folder = "measurements"
    m = Measurements(folder)

    example_series = TimeSeries(
            compound="NO2",
            station_code="AB123",
            averaging_time="1g",
            timestamps=[datetime(2023, 1, 1, h) for h in range(5)],
            values=[10, 20, 15, 14, 13],
            unit="ug/m3"
        )
    
    analyzers = [
        OutlierDetector(k=2),
        ZeroSpikeDetector(),
        ThresholdDetector(threshold=18),
        # doesnt inherit from SeriesValidator but has analyze() method
        SimpleReporter()  
    ]

    # use every analyzer without checking type – this is duck typing
    for analyzer in analyzers:
        print(f"[{analyzer.__class__.__name__}]")
        results = analyzer.analyze(example_series)
        for line in results:
            print(" -", line)
        print()

def main():
    #test_measurements()
    test_duck_typing()

if __name__ == "__main__":
    main()
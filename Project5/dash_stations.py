import csv
import re
from pathlib import Path

# returns list of stations having at least 1 dash in "Nazwa stacji"
def find_stations_with_dash(filepath: Path) -> list:
    # matches any dash surrounded by optional whitespace
    pattern = re.compile(r"\s*[-–]\s*")

    results = []
    with filepath.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        # going through every station, every row is dict
        for row in reader:
            # returns value for key "Nazwa stacji"
            name = row.get("Nazwa stacji")
            # safety: if value doesnt exist dont add it to list
            if pattern.search(name) and name:
                results.append(name)

    return results


if __name__ == "__main__":
    path = Path("stacje.csv")

    stations_with_dash = find_stations_with_dash(path)

    for name in stations_with_dash:
        print(name)
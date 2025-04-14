import csv
import re
from pathlib import Path

# returns list of tuples (latitude, longitude) decimal number with 6 digit precision 
def extract_coordinates(filepath: Path) -> list:

    # \d+ one or more digits before the dot, \. – dot, \d{6} exactly 6 digits after the dot, $ end
    pattern = re.compile(r"^\d+\.\d{6}$")
    coordinates = []

    with filepath.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        # going through every station, every row is dict
        for row in reader:
            # return values of this fields
            lat = row.get("WGS84 φ N", "")
            lon = row.get("WGS84 λ E", "")

            if pattern.fullmatch(lat) and pattern.fullmatch(lon):
                coordinates.append((lat, lon))
    return coordinates


if __name__ == "__main__":
    path = Path("stacje.csv")

    coordinates = extract_coordinates(path)
    
    for lat, lon in coordinates:
        print(f"{lat}, {lon}")  

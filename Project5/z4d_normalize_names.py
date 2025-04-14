import csv
import unicodedata
from pathlib import Path

#returns station names replacing space with "_" and removing polish chars
def normalize_station_names(filepath: Path) -> list:
    normalized_names = []

    with filepath.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        # going through every station, every row is dict
        for row in reader:
            # returns value for key "Nazwa stacji"
            name = row.get("Nazwa stacji", "")
            name = name.replace(" ", "_")
            # removing polish chars
            name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
            normalized_names.append(name)

    return normalized_names


if __name__ == "__main__":
    path = Path("stacje.csv")

    new_names = normalize_station_names(path)

    for name in new_names:
        print(name)
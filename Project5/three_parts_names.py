import csv
import re
from pathlib import Path


def find_three_part_locations(filepath: Path) -> list:
    result = []
    # exactly 2 dashes: [^-]* any chars not "-", 
    pattern = re.compile(r"^[^-]*-[^-]*-[^-]*$")  

    with filepath.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        # going through every station, every row is dict
        for row in reader:
            # returns value for key "Nazwa stacji"
            name = row.get("Nazwa stacji")
            if pattern.match(name):
                result.append(name)

    return result


if __name__ == "__main__":
    path = Path("stacje.csv")

    three_part_locations = find_three_part_locations(path)

    for name in three_part_locations:
        print(name)

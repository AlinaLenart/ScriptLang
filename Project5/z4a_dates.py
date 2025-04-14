import csv
import re
from pathlib import Path

# returns list of dates in RRRR-MM-DD format from "Data uruchomienia" and "Data zamknięcia"
def extract_dates_from_file(filepath: Path) -> list[str]:

    # \d{4} precisely 4 digits, \d{2} precisiely 2 digits
    pattern = re.compile(r"\d{4}-\d{2}-\d{2}")
    dates = []

    with filepath.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        # going through every station, every row is dict
        for row in reader:
            # searching for field where dict key is "Data ..."
            for field in ["Data uruchomienia", "Data zamknięcia"]:
                # return value of this field
                value = row.get(field)
                # safety: if value doesnt exist dont add it to list
                if pattern.fullmatch(value) and value:
                    dates.append(value)

    return dates


if __name__ == "__main__":
    path = Path("stacje.csv")

    dates = extract_dates_from_file(path)
    
    for date in dates:
        print(date)
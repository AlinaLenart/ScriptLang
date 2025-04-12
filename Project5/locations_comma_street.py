import csv
import re
from pathlib import Path

# returns list of station names with comma and al. or ul.
def find_locations_with_comma_and_street(filepath: Path) -> list:
    result = []

    # , comma, .* any chars, \b end of word (ul./al. is separate), then ul. or al. and after | make it in another direction 
    pattern = re.compile(r",.*\b(ul\.|al\.)|\b(ul\.|al\.).*,", re.IGNORECASE)

    with filepath.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        # going through every station, every row is dict
        for row in reader:
            name = row.get("Nazwa stacji", "")
            if pattern.search(name):
                result.append(name)

    return result


if __name__ == "__main__":
    path = Path("stacje.csv")

    matches = find_locations_with_comma_and_street(path)

    for name in matches:
        print(name)  
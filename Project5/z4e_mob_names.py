import csv
import re
from pathlib import Path

# returns list of stations having not compatible name station with station type (about MOB - mobile stations)
# works on both sides, checks if mob = mobilna
def find_mob_mismatches(filepath: Path) -> list:
    mismatches = []

    with filepath.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        # going through every station, every row is dict
        for row in reader:
            # returns values for key "Kod stacji" and "Rodzaj stacji"
            code = row.get("Kod stacji", "").strip()
            kind = row.get("Rodzaj stacji", "").strip()

            # gets booleans about mob ending and kind "mobilna"
            code_ends_mob = bool(re.search(r"mob$", code, re.IGNORECASE))
            kind_mobilna = (kind.lower() == "mobilna")

            # if end with MOB and not mobilna or mobilna but doesnt end with MOB
            if code_ends_mob != kind_mobilna:
                mismatches.append(f"{code} – {kind}")

    return mismatches


if __name__ == "__main__":
    path = Path("stacje.csv")

    invalid = find_mob_mismatches(path)

    for code in invalid:
        print(code)
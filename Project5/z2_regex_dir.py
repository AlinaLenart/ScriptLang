import re
from pathlib import Path

# search csv files in directory and group them by filename pattern
def group_measurement_files_by_key(path: Path) -> dict:
    result = {}
    # regex: <year>_<measurement>_<frequency>.csv, dividing into subgroups 
    # ^ beginning of line, (\d{4}) precisely 4 digits, (.+?) any char at least one, match non-greedy (lazy, match as few char as possible if matching overall pattern)
    pattern = re.compile(r"^(\d{4})_(.+?)_(.+?)\.csv$")

    for file_path in path.iterdir():
        if not file_path.is_file():
            continue

        match = pattern.match(file_path.name)
        if match:
            year, compound, frequency = match.groups()
            result[(year, compound, frequency)] = file_path

    return result

if __name__ == "__main__":
    dir = Path("measurements")  
    grouped_files = group_measurement_files_by_key(dir)

    for key, filepath in grouped_files.items():
        print(f"{key}: {filepath}")

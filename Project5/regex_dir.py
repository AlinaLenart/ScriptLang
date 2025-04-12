import re
from pathlib import Path

def group_measurement_files_by_key(path: Path):
    """
    Przeszukuje pliki w katalogu `path` i grupuje je według wzorca nazwy pliku:
    <rok>_<wielkość>_<częstotliwość>.csv

    Argumenty:
        path (str): ścieżka do katalogu (np. 'measurements')

    Zwraca:
        dict: {(rok, wielkość, częstotliwość): pełna_ścieżka_do_pliku}
    """
    result = {}
    # regex: <year>_<measurement>_<frequency>.csv  
    # ^ beginning of line, (\d{4}) precisely 4 digits, (.+?) any char at least one, match non-greedy (lazy, match as few char as possible if matching overall pattern)
    pattern = re.compile(r"^(\d{4})_(.+?)_(.+?)\.csv$")

    for file in path.iterdir():
        if not file.is_file():
            continue

        match = pattern.match(file.name)
        if match:
            rok, wielkosc, czestotliwosc = match.groups()
            result[(rok, wielkosc, czestotliwosc)] = file

    return result

if __name__ == "__main__":
    katalog = Path("measurements")  
    grouped_files = group_measurement_files_by_key(katalog)

    for key, filepath in grouped_files.items():
        print(f"{key}: {filepath}")

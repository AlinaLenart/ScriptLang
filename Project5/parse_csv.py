import csv
import os
import re
import json

# returns dict of station codes, with dict value: info dict, measurements list
def load_stations(path):
    stations = {}

    with open(path, newline='', encoding='utf-8') as f:
        # reads file and returns every line as dict
        reader = csv.DictReader(f)
        for row in reader:
            station_code = row["Kod stacji"]
            stations[station_code] = {
                "info": row,
                # future list of measurements group
                "measurements": []  
            }
    return stations

def parse_filename(filename):
    match = re.match(r"(\d{4})_(.+?)_(.+?)\.csv", filename)
    if match:
        year, compound, frequency = match.groups()
        return int(year), compound, frequency
    return None

def load_measurements_grouped(stations, measurements_dir):
    for fname in os.listdir(measurements_dir):
        if not fname.endswith('.csv'):
            continue
        parsed = parse_filename(fname)
        if not parsed:
            continue

        rok, wielkosc, czestotliwosc = parsed
        path = os.path.join(measurements_dir, fname)

        with open(path, newline='', encoding='utf-8') as f:
            lines = list(csv.reader(f))
            if len(lines) < 4:
                continue

            station_codes = lines[1][1:]
            for row in lines[3:]:
                if not row or len(row) < 2:
                    continue
                nr = row[0]
                values = row[1:]

                for i, val in enumerate(values):
                    kod_stacji = station_codes[i].strip()
                    if kod_stacji not in stations or val.strip() == "":
                        continue

                    try:
                        wartosc = float(val.replace(",", "."))
                    except ValueError:
                        continue

                    # Znajdź istniejącą grupę dla (rok, wielkosc, czestotliwosc) lub stwórz nową
                    station_data = stations[kod_stacji]
                    grupa = next(
                        (g for g in station_data["measurements"]
                         if g["rok"] == rok and g["wielkosc"] == wielkosc and g["czestotliwosc"] == czestotliwosc),
                        None
                    )
                    if not grupa:
                        grupa = {
                            "rok": rok,
                            "wielkosc": wielkosc,
                            "czestotliwosc": czestotliwosc,
                            "pomiary": []
                        }
                        station_data["measurements"].append(grupa)

                    grupa["pomiary"].append({
                        "nr": nr,
                        "wartosc": wartosc
                    })
    return stations

def main():
    sciezka_stacji = '/Users/al/Code/Uni/ScriptLang/Project5/stacje.csv'
    sciezka_pomiarow = '/Users/al/Code/Uni/ScriptLang/Project5/measurements/'
    sciezka_wyjscia = '/Users/al/Code/Uni/ScriptLang/Project5/merged_data.json'

    stations = load_stations(sciezka_stacji)
    merged_data = load_measurements_grouped(stations, sciezka_pomiarow)


    with open(sciezka_wyjscia, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)

    # Przykład użycia
    for kod, dane in merged_data.items():
        print(f"Stacja: {dane['info']['Kod stacji']}")
        print(f"Liczba pomiarów: {len(dane['measurements'])}")

if __name__ == "__main__":
    main()  
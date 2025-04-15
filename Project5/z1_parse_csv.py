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

# parses filename to extract: year compound and frequency
def parse_filename(filename):
    # regex: <year>_<measurement>_<frequency>.csv  
    # ^ beginning of line, (\d{4}) precisely 4 digits, (.+?) any char at least one, match non-greedy (lazy, match as few char as possible if matching overall pattern) 
    match = re.match(r"(\d{4})_(.+?)_(.+?)\.csv", filename)
    if match:
        year, compound, frequency = match.groups()
        return int(year), compound, frequency
    return None

# loads measurements from csv files, groups them by year, compound and frequency
# and adds them to the corresponding station in the stations dict
def load_measurements_grouped(stations, measurements_dir):
    for fname in os.listdir(measurements_dir):
        if not fname.endswith('.csv'):
            continue
        parsed = parse_filename(fname)
        if not parsed:
            continue

        year, compound, frequency = parsed
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
                    station_code = station_codes[i].strip()
                    if station_code not in stations or val.strip() == "":
                        continue

                    # replace , with . to make float conversion possible (in task, csv clean)
                    try:
                        value = float(val.replace(",", "."))
                    except ValueError:
                        continue


                    station_data = stations[station_code]
                    group = next(
                        (g for g in station_data["measurements"]
                         if g["rok"] == year and g["wielkosc"] == compound and g["czestotliwosc"] == frequency),
                        None
                    )
                    
                    if not group:
                        group = {
                            "rok": year,
                            "wielkosc": compound,
                            "czestotliwosc": frequency,
                            "pomiary": []
                        }
                        station_data["measurements"].append(group)

                    group["pomiary"].append({
                        "nr": nr,
                        "wartosc": value
                    })
    return stations

def main():
    station_path = '/Users/al/Code/Uni/ScriptLang/Project5/stacje.csv'
    measurements_path = '/Users/al/Code/Uni/ScriptLang/Project5/measurements/'
    output_path = '/Users/al/Code/Uni/ScriptLang/Project5/merged_data.json'

    stations = load_stations(station_path)
    merged_data = load_measurements_grouped(stations, measurements_path)


    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)

    # print the number of measurements files for each station
    for kod, dane in merged_data.items():
        print(f"Station code: {dane['info']['Kod stacji']}")
        print(f"Amount of files mention: {len(dane['measurements'])}")

if __name__ == "__main__":
    main()  
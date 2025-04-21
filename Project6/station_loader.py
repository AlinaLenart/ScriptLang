import csv
from station import Station  

def load_stations_from_csv(filepath):
    stations = []

    with open(filepath, encoding='utf-8') as f:
        reader = csv.reader(f)
        # skip header
        header = next(reader)  

        for row in reader:
            station = Station(
                id=row[0],
                stat_code=row[1],
                global_code=row[2],
                name=row[3],
                old_code=row[4],
                start_date=row[5],
                end_date=row[6],
                type=row[7],
                region=row[8],
                kind=row[9],
                voivo=row[10],
                city=row[11],
                address=row[12],
                N_coor=row[13],
                E_coor=row[14]
            )
            stations.append(station)
    
    return stations

if __name__ == "__main__":
    stations = load_stations_from_csv("stacje.csv")

    print(f"__str__:")
    print(stations[0])        # __str__
    print(f"\n__repr__:")
    print(repr(stations[0])) 
    print(f"\n__eq__: (stations[0] == stations[1])")
    print(stations[0] == stations[1])  # __eq__
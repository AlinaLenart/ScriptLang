import argparse
import sys
from pathlib import Path
import re
from random_station import find_random_station, find_measurement_file, get_station_measurements

# check if given data is correct, then transfer into MM/DD/YYYY like in measurements csv files
def validate_date(date_str: str) -> str:
    # taking date in YYYY-MM-DD format
    pattern = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")
    match = pattern.fullmatch(date_str)

    # exit if given date is incorrect
    if not match:
        print(f"Invalid date format: '{date_str}' use YYYY-MM-DD")
        sys.exit(1)

    year, month, day = match.groups()
    # taking last 2 digits of the year
    year_short = year[2:] 

    return f"{month}/{day}/{year_short} 12:00"


# random subcommand
def subcommand_random(args):
    print(f"Compound : {args.c}, Frequency: {args.f}, Time: {args.s} to {args.e}")
    name, address = find_random_station(args.c, args.f, args.s, args.e)
    print(f"After random search: \nName: {name} Address: {address}")

# stats subcommand
def subcommand_stats(args):
    print(f"Station kod: {args.sc}, Compound: {args.c}, Frequency: {args.f}, Time: {args.start} to {args.end}")
    
    # Znajdź plik z pomiarami
    measurement_file = find_measurement_file(args.metric, args.frequency, Path("measurements"))
    if not measurement_file:
        print(f"Nie znaleziono pliku z pomiarami dla {args.metric} {args.frequency}")
        return
    
    # Wczytaj dane dla wybranej stacji
    measurements = get_station_measurements(
        measurement_file, 
        args.station, 
        args.start, 
        args.end
    )
    
    if not measurements:
        print(f"Brak danych dla stacji {args.station} w podanym zakresie czasowym")
        return
    
    # Oblicz statystyki
    avg = sum(measurements) / len(measurements)
    
    if len(measurements) > 1:
        variance = sum((x - avg) ** 2 for x in measurements) / (len(measurements) - 1)
        stdev = variance ** 0.5
    else:
        stdev = 0
    
    print("\nWyniki statystyczne:")
    print(f"Średnia: {avg:.2f}")
    print(f"Odchylenie standardowe: {stdev:.2f}")
    print(f"Liczba pomiarów: {len(measurements)}")

# default behaviour, without subcommand, pure reading parameters
def default_command(args):
    print(f"Compound : {args.c}, Frequency: {args.f}, Time: {args.s} to {args.e}")


def main():
    parser = argparse.ArgumentParser(description="Measurement CLI with optional subcommands")

    # Ogólne argumenty (działają z lub bez podkomend)
    parser.add_argument("--c", help="Measured compound, e.g. PM10")
    parser.add_argument("--f", help="Measurement frequency, e.g. 24g")
    parser.add_argument("--s", type=validate_date, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--e", type=validate_date, help="End date (YYYY-MM-DD)")

    subparsers = parser.add_subparsers(dest="subcommand")

    # Subcommand: losowa
    parser_losowa = subparsers.add_parser("rand", help="Show a random station with filter info")
    parser_losowa.add_argument("--c", required=True, help="Measured compound, e.g. PM10")
    parser_losowa.add_argument("--f", required=True, help="Measurement frequency, e.g. 24g")
    parser_losowa.add_argument("--s", required=True, type=validate_date, help="Start date (YYYY-MM-DD)")
    parser_losowa.add_argument("--e", required=True, type=validate_date, help="End date (YYYY-MM-DD)")
    parser_losowa.set_defaults(func=subcommand_random) 

    # Subcommand: statystyki
    parser_stat = subparsers.add_parser("stats", help="Calculate statistics for a station")
    parser_stat.add_argument("station", help="Station code, e.g. DsCzerStraza")
    parser_stat.add_argument("compound", help="Measured compound, e.g. PM10")
    parser_stat.add_argument("frequency", help="Measurement frequency, e.g. 24g")
    parser_stat.add_argument("start", type=validate_date, help="Start date (YYYY-MM-DD)")
    parser_stat.add_argument("end", type=validate_date, help="End date (YYYY-MM-DD)")
    parser_stat.set_defaults(func=subcommand_stats)

    args = parser.parse_args()

    # Jeśli użyto podkomendy – uruchom odpowiednią funkcję
    if hasattr(args, "func"):
        args.func(args)
    # Jeśli nie użyto podkomendy – ale podano dane główne
    elif args.m and args.f and args.s and args.e:
        run_default(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

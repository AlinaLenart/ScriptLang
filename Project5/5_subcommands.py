import argparse
import sys
import re
from random_station import find_random_station

def validate_date(date_str: str) -> str:
    pattern = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")
    match = pattern.fullmatch(date_str)

    if not match:
        print(f"Invalid date format: '{date_str}'. Use YYYY-MM-DD.")
        sys.exit(1)

    year, month, day = match.groups()
    year_short = year[2:]  # take last 2 digits of the year
    return f"{day}/{month}/{year_short} 12:00"

# --- Podkomenda: losowa stacja ---
def run_losowa(args):
    print("[DEBUG] Podkomenda: losowa")
    print(f"Metric: {args.m}, Frequency: {args.f}")
    print(f"Date range: {args.s} to {args.e}")
    nazwa, adres = find_random_station(args.m, args.f, args.s, args.e)
    print(nazwa)
    print(adres)

# --- Podkomenda: statystyki ---
def run_statystyki(args):
    print("[DEBUG] Podkomenda: statystyki")
    print(f"Station: {args.station}")
    print(f"Metric: {args.metric}, Frequency: {args.frequency}")
    print(f"Date range: {args.start} to {args.end}")
    print("Example result: Mean: 12.3, Std dev: 3.1")

# --- Domyślne zachowanie bez podkomendy ---
def run_default(args):
    print("[DEBUG] Tryb domyślny (bez podkomendy)")
    print(f"Metric: {args.m}, Frequency: {args.f}")
    print(f"Date range: {args.s} to {args.e}")
    print("Default behavior executed.")

# --- Główna funkcja ---
def main():
    parser = argparse.ArgumentParser(description="Measurement CLI with optional subcommands")

    # Ogólne argumenty (działają z lub bez podkomend)
    parser.add_argument("--m", help="Measured metric, e.g. PM10")
    parser.add_argument("--f", help="Measurement frequency, e.g. 24g")
    parser.add_argument("--s", type=validate_date, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--e", type=validate_date, help="End date (YYYY-MM-DD)")

    subparsers = parser.add_subparsers(dest="subcommand")

    # Subcommand: losowa
    parser_losowa = subparsers.add_parser("losowa", help="Show a random station")
    parser_losowa.add_argument("--m", required=True, help="Measured metric, e.g. PM10")
    parser_losowa.add_argument("--f", required=True, help="Measurement frequency, e.g. 24g")
    parser_losowa.add_argument("--s", required=True, type=validate_date, help="Start date (YYYY-MM-DD)")
    parser_losowa.add_argument("--e", required=True, type=validate_date, help="End date (YYYY-MM-DD)")
    parser_losowa.set_defaults(func=run_losowa) 

    # Subcommand: statystyki
    parser_stat = subparsers.add_parser("statystyki", help="Calculate statistics for a station")
    parser_stat.add_argument("station", help="Station code, e.g. DsCzerStraza")
    parser_stat.add_argument("metric", help="Measured metric, e.g. PM10")
    parser_stat.add_argument("frequency", help="Measurement frequency, e.g. 24g")
    parser_stat.add_argument("start", type=validate_date, help="Start date (YYYY-MM-DD)")
    parser_stat.add_argument("end", type=validate_date, help="End date (YYYY-MM-DD)")
    parser_stat.set_defaults(func=run_statystyki)

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

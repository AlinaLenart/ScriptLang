import argparse
import sys
import re
from z6_random_station import find_random_station, calculate_stats


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
    print(f"Compound : {args.compound}, Frequency: {args.frequency}, Time: {args.start} to {args.end}")
    find_random_station(args.compound, args.frequency, args.start, args.end)
   
# stats subcommand
def subcommand_stats(args):
    print(f"Station: {args.station}, Compound: {args.compound}, Frequency: {args.frequency}, Time: {args.start} to {args.end}")
    calculate_stats(args.station, args.compound, args.frequency, args.start, args.end)
   

# default behaviour, without subcommand, pure reading parameters
def default_command(args):
    print(f"Compound : {args.compound}, Frequency: {args.frequency}, Time: {args.start} to {args.end}")



def main():

    if len(sys.argv) > 1 and sys.argv[1] in ["rand", "stats"]:
        parser = argparse.ArgumentParser(description="Measurement CLI with subcommands")
        subparsers = parser.add_subparsers(dest="subcommand")

        # random subcomm
        parser_rand = subparsers.add_parser("rand", help="Show a random station with filter info")
        parser_rand.add_argument("compound", help="Measured compound, e.g. PM10")
        parser_rand.add_argument("frequency", help="Measurement frequency, e.g. 24g")
        parser_rand.add_argument("start", type=validate_date, help="Start date (YYYY-MM-DD)")
        parser_rand.add_argument("end", type=validate_date, help="End date (YYYY-MM-DD)")
        parser_rand.set_defaults(func=subcommand_random)

        # stats subcommand
        parser_stats = subparsers.add_parser("stats", help="Calculate statistics for given station")
        parser_stats.add_argument("station", help="Station code, e.g. DsCzerStraza")
        parser_stats.add_argument("compound", help="Measured compound, e.g. PM10")
        parser_stats.add_argument("frequency", help="Measurement frequency, e.g. 24g")
        parser_stats.add_argument("start", type=validate_date, help="Start date (YYYY-MM-DD)")
        parser_stats.add_argument("end", type=validate_date, help="End date (YYYY-MM-DD)")
        parser_stats.set_defaults(func=subcommand_stats)

        args = parser.parse_args()
        args.func(args)

    else:
        # default command
        parser = argparse.ArgumentParser(description="Default usage without subcommands")
        parser.add_argument("compound", help="Measured compound, e.g. PM10")
        parser.add_argument("frequency", help="Measurement frequency, e.g. 24g")
        parser.add_argument("start", type=validate_date, help="Start date (YYYY-MM-DD)")
        parser.add_argument("end", type=validate_date, help="End date (YYYY-MM-DD)")
        args = parser.parse_args()
        default_command(args)

if __name__ == "__main__":
    main()

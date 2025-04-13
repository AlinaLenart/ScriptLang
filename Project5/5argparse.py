import argparse
import sys
import re

def validate_date(date_str: str) -> str:

    pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    if not pattern.fullmatch(date_str):
        print(f"Invalid date format: '{date_str}'. Should be: RRRR-MM-DD.")
        sys.exit(1)

    return date_str  
    
def main():
    parser = argparse.ArgumentParser(description="Measurement CLI")

    # positional arguments – arguments that are required and identified by their position in the command line
    parser.add_argument("metric", help="Measured value, e.g. PM2.5, PM10, NO")
    parser.add_argument("frequency", help="Measurement frequency, e.g. 1g, 24g")
    parser.add_argument("start", type=validate_date, help="Start date (format: YYYY-MM-DD)")
    parser.add_argument("end", type=validate_date, help="End date (format: YYYY-MM-DD)")
    args = parser.parse_args()

    print(f" Parameters: {args.metric}, {args.frequency}, Dates: {args.start}, {args.end}")


if __name__ == "__main__":
    main()
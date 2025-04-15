import csv
import re
from pathlib import Path

# returns list of addresses of stations in a given city as 4 elements tuple
def get_addresses(path: Path, city: str) -> list[tuple]:
    results = []

    with path.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Miejscowość"].strip().lower() != city.strip().lower():
                continue

            woj = row["Województwo"].strip()
            city = row["Miejscowość"].strip()
            address = row["Adres"].strip()

            
            # regex: fe. "ul. Norwida 3" => "Norwida, 3", divided into 2 groups: street and number(optional)
            # ul. is optional, [..] any chars in brackets, \w letters, digits, additional polish letters, wspace, comma, dot, hyphen
            # +? lazy match
            # \s+ at least one space, \d+ at least one digit and [A-Za-z]? optional letter
            match = re.match(r"(?:ul\.\s*)?([\wąćęłńóśźżĄĆĘŁŃÓŚŹŻ ,.\-]+?)(?:\s+(\d+[A-Za-z]?))?$", address)
            if match:
                street = match.group(1).strip()
                number = match.group(2)
                # number is optional
                if number:
                    results.append((woj, city, street, number))
                else:
                    results.append((woj, city, street))
    return results

def main():
    file = Path("stacje.csv")
    city = "Głogów"

    adresses = get_addresses(file, city)

    print(f"Station addresses in: {city}")
    for a in adresses:
        print(a)


if __name__ == "__main__":
    main()

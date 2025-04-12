import csv
import re
from pathlib import Path

def get_addresses(path: Path, city: str):
    """
    Zwraca listę adresów stacji w danym mieście jako czwórki:
    (województwo, miasto, ulica, numer) — jeśli brak numeru, tylko 3 pola.

    Argumenty:
        path (Path): ścieżka do pliku CSV z metadanymi
        city (str): nazwa miejscowości, np. "Głogów"

    Zwraca:
        list[tuple]: lista krotek z adresami
    """
    results = []
    with path.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Miejscowość"].strip().lower() != city.strip().lower():
                continue

            woj = row["Województwo"].strip()
            miasto = row["Miejscowość"].strip()
            adres = row["Adres"].strip()

            # Wyrażenie regularne: np. "ul. Norwida 3", "ul. Stroma", "Wita Stwosza 2", itp.
            match = re.match(r"(?:ul\.\s*)?([\wąćęłńóśźżĄĆĘŁŃÓŚŹŻ ,.\-]+?)(?:\s+(\d+[A-Za-z]?))?$", adres)
            if match:
                ulica = match.group(1).strip()
                numer = match.group(2)
                if numer:
                    results.append((woj, miasto, ulica, numer))
                else:
                    results.append((woj, miasto, ulica))
    return results

if __name__ == "__main__":
    plik = Path("stacje.csv")
    miejscowosc = "Głogów"

    adresy = get_addresses(plik, miejscowosc)

    print(f"Adresy stacji w miejscowości: {miejscowosc}")
    for a in adresy:
        print(a)

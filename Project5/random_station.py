import csv
import random
from pathlib import Path
from datetime import datetime

def find_random_station(wielkosc: str, czestotliwosc: str, poczatek: str, koniec: str, 
                       measurements_dir: Path = Path("measurements"),
                       stations_file: Path = Path("stacje.csv")) -> tuple:
    """
    Znajduje losową stację, która mierzy daną wielkość w zadanym przedziale czasowym.
    """
    # Znajdź odpowiedni plik z pomiarami
    measurement_file = find_measurement_file(wielkosc, czestotliwosc, measurements_dir)
    if not measurement_file:
        print(f"Nie znaleziono pliku dla {wielkosc} {czestotliwosc}")
        return None, None
    
    # Wczytaj dane pomiarowe
    station_codes = get_stations_in_time_range(measurement_file, poczatek, koniec)
    if not station_codes:
        print(f"Nie znaleziono stacji z danymi w podanym zakresie dat")
        return None, None
    
    # Wybierz losową stację
    random_station_code = random.choice(station_codes)
    # print(f"Wybrano stację o kodzie: {random_station_code}")
    
    # Znajdź metadane stacji
    return get_station_metadata(random_station_code, stations_file)

def find_measurement_file(wielkosc: str, czestotliwosc: str, measurements_dir: Path) -> Path:
    """Znajduje plik CSV z pomiarami dla danej wielkości i częstotliwości."""
    for file in measurements_dir.glob(f"*_{wielkosc}_{czestotliwosc}.csv"):
        return file
    return None

def get_stations_in_time_range(measurement_file: Path, start_date: str, end_date: str) -> list:
    """
    Zwraca listę kodów stacji, które mają dane w zadanym przedziale czasowym.
    Przyjmuje daty w formacie DD/MM/YY HH:MM (jak w plikach CSV)
    """
    valid_stations = set()
    
    with open(measurement_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        
        # Pobierz nagłówki kolumn (kody stacji)
        headers = next(reader)
        
        # Pomijamy kolejne 4 wiersze (Nr, Wskaźnik, Czas uśredniania, Jednostka, Kod stanowiska)
        for _ in range(4):
            next(reader)
        
        # Teraz odczytaj właściwe kody stacji z wiersza "Kod stacji"
        station_codes_row = next(reader)
        station_codes = [code.split('-')[0] for code in station_codes_row[1:]]  # Pomijamy pierwszy element (data)
        
        for row in reader:
            if not row:  # Pomiń puste wiersze
                continue
                
            try:
                date_str = row[0].strip()
                if not date_str:
                    continue
                    
                # Sprawdź czy data mieści się w zakresie
                if start_date <= date_str <= end_date:
                    # Sprawdź, które stacje mają dane w tym wierszu
                    for i, value in enumerate(row[1:]):  # Pomijamy kolumnę z datą
                        if value.strip():  # Jeśli wartość nie jest pusta
                            valid_stations.add(station_codes[i])
            except (ValueError, IndexError) as e:
                print(f"Błąd przetwarzania wiersza: {e}")
                continue
    
    return list(valid_stations)

def get_station_metadata(station_code: str, stations_file: Path) -> tuple:
    """
    Pobiera metadane stacji na podstawie kodu z pliku stacje.csv.
    """
    with open(stations_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            if row['Kod stacji'] == station_code:
                # Budujemy adres z dostępnych pól
                wojewodztwo = row.get('Województwo', '')
                miejscowosc = row.get('Miejscowość', '')
                adres = row.get('Adres', '')
                
                # Jeśli w polu Adres jest "ul." to zostawiamy, w przeciwnym razie dodajemy "ul."
                if adres and not adres.startswith('ul.') and not adres.startswith('al.'):
                    adres = f"ul. {adres}" if adres else ""
                
                # Składamy pełny adres
                full_address = ", ".join(filter(None, [wojewodztwo, miejscowosc, adres]))
                
                return row['Nazwa stacji'], full_address
    
    print(f"Nie znaleziono metadanych dla stacji: {station_code}")
    return None, None

def get_station_measurements(measurement_file: Path, station_code: str, 
                           start_date: str, end_date: str) -> list[float]:
    """
    Zwraca listę pomiarów dla danej stacji w zadanym przedziale czasowym.
    """
    measurements = []
    station_index = None
    
    with open(measurement_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        
        # Znajdź indeks kolumny dla danej stacji
        headers = next(reader)
        for _ in range(4):  # Pomijamy kolejne 4 wiersze
            next(reader)
        
        # Wiersz z kodami stacji
        station_codes_row = next(reader)
        for i, code in enumerate(station_codes_row[1:]):  # Pomijamy pierwszą kolumnę (datę)
            if code.startswith(f"{station_code}-"):
                station_index = i + 1  # +1 bo pomijamy pierwszą kolumnę
                break
                
        if station_index is None:
            print(f"Nie znaleziono stacji {station_code} w pliku {measurement_file}")
            return []
        
        # Przetwarzaj dane
        for row in reader:
            if not row:
                continue
                
            try:
                date_str = row[0].strip()
                if not date_str:
                    continue
                    
                # Sprawdź czy data mieści się w zakresie
                if start_date <= date_str <= end_date:
                    value = row[station_index].strip()
                    if value:  # Jeśli wartość nie jest pusta
                        measurements.append(float(value.replace(',', '.')))  # Obsługa formatu polskiego
            except (ValueError, IndexError) as e:
                print(f"Błąd przetwarzania wiersza: {e}")
                continue
    
    return measurements
import reader
import ipaddress

def get_entries_by_addr(log: list, addr) -> list:
    results = []
    is_ip_addr = False

    try:
        ipaddress.ip_address(addr)
        is_ip_addr = True
    except ValueError:
        pass  

    for entry in log:
        try:
            if is_ip_addr:
                if entry[2] == addr:  # orig_h
                    results.append(entry)
            else:
                if entry[8] == addr:  # host (domena)
                    results.append(entry)
        except IndexError:
            continue  # pomiń błędnie sformatowane wpisy

    return results

def get_entries_by_code(log: list, status_code: int) -> list:

    if not (100 <= status_code <= 599):
        raise ValueError(f"Nieprawidłowy kod statusu HTTP: {status_code}")

    filtered = []

    for entry in log:
        try:
            if isinstance(entry, tuple) and entry[-1] == status_code:
                filtered.append(entry)
        except IndexError:
            continue  # pomiń błędnie sformatowane wpisy

    return filtered

def get_failed_reads(log: list, combine: bool = False):
    """
    Zwraca wpisy z błędami HTTP (4xx i 5xx).
    
    Parametry:
    - log: lista krotek (każda kończy się kodem statusu HTTP),
    - combine: jeśli True, zwraca jedną listę z obu typów błędów,
               jeśli False, zwraca osobno (lista_4xx, lista_5xx).
    """
    errors_4xx = []
    errors_5xx = []

    for entry in log:
        try:
            if not isinstance(entry, tuple):
                continue
            status = entry[-1]
            if 400 <= status <= 499:
                errors_4xx.append(entry)
            elif 500 <= status <= 599:
                errors_5xx.append(entry)
        except (IndexError, TypeError):
            continue  # Pomijamy błędne wpisy

    if combine:
        return errors_4xx + errors_5xx
    else:
        return errors_4xx, errors_5xx

def get_entries_by_extension(log: list, extension: str) -> list:
    """
    Zwraca wpisy logów, które dotyczą żądań plików z danym rozszerzeniem (np. 'jpg', 'pdf').

    Parametry:
    - log: lista krotek z danymi (każda zawiera uri na pozycji 8)
    - extension: rozszerzenie pliku (bez kropki)

    Zwraca:
    - listę krotek, gdzie uri kończy się na podane rozszerzenie (np. '.jpg')
    """
    if not isinstance(extension, str) or not extension:
        raise ValueError("Podaj prawidłowe rozszerzenie pliku jako ciąg znaków.")

    filtered = []

    for entry in log:
        try:
            uri = entry[8]  # uri znajduje się w pozycji 8 krotki
            if isinstance(uri, str) and uri.lower().endswith(f".{extension.lower()}"):
                filtered.append(entry)
        except IndexError:
            continue  # pomiń błędne wpisy

    return filtered


if __name__ == "__main__":
    logs = reader.read_log()
    


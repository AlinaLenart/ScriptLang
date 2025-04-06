#!/usr/bin/env python3
import sys
import os

def parse_arguments():
    """
    Parsuje argumenty wiersza poleceń.
    Rozpoznaje:
      --lines=n -> określa liczbę linii do wypisania (domyślnie 10)
      [plik]   -> ścieżka do pliku; jeśli podana, dane ze STDIN są ignorowane.
    """
    lines_to_print = 10
    file_path = None

    for arg in sys.argv[1:]:
        if arg.startswith('--lines='):
            try:
                lines_to_print = int(arg.split('=', 1)[1])
            except ValueError:
                print("Niepoprawna wartość dla --lines. Używam domyślnej wartości 10.", file=sys.stderr)
                lines_to_print = 10
        elif not arg.startswith('-'):
            file_path = arg
    return lines_to_print, file_path

def tail_lines(lines, count):
    """
    Zwraca ostatnie 'count' linii z listy 'lines'.
    Jeśli liczba linii jest mniejsza niż count, zwraca wszystkie linie.
    """
    if len(lines) <= count:
        return lines
    return lines[-count:]

def read_input(file_path = None):
    """
    Odczytuje linie wejściowe.
    Jeśli file_path jest podany, czyta z pliku.
    W przeciwnym razie próbuje odczytać dane ze standardowego wejścia (STDIN).
    """
    lines = []
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            sys.exit(f"Błąd podczas otwierania pliku '{file_path}': {e}")
    elif not sys.stdin.isatty():
        lines = sys.stdin.readlines()
    else:
        sys.exit("Brak danych wejściowych. Podaj plik jako argument lub przekieruj dane przez STDIN.")
    return [line.rstrip('\n') for line in lines]

def main():
    # Blok testowy modułu tail.py.
    # Umożliwia uruchomienie modułu niezależnie dla celów testowania.
    count, file_path = parse_arguments()
    input_lines = read_input(file_path)
    result = tail_lines(input_lines, count)
    for line in result:
        print(line)

if __name__ == "__main__":
   main()

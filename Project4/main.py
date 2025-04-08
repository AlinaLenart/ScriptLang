#!/usr/bin/env python3
import sys
import os
import json
import subprocess
from aggregator import aggregate_statistics

def main():
    if len(sys.argv) < 2:
        sys.exit("Użycie: python main.py <ścieżka_do_katalogu>")
    
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        sys.exit(f"{directory} nie jest katalogiem.")
    
    results = []
    # Przetwarzamy tylko pliki z rozszerzeniem .txt (plik tekstowy)
    for filename in os.listdir(directory):
        if not filename.lower().endswith('.txt'):
            continue
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            try:
                # Uruchamiamy analyze_file.py, przekazując ścieżkę do pliku przez STDIN.
                proc = subprocess.run(
                    [sys.executable, "analyze_file.py"],
                    input=file_path,
                    text=True,
                    capture_output=True,
                    check=True
                )
                result = json.loads(proc.stdout)
                results.append(result)
            except subprocess.CalledProcessError as e:
                print(f"Błąd przy analizie pliku {file_path}: {e}", file=sys.stderr)
            except json.JSONDecodeError as e:
                print(f"Błąd dekodowania JSON dla pliku {file_path}: {e}", file=sys.stderr)
    
    if not results:
        sys.exit("Brak przetworzonych plików.")
    
    aggregated = aggregate_statistics(results)
    print(json.dumps(aggregated, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

import os
import sys

def get_path_directories():
    """
    Pobiera zmienną środowiskową PATH i dzieli ją na listę katalogów.
    """
    path_var = os.environ.get("PATH", "")
    directories = path_var.split(os.pathsep)
    return directories

def list_executables(directory):
    """
    Zwraca listę plików wykonywalnych w danym katalogu.
    Na Windows sprawdzamy rozszerzenia (.exe, .bat, .cmd),
    a na systemach Unix-like wykorzystujemy os.access z os.X_OK.
    """
    executables = []
    try:
        for item in os.listdir(directory):
            full_path = os.path.join(directory, item)
            if os.path.isfile(full_path):
                if os.name == "nt":
                    ext = os.path.splitext(item)[1].lower()
                    if ext in [".exe", ".bat", ".cmd"]:
                        executables.append(item)
                else:
                    if os.access(full_path, os.X_OK):
                        executables.append(item)
    except Exception:
        # W przypadku błędów (np. brak dostępu) pomijamy dany katalog
        pass
    return executables

def display_path_directories(list_exec=False):
    """
    Wypisuje katalogi ze zmiennej PATH.
    
    Jeśli list_exec jest False, wypisuje tylko katalogi (każdy w osobnej linii).
    Jeśli list_exec jest True, dla każdego katalogu wypisuje także listę plików wykonywalnych.
    """
    directories = get_path_directories()
    if list_exec:
        for directory in directories:
            print(f"{directory}:")
            exec_files = list_executables(directory)
            if exec_files:
                for exe in exec_files:
                    print(f"  {exe}")
            else:
                print("  [Brak plików wykonywalnych]")
            print()  # pusty wiersz dla czytelności
    else:
        for directory in directories:
            print(directory)

def main():
    # Testowanie modułu. 
    # Użyj parametru -e lub --executables, aby wypisać także pliki wykonywalne.
    flag = False
    if len(sys.argv) > 1 and sys.argv[1] in ("-e", "--executables"):
        flag = True
    display_path_directories(list_exec=flag)

if __name__ == "__main__":
    main()

from reader import read_log

# Zaimplementuj mechanizm sortowania listy korzystając z funkcji sorted() lub sort().
# index – liczba określająca element krotki, według którego zostanie wykonane sortowanie.
def sort_log(log: list, index: int) -> list:
    try:
        if not log:
            return []

        # Sprawdzenie poprawności indeksu względem długości krotek
        # if not all(isinstance(entry, tuple) for entry in log):
        #     raise ValueError("Wszystkie wpisy w logu muszą być krotkami.")
        # if index < 0 or index >= len(log[0]):
        #     raise IndexError(f"Index {index} wykracza poza rozmiar krotek.")
        # Sortowanie listy według danego indeksu
        return sorted(log, key=lambda entry: entry[index])

    except IndexError as e:
        print(f"tak indeksu: {e}")
    except ValueError as e:
        print(f"Błąd wartości: {e}")
    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")

    return []






if __name__ == "__main__":
    print("sorted.py")

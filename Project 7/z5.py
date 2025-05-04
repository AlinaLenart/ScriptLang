import logging
import functools
import time
from datetime import datetime

# logging config
# Konfiguracja logowania — logi będą zapisywane do pliku 'logi.log'
logging.basicConfig(
    # logs will be saved to logs.log file
    filename='logs.log',
    encoding='utf-8',
    level=logging.DEBUG,  # umożliwia logowanie wszystkiego od DEBUG w górę
    format='%(asctime)s\t%(levelname)s\t%(message)s'
)

# logging decorator func call and classes
def log(level=logging.INFO):
    def decorator(obj):
        if isinstance(obj, type):  # dekorowanie klasy
            original_init = obj.__init__

            @functools.wraps(original_init)
            def new_init(self, *args, **kwargs):
                logging.log(level, f"Utworzono obiekt klasy {obj.__name__} z args={args}, kwargs={kwargs}")
                original_init(self, *args, **kwargs)

            obj.__init__ = new_init
            return obj

        # func decorating
        elif callable(obj):  
            @functools.wraps(obj)
            def wrapper(*args, **kwargs):
                start = time.perf_counter()
                logging.log(level, f"Function call {obj.__name__} with args={args}, kwargs={kwargs}")
                result = obj(*args, **kwargs)
                end = time.perf_counter()
                logging.log(level, f"Function {obj.__name__} returned {result} (time: {end - start:.6f}s)")
                return result

            return wrapper
        else:
            raise TypeError("Dekorator @log może być użyty tylko z klasami lub funkcjami.")
    return decorator

# testing func with decorator
@log(logging.DEBUG)
def add(x, y):
    return x + y

# testing class with decorator
@log(logging.INFO)
class Station:
    def __init__(self, code, name):
        self.code = code
        self.name = name

    def station_info(self):
        print(f"Station: {self.name} ({self.code}.upper())")
        return (self.code.upper())


if __name__ == "__main__":
    wynik = add(7, 8)
    print("Wynik dodawania:", wynik)

    s = Station("WAW3424_Mob", "Warszawa ul. Mokotowska 13")
    print(s.station_info())

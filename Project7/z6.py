import logging
import functools
import time

# logging config
logging.basicConfig(
    # logs will be saved to logs.log file, overwriting previous logs
    filename='logs.log',
    encoding='utf-8',
    # log level, can be changed to logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
    level=logging.DEBUG,
    # time, log level and message  
    format='%(asctime)s\t%(levelname)s\t%(message)s'
)

# logging decorator func call and classes
def log(level):
    # actual decorator that will wrap the function or class
    def decorator(obj):
        # check if class
        if isinstance(obj, type):  
            original_init = obj.__init__

            # internal wrapper function in decorator that wraps original function 
            @functools.wraps(original_init)
            def new_init(self, *args, **kwargs):
                logging.log(level, f"Created object of class {obj.__name__} with args={args}, kwargs={kwargs}")
                # call original __init__ method
                original_init(self, *args, **kwargs)
    
            obj.__init__ = new_init
            return obj

        # check if  function
        elif callable(obj): 
            @functools.wraps(obj)
            def wrapper(*args, **kwargs):
                start = time.perf_counter()
                logging.log(level, f"Function call {obj.__name__} with args={args}, kwargs={kwargs}")
                # call original function
                result = obj(*args, **kwargs)
                end = time.perf_counter()
                logging.log(level, f"Function {obj.__name__} returned {result} (time: {end - start:.6f}s)")
                return result
            return wrapper
        
        # decorator only to functions or classes
        else:
            raise TypeError("@log can be used only with classes or func")
        
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
    #@log(logging.INFO)
    def station_info(self):
        print(f"Station: {self.name} ({self.code}.upper())")
        return (self.code.upper())

def main():
    result = add(7, 8)
    print("Adding result:", result)

    result2 = add(x=7, y=8)
    print("Adding result:", result2)

    s = Station("WAW3424_Mob", "Warszawa ul. Mokotowska 13")
    # not logged, because _station_info is not decorated
    s.station_info()


if __name__ == "__main__":
    main()

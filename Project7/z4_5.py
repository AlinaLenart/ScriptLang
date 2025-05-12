from functools import lru_cache
import time

def make_generator(f):
    def generator():
        n = 1  
        while True:
            # lazy evaluation of f(n), calcualte every next(), used for generator func
            yield f(n) 
            n += 1
            # return generator object
    return generator()  

# memoized version
def make_generator_mem(f):
    # decorate the fucntion with lru_cache
    memo_f = lru_cache(maxsize=128)(f)  
    # the same function but with memoization
    return make_generator(memo_f)      

# slow function to test the generatir, multiply by 2
@lru_cache(maxsize=128)
def slow_double(n):
    print(f"\nCalculating 2 * {n}...")
    time.sleep(1)  # sztuczne spowolnienie
    return 2 * n


def main():
    print("\n\nAlternating sign:")
    alt_sign = make_generator(lambda n: n if n % 2 else -n)
    for _ in range(8):
        print(next(alt_sign), end=" ")  # 1 -2 3 -4 5 -6 7 -8


    print("\n\nTesting make_generator_mem with slow_double(n):")

    gen = make_generator_mem(slow_double)

    ## with delayed evaluation
    for _ in range(5):
        print(next(gen), end=" ")  # 5 sec

    # same generator, but with cached values (no dealy)
    gen2 = make_generator_mem(slow_double)
    print("\n\nSame func call but cached values (instant result):")
    for _ in range(5):
        print(next(gen2), end=" ")  

if __name__ == "__main__":
    main()
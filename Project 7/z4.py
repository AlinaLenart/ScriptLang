def make_generator(f):
    # define a generator function inside (closure)
    def generator():
        n = 1  # Start from 1
        while True:
            yield f(n)  # Lazy evaluation of f(n)
            n += 1
    return generator()  # Return the generator object


if __name__ == "__main__":
    print("\n\nAlternating sign:")
    alt_sign = make_generator(lambda n: n if n % 2 else -n)
    for _ in range(8):
        print(next(alt_sign), end=" ")  # 1 -2 3 -4 5 -6 7 -8

    print("\n\Squares:")
    powers = make_generator(lambda n: n ** 2)
    for _ in range(5):
        print(next(powers), end=" ")  # 1 4 9 16 25
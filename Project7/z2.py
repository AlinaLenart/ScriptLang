from functools import reduce
#functional acumulation
# reduce(func, iterable, initial) 

# returns true if ALL elements satisfy the predicate
def forall(pred, iterable):
    return reduce(lambda acc, el: acc and pred(el), iterable, True)

# returns true if AT LEAST ONE element satisfies the predicate
def exists(pred, iterable):
    return reduce(lambda acc, el: acc or pred(el), iterable, False)

# returns true IF AT LEAST N elements satisfy the predicate
def atleast(n, pred, iterable):
    return reduce(lambda acc, el: acc + int(pred(el)), iterable, 0) >= n

# returns true IF AT MOST N elements satisfy the predicate
def atmost(n, pred, iterable):
    return reduce(lambda acc, el: acc + int(pred(el)), iterable, 0) <= n


def main():
    is_even = lambda x: x % 2 == 0
    numbers = [2, 4, 6, 8]
    mixed = [1, 2, 3, 4]

    print("forall(is_even, numbers):", forall(is_even, numbers))  # true
    print("forall(is_even, mixed):", forall(is_even, mixed))      # false

    print("exists(is_even, numbers):", exists(is_even, numbers))  # true
    print("exists(is_even, [1, 3, 5]):", exists(is_even, [1, 3, 5]))  # false

    print("atleast(2, is_even, mixed):", atleast(2, is_even, mixed))  # true
    print("atleast(3, is_even, mixed):", atleast(3, is_even, mixed))  # false

    print("atmost(2, is_even, mixed):", atmost(2, is_even, mixed))    # true
    print("atmost(1, is_even, mixed):", atmost(1, is_even, mixed))    # false

if __name__ == "__main__":
    main()

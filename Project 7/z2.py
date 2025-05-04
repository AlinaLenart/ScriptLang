# returns true if all elements satisfy the predicate
def forall(pred, iterable):
    return all(map(pred, iterable))

# returns true if at least one element satisfies the predicate
def exists(pred, iterable):
    return any(map(pred, iterable))

# returns true if at least n elements satisfy the predicate
def atleast(n, pred, iterable):
    return sum(map(pred, iterable)) >= n

# returns true if at most n elements satisfy the predicate
def atmost(n, pred, iterable):
    return sum(map(pred, iterable)) <= n


if __name__ == "__main__":
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

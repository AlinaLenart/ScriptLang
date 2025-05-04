from functools import reduce
from collections import defaultdict
from collections.abc import Iterable

# create an acronym from the first letters of each word '(uppercased)
def acronym(words):
    return reduce(lambda acc, w: acc + w[0].upper(), words, '')

def median(list):
    if not list:
        #handle edge case: empty list
        raise ValueError("Cannot compute median of an empty list")
    sorted_list = sorted(list)
    n = len(sorted_list)
    return (
        # middle element for odd length list
        sorted_list[n // 2]
        if n % 2
        # average for even length list
        else (sorted_list[n // 2 - 1] + sorted_list[n // 2]) / 2
    )

# calculate esquare root using Newtons method
def pierwiastek(x, epsilon):
    def newton(y):
        return y if abs(y*y - x) < epsilon else newton((y + x / y) / 2)
    return newton(x / 2)

# create a dictionary mapping each letter to a list of words containing that letter
def make_alpha_dict(text):
    # split input text -> list of words
    words = text.split()
    # extract all alphabetic chars from the text, remove duplicates and sort them
    letters = sorted(set(filter(str.isalpha, ''.join(words))))
    # use reduce() to build dict 
    # for each letter add an entry mapping it to a list of words that contain that letter
    return reduce(
        lambda acc, letter: {
            # keep all previous dictionary entries
            **acc,  
            # sdd words containing the current letter
            letter: list(filter(lambda word: letter in word, words))  # Add words containing the current letter
        },
        # sequence of unique letters to iterate over and initial empty dictionary
        letters,  {}
    )

# flatten nested lists/tuples into a single flat list
def flatten(lst):
    return list(
        reduce(
            lambda acc, el: acc + (flatten(el) if isinstance(el, (list, tuple)) else [el]),
            lst,
            []
        )
    )


if __name__ == "__main__":
    print("acronym(['Zakład', 'Ubezpieczeń', 'Społecznych']) =", acronym(['Zakład', 'Ubezpieczeń', 'Społecznych']))  # ZUS
    print("median([1, 1, 19, 2, 3, 4, 4, 5, 1]) =", median([1, 1, 19, 2, 3, 4, 4, 5, 1]))  # 3
    print("pierwiastek(3, epsilon=0.1) =", pierwiastek(3, epsilon=0.1))  # ~1.73
    print("make_alpha_dict('on i ona') =", make_alpha_dict("on i ona"))
    print("flatten([1, [2, 3], [[4, 5], 6]]) =", flatten([1, [2, 3], [[4, 5], 6]]))  # [1, 2, 3, 4, 5, 6]
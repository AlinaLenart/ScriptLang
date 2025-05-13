from functools import reduce
# from collections import defaultdict
# from collections.abc import Iterable

# create an acronym (skrotowiec) from the first letters of each word '(uppercased)
def acronym(words):
    return reduce(lambda acc, current_word: acc + current_word[0].upper(), words, '')

def median(list):
    #handle edge case: empty list
    assert list, "Cannot compute median of an empty list" 
    sorted_list = sorted(list)
    n = len(sorted_list)
    return (
        # middle element for odd length list
        sorted_list[n // 2] if n % 2
        # average for even length list
        else (sorted_list[n // 2 - 1] + sorted_list[n // 2]) / 2
    )

# calculate esquare root using newtons method, epsilon is the precision
def pierwiastek(x, epsilon):
    """y=x/2  # initial guess
    while abs(y*y-x)>= epsilon:
        y =(y+x/y)/2  # next approximation
    return y"""
    assert x >= 0, "Cannot compute square root of a negative number"
    def newton(y):
        # finding next approximation of y
        return y if abs(y*y - x) < epsilon else newton((y + x / y) / 2)
    return newton(x / 2)

# create a dictionary mapping each letter to a list of words containing that letter
def make_alpha_dict(text):
    # split input text -> list of words
    words = text.split()
    # extract all alphabetic chars from the text
    # join = make string from words, filter = remove non alpha 
    # dict.fromkeys = remove duplicates, SAME order
    letters = dict.fromkeys(filter(str.isalpha, ''.join(words))).keys()

    # use reduce(function, iterable, initial) to iteratively build dict 
    # letter : list od words from input cointining that letter
    return reduce(
        lambda acc, letter: {
            # copy previous dict
            **acc,  
            # add new words containing the current letter
            letter: list(filter(lambda word: letter in word, words)) 
        },
        letters,  {}
    )

# flatten nested lists/tuples into a single flat list
def flatten(lst):
    # reduce(func, iterable, initial) 
    return list(
        reduce(
            # if el is list or tuple = flatten (non-tail recursion) it - not last operation
            # else add to acc
            lambda acc, el: acc + (flatten(el) if isinstance(el, (list, tuple)) else [el]),
            lst,
            []
        )
    )


def main():
    print("acronym(['Zakład', 'Ubezpieczeń', 'Społecznych']) =", acronym(['Zakład', 'Ubezpieczeń', 'Społecznych']))  # ZUS
    print("median([1, 1, 19, 2, 3, 4, 4, 5, 1]) =", median([1, 1, 19, 2, 3, 4, 4, 5, 1]))  # 3
    # print("median([]) =", median([]))
    print("pierwiastek(9, epsilon=0.1) =", pierwiastek(9, epsilon=0.0001))  # 3,...
    print("make_alpha_dict('on i ona') =", make_alpha_dict("on i ona"))
    print("flatten([1, [2, 3], [[4, 5], 6]]) =", flatten([1, [2, 3], [[4, 5], 6]]))  # [1, 2, 3, 4, 5, 6]

if __name__ == "__main__":
    main()
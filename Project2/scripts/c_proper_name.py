import sys
from helpers import utils

def calculate_proper_name_sentence_ratio() -> float:
    total_sentences = 0
    sentences_with_proper_names = 0
    in_sentence = False
    first_word = True
    contains_proper_name = False
    current_word = ""

    for line in sys.stdin:
        for char in line:
            # if char == "—":
            #     first_word = True
            #     continue
            # building current word
            if char.isalpha():  
                current_word += char
            # char is not alphabetic but current word exists = new word
            elif current_word: 
                # check if current word is proper name by helper function
                if utils.is_proper_name(current_word, first_word):
                    contains_proper_name = True
                # continue processing sentence and reset current word
                first_word = False  
                current_word = "" 

            # end of sentence reached
            if utils.is_sentence_end_mark(char): 
                # count sentence to total counter
                if in_sentence:
                    total_sentences += 1
                    # count sentence as with proper name
                    if contains_proper_name:
                        sentences_with_proper_names += 1
                    # reset buffer for new sentence
                    contains_proper_name = False
                    first_word = True
                    in_sentence = False
            # remove whitespace chars, recognize sentence start
            elif char.strip():  
                in_sentence = True

    # edge case = if last sentence ends without punctuation 
    if in_sentence:
        total_sentences += 1
        if contains_proper_name:
            sentences_with_proper_names += 1

    # to avoid dividing by zero
    if total_sentences == 0:
        return 0.0

    return (sentences_with_proper_names / total_sentences) * 100
    


if __name__ == "__main__":
    try:
        result = calculate_proper_name_sentence_ratio()
        print(f"Procent of sentences with proper names: {result:.2f}%")
    except Exception as e:
        print(f"Błąd: {e}", file=sys.stderr)
        sys.exit(1)

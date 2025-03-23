import sys
#for voluming up value to int
import math
from helpers import utils

# helper function to find fourth quantil sentence length
def calculate_quantil_value() -> int:
    sentence_lengths = []
    current_length = 0

    # first processing: collecting sentences lengths 
    for line in sys.stdin:
        for char in line:
            # if not blank character increase length
            if not utils.is_whitespace(char):  
                current_length += 1  
            # reached sentence end
            if utils.is_sentence_end_mark(char):  
                sentence_lengths.append(current_length)  
                current_length = 0  
    # no sentences to process
    if not sentence_lengths:
        return 0  

    # calculating fourth quantile, sort values to pick value with is straight in the 3/4 of set
    sentence_lengths.sort()
    # if index is float it volumes up result
    quantil_index = math.ceil(0.75 * len(sentence_lengths))
    return sentence_lengths[quantil_index]  

# function that filters longest 3/4 sentences
def filter_longest_sentences() -> str:
    quantil_value = calculate_quantil_value()
    # no valid sentences  
    if quantil_value == 0:
        return ""  

    current_sentence = ""
    current_length = 0
    result = ""

    # we have to reset stdin to process input again - second processing
    sys.stdin.seek(0)  

    for line in sys.stdin:
        for char in line:
            # if not blank character increase length
            if not utils.is_whitespace(char):  
                current_length += 1 
            # update sentence buffor     
            current_sentence += char  
            # reached sentence end
            if utils.is_sentence_end_mark(char):  
                # rule followed, append sentence to result
                if current_length >= quantil_value:  
                    result += current_sentence.strip() + "\n"  

                #reset current sentence buffors
                current_sentence = ""
                current_length = 0  
    # remove \n
    return result.strip()  

if __name__ == "__main__":
    try:
        result = filter_longest_sentences()
        print(result)  
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
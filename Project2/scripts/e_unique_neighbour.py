import sys
from helpers import utils

# longest sentence where neighbouring word starts with another letter
def find_longest_unique_sentence() -> str:
    longest_sentence = ""
    longest_length = 0
    current_sentence = ""
    current_length = 0
    prev_start_letter = ""
    current_word = ""
    valid_sentence = True 

    for line in sys.stdin:
        for char in line:
            # check if char is part of the current word
            if char.isalpha():
                current_word += char 
                # char is not alphabetic but current word exists = new word
            elif current_word: 
                # converting to lower case to avoid mistakes like N =/= n
                first_letter = current_word[0].lower()  
                # neighbours start with same letter = don't count this sentence
                if first_letter == prev_start_letter:
                    valid_sentence = False  
                # reset for next word
                prev_start_letter = first_letter
                current_word = ""  

            # adding character to sentence buffer
            current_sentence += char

            # count non whitespace characters
            if not utils.is_whitespace(char):
                current_length += 1

            # recognize sentence end
            if utils.is_sentence_end_mark(char):
                # if rule is followed, change longest bufor if needed
                if valid_sentence and current_length > longest_length:
                    longest_length = current_length
                    longest_sentence = current_sentence

                # # reset for next sentence
                current_sentence = ""
                current_length = 0
                prev_start_letter = ""
                valid_sentence = True 

    # edge case = last sentence in file without punctuation
    if valid_sentence and current_length > longest_length:
        longest_sentence = current_sentence

    return longest_sentence.strip()

if __name__ == "__main__":
    try:
        longest = find_longest_unique_sentence()
        print(longest)
    except Exception as e:
        print(f"Błąd: {e}", file=sys.stderr)
        sys.exit(1)

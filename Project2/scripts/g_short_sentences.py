import sys
from helpers import utils

MAX_WORDS_IN_SHORT_SENTENCE = 4

#function that counts words in each sentence given
def count_words(sentence: str) -> int:
    words_count = 0
    # separate words from whitespace
    in_word = False

    for char in sentence:
        if char.isalpha():
            # when word ends
            if not in_word:
                words_count += 1
            in_word = True
            # when current char is whitespace (end of the word)
        elif utils.is_whitespace(char):
            in_word = False  

    return words_count

# function that extracts sentences from text and returns string only with sentences MAX_WORDS_IN_SHORT_SENTENCE
def filter_short_sentences() -> str:
    current_sentence = ""
    result = ""

    for line in sys.stdin:
        for char in line:
            # create current sentence buffor
            current_sentence += char
            # sentence end recognized
            if utils.is_sentence_end_mark(char):  
                if count_words(current_sentence) <= MAX_WORDS_IN_SHORT_SENTENCE:
                    # if words in sentence follow the rule, append sentence to result
                    result += current_sentence.strip() + "\n"  

                # reset buffor
                current_sentence = ""
    # remove added \n
    return result.strip()  

if __name__ == "__main__":
    try:
        result = filter_short_sentences()
        print(result)  
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

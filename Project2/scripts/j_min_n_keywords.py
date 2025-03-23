import sys
from helpers import utils

# set/collection of unique keywords
KEYWORDS = {'i', 'oraz', 'ale', 'że', 'lub'}
MIN_KEYWORDS = 2

# function that filters only sentences using at least MIN_CONJUCTIONS of KEYWORDS
def filter_sentences_with_keywords():
    current_sentence = ""
    current_word = ""
    keyword_count = 0
    result = ""

    for line in sys.stdin:
        for char in line:
            # building current word char by char
            if char.isalpha(): 
                current_word += char
            # fe. whitespace encountered = word end
            else:
                if current_word:  
                    # check if current word is one of KEYWORDS and count it
                    if current_word in KEYWORDS:  
                        keyword_count += 1
                    # update sentence buffor and reset word buffor
                    current_sentence += current_word  
                    current_word = ""  

                #add non alphabetic char . or space to sentence buffor
                current_sentence += char  

                # sentence end
                if utils.is_sentence_end_mark(char): 
                    # check if sentence follow MIN_KEYWORDS ammount of KEYWORDS
                    if keyword_count >= MIN_KEYWORDS:  
                        result += current_sentence.strip() + "\n"

                    #reste buffors for next sentence
                    current_sentence = ""
                    keyword_count = 0

    # edge case = last sentence without punctuation
    if current_word and keyword_count >= MIN_KEYWORDS:
        result += current_sentence.strip() + "\n"

    # remove \n
    return result.strip()  

if __name__ == "__main__":
    try:
        result = filter_sentences_with_keywords()
        print(result)  
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
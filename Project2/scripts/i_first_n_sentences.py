import sys
from helpers import utils

AMOUNT_OF_SENTENCES_TO_SHOW = 20

def extract_first_n_sentences():
    sentence_count = 0
    current_sentence = ""
    result = ""

    for line in sys.stdin:
        for char in line:
            # update current sentence buffor for current character
            current_sentence += char 
            
            # sentence end recognzied
            if utils.is_sentence_end_mark(char):
                # update counter and result with curret sentence
                sentence_count += 1
                result += current_sentence.strip() + "\n"

                # reset current sentence buffor for next one
                current_sentence = ""

                # limit reached
                if sentence_count == AMOUNT_OF_SENTENCES_TO_SHOW:
                    return result.strip()
    # edge case: text has less than AMOUNT sentences
    return result.strip()

if __name__ == "__main__":
    try:
        result = extract_first_n_sentences()
        print(result)
    except Exception as e:
        print(f"Błąd: {e}", file=sys.stderr)
        sys.exit(1)

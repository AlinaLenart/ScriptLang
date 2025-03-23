import sys
from helpers import utils

#function that filters only sentences ended by ! or ?
def filter_exclamatory_and_question_sentences() -> str:
    current_sentence = ""
    result = ""

    for line in sys.stdin:
        for char in line:
            # create current sentence buffor by adding each character
            current_sentence += char  

            # check if sentence follow the rule, then append it to result
            if utils.is_question_or_exclamation(char):
                result += current_sentence.strip() + "\n"
                #reset current buffor
                current_sentence = ""
                #normal sentence to omit
            elif utils.is_sentence_end_mark(char):
                current_sentence = ""

if __name__ == "__main__":
    try:
        result = filter_exclamatory_and_question_sentences()
        print(result)
    except Exception as e:
        print(f"Błąd: {e}", file=sys.stderr)
        sys.exit(1)

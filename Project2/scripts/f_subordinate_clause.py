import sys
from helpers import utils

# function finds FIRST sentence in text having at least 2 complex sentence
def find_complex_sentence() -> str:
    current_sentence = ""
    comma_count = 0

    for line in sys.stdin:
        for char in line:
            # sentence output buffor
            current_sentence += char

            # count comma in sentence
            if char == ",":
                comma_count += 1

            # recognize sentence end
            if utils.is_sentence_end_mark(char):
                # complex snetence means more than 1 comma
                if comma_count > 1:  
                    return current_sentence.strip()

                # reset sentence buffor
                current_sentence = ""
                comma_count = 0

    return "Valid sentence not found"

if __name__ == "__main__":
    try:
        result = find_complex_sentence()
        print(result)
    except Exception as e:
        print(f"Błąd: {e}", file=sys.stderr)
        sys.exit(1)

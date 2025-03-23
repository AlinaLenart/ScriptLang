import sys
from helpers import utils

def find_longest_sentence() -> str:
    longest_sentence = ""
    longest_length = 0
    current_sentence = ""
    current_length = 0

    for line in sys.stdin:
        for char in line:
            # count everything but whitespace chracters
            if not utils.is_whitespace(char):
                current_length += 1
                
            # update current sentence 
            current_sentence += char

            # recognize sentence end
            if utils.is_sentence_end_mark(char):
                # compare length (and change longest buffor if needed)
                if current_length > longest_length:
                    longest_length = current_length
                    longest_sentence = current_sentence

                # reset buffor for current
                current_sentence = ""
                current_length = 0

    # edge case = last sentence in file without punctuation
    if current_length > longest_length:
        longest_sentence = current_sentence

    # return with strip to avoid using unnecessary whitespace characters
    return longest_sentence.strip() 

if __name__ == "__main__":
    try:
        longest = find_longest_sentence()
        print("Longest sentence:")
        print(longest)
    except Exception as e:
        print(f"Błąd: {e}", file=sys.stderr)
        sys.exit(1)

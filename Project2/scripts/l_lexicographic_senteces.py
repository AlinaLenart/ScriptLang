import sys
from helpers import utils

#function that checks if words in sentence are sorted alphabetically
def is_lexicographically_sorted(sentence: str) -> bool:
    previous_word = ""
    current_word = ""

    for char in sentence:
        # build word from alphabetic char
        if char.isalpha():
            current_word += char 
        # non alphabetic character = word end  
        elif current_word:  
            # have to be lowered to not ruined N = n, a > N
            if previous_word and previous_word.lower() > current_word.lower():
                # broken order = no need to check other words
                return False 
            # reset current word
            previous_word = current_word
            current_word = ""  
    # if whole sentence follow the rule
    return True 

# filters only lexicographically sorted sentences (words are sorted alphabetically) 
def filter_lexicographically_sorted_sentences() -> str:
    current_sentence = ""
    result = ""

    for line in sys.stdin:
        for char in line:
            # uopdate buffor for sentence, needed for output
            current_sentence += char 

            # sentence end reached
            if utils.is_sentence_end_mark(char): 
                 # rule followed, append sentence to result
                if is_lexicographically_sorted(current_sentence):
                    result += current_sentence.strip() + "\n"  # Append to result
                
                # reset current sentence buffor
                current_sentence = ""
    #remove \n
    return result.strip()  

if __name__ == "__main__":
    try:
        result = filter_lexicographically_sorted_sentences()
        print(result)  
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
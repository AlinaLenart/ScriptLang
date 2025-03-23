# returns True if the line is empty or contains only whitespace
def is_line_empty(line: str) -> bool:
    #strip function removes all leading and trailing whitespace from line (spaces, tabs, newm lines)
    return line.strip() == ""

# returns True if the character is a whitespace character
def is_whitespace(char: str) -> bool:
    return char == " " or char == "\t" or char == "\n"  

# returns True if the character is a sentence end punctuation mark 
def is_sentence_end_mark(char: str) -> bool:
    return char in {'.', '!', '?', ':'}

# check if word is proper name = exists, starts with upper case and not first word in sentence
def is_proper_name(word: str, first_word: bool) -> bool:
    return word and word[0].isupper() and not first_word

# def remove_whitespace(s:str) -> str:
# #     return s.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")

# def is_valid_word_char(char: str) -> bool:
#     return char.isalpha() or char == "-"

def is_question_or_exclamation(char: str) -> bool:
    return char in {'?', '!'}
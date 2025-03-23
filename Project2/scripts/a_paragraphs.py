import sys
from helpers import utils

def count_paragraphs() -> int:
    paragraph_count = 0
    in_paragraph = False

    for line in sys.stdin:
        # helper function that checks if after deleting all whitespace characters line is emtpy
        if utils.is_line_empty(line):
            in_paragraph = False  
        # new paragrapgh recognized
        elif not in_paragraph:
            paragraph_count += 1  
            in_paragraph = True
        
    return paragraph_count


if __name__ == "__main__":
    try:
        result = count_paragraphs()
        print(f"Number of paragraphs: {result}")
    except FileNotFoundError:
        print("Error: The specified file was not found.", file=sys.stderr)
    except PermissionError:
        print("Error: Permission denied while accessing the file.", file=sys.stderr)
    except ModuleNotFoundError:
        print("Error: The `helpers` module or `utils` file is missing or not found.", file=sys.stderr)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)



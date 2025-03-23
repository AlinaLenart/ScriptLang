import sys
from helpers import utils

def count_non_whitespace_characters() -> int:
     # counter for char number
    char_count = 0
    # going down char by char
    for line in sys.stdin:
        for char in line:  
            # if inside word
            if not utils.is_whitespace(char):
                char_count += 1
    return char_count


if __name__ == "__main__":
    try:
        result = count_non_whitespace_characters()
        print(f"Number of characters (without whitespace characters): {result}")
    except FileNotFoundError:
        print("Error: The specified file was not found.", file=sys.stderr)
    except PermissionError:
        print("Error: Permission denied while accessing the file.", file=sys.stderr)
    except ModuleNotFoundError:
        print("Error: The `helpers` module or `utils` file is missing or not found.", file=sys.stderr)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)

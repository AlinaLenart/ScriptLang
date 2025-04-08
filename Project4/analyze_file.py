import sys
import json
import collections

# analyzes a text file and returns: file path, total characters, words, lines and most frequent character, word
def analyze_file(file_path):
    try:
        #try to open and read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        sys.exit(f"Error readingf file '{file_path}': {e}")

    total_characters = len(content)

     #split into words and count them
    words = content.split()
    total_words = len(words)

    lines = content.splitlines()
    total_lines = len(lines)

    char_counter = collections.Counter(content)
    most_common_char, _ = char_counter.most_common(1)[0] if char_counter else (None, 0)

    #count word frequencies, case-insensitive
    word_counter = collections.Counter(word.lower() for word in words)
    most_common_word, _ = word_counter.most_common(1)[0] if word_counter else (None, 0)

    # build result dictionary
    result = {
        "file_path": file_path,
        "total_characters": total_characters,
        "total_words": total_words,
        "total_lines": total_lines,
        "most_frequent_character": most_common_char,
        "most_frequent_word": most_common_word
    }
    return result

def main():
    file_path = sys.stdin.read().strip()
    if not file_path:
        sys.exit("No file path given")
    analysis = analyze_file(file_path)
    print(json.dumps(analysis, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

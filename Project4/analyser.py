#!/usr/bin/env python3
import sys
import json
import collections

def analyze_file(file_path):
    """
    Analizuje zawartość pliku tekstowego i zwraca słownik zawierający:
      - file_path: ścieżka do pliku,
      - total_characters: całkowita liczba znaków,
      - total_words: całkowita liczba słów,
      - total_lines: liczba wierszy,
      - most_frequent_character: znak występujący najczęściej,
      - most_frequent_word: słowo występujące najczęściej.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        sys.exit(f"Błąd podczas odczytu pliku '{file_path}': {e}")

    total_characters = len(content)
    words = content.split()
    total_words = len(words)
    lines = content.splitlines()
    total_lines = len(lines)

    char_counter = collections.Counter(content)
    most_common_char, _ = char_counter.most_common(1)[0] if char_counter else (None, 0)

    word_counter = collections.Counter(word.lower() for word in words)
    most_common_word, _ = word_counter.most_common(1)[0] if word_counter else (None, 0)

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
    # Odczytujemy ścieżkę do pliku ze standardowego wejścia.
    file_path = sys.stdin.read().strip()
    if not file_path:
        sys.exit("Nie podano ścieżki do pliku.")
    analysis = analyze_file(file_path)
    print(json.dumps(analysis, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

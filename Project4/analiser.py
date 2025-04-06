import sys
import json
import collections

def analyze_file(file_path):
    """
    Analizuje zawartość pliku i zwraca słownik ze statystykami:
      - file_path: ścieżka do pliku,
      - total_characters: całkowita liczba znaków,
      - total_words: całkowita liczba słów,
      - total_lines: liczba wierszy,
      - most_frequent_character: znak występujący najczęściej wraz z liczbą wystąpień,
      - most_frequent_word: słowo występujące najczęściej wraz z liczbą wystąpień,
      - char_counts: szczegółowy licznik znaków,
      - word_counts: szczegółowy licznik słów.
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
    most_common_char, most_common_char_count = char_counter.most_common(1)[0] if char_counter else (None, 0)

    word_counter = collections.Counter(word.lower() for word in words)
    most_common_word, most_common_word_count = word_counter.most_common(1)[0] if word_counter else (None, 0)

    result = {
        "file_path": file_path,
        "total_characters": total_characters,
        "total_words": total_words,
        "total_lines": total_lines,
        "most_frequent_character": most_common_char,
        "most_frequent_character_count": most_common_char_count,
        "most_frequent_word": most_common_word,
        "most_frequent_word_count": most_common_word_count,
        "char_counts": dict(char_counter),
        "word_counts": dict(word_counter)
    }
    return result

def main():
    # Czytamy sciezke do pliku ze standardowego wejscia
    file_path = sys.stdin.read().strip()
    if not file_path:
        sys.exit("Nie podano ścieżki do pliku.")
    analysis = analyze_file(file_path)
    # Wypisujemy wynik w formacie JSON
    print(json.dumps(analysis, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

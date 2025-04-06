import collections

def aggregate_statistics(results):
    """
    Agreguje statystyki z listy wyników (słowników) uzyskanych z analizy plików.
    Zwraca słownik zawierający:
      - total_files: liczbę przetworzonych plików,
      - total_characters: sumaryczną liczbę znaków,
      - total_words: sumaryczną liczbę słów,
      - total_lines: sumaryczną liczbę wierszy,
      - most_frequent_character: znak występujący najczęściej globalnie,
      - most_frequent_word: słowo występujące najczęściej globalnie.
    """
    total_files = len(results)
    total_characters = sum(item["total_characters"] for item in results)
    total_words = sum(item["total_words"] for item in results)
    total_lines = sum(item["total_lines"] for item in results)
    
    overall_char_counter = collections.Counter()
    overall_word_counter = collections.Counter()
    for item in results:
        overall_char_counter.update(item.get("char_counts", {}))
        overall_word_counter.update(item.get("word_counts", {}))
    
    most_common_char, _ = overall_char_counter.most_common(1)[0] if overall_char_counter else (None, 0)
    most_common_word, _ = overall_word_counter.most_common(1)[0] if overall_word_counter else (None, 0)
    
    aggregate_result = {
        "total_files": total_files,
        "total_characters": total_characters,
        "total_words": total_words,
        "total_lines": total_lines,
        "most_frequent_character": most_common_char,
        "most_frequent_word": most_common_word
    }
    return aggregate_result

if __name__ == "__main__":
    print("aggregator")

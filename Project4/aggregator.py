import collections

# aggregates stats from multiple file analyses, returns: total files, characters, words, lines and most frequent character and word 
def aggregate_statistics(results):
    #count total number of files
    total_files = len(results)

    total_characters = sum(item["total_characters"] for item in results)
    total_words = sum(item["total_words"] for item in results)
    total_lines = sum(item["total_lines"] for item in results)
    
    # counting frequency
    overall_char_counter = collections.Counter()
    overall_word_counter = collections.Counter()
    
    for item in results:
        overall_char_counter[item["most_frequent_character"]] += 1
        overall_word_counter[item["most_frequent_word"]] += 1

    most_common_char, _ = overall_char_counter.most_common(1)[0] if overall_char_counter else (None, 0)
    most_common_word, _ = overall_word_counter.most_common(1)[0] if overall_word_counter else (None, 0)
    
    # build result dictionary
    aggregate_result = {
        "total_files": total_files,
        "total_characters": total_characters,
        "total_words": total_words,
        "total_lines": total_lines,
        "most_frequent_character": most_common_char,
        "most_frequent_word": most_common_word
    }
    return aggregate_result



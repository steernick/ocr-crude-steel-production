def jaccard_similarity(str1, str2):
    set1 = set(str1)
    set2 = set(str2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    similarity = intersection / union
    return similarity


def find_similar_words_jaccard(input_word, word_list, threshold):
    similar_words = [word for word in word_list if jaccard_similarity(input_word, word) >= threshold]
    return similar_words


if __name__ == "__main__":
    # Example usage
    input_word = "python"
    word_list = ["java", "javascript", "pythons", "pyramid", "perl", "ruby", "pythonic"]

    threshold = 0.5  # You can adjust the threshold based on your requirement

    similar_words = find_similar_words_jaccard(input_word, word_list, threshold)

    print(f"Similar words to '{input_word}' with Jaccard similarity >= {threshold}:")
    print(similar_words)
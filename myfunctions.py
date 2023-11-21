import re


def jaccard_similarity(str1, str2):
    set1 = set(str1)
    set2 = set(str2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    similarity = intersection / union
    return similarity


def find_similar_words_jaccard(input_word, word_list, threshold: float):
    similar_words = [word for word in word_list if jaccard_similarity(input_word, word) >= threshold]
    return similar_words


def similar_words_with_jaccard_similarity(input_word, word_list):
    similar_words = {word: round(jaccard_similarity(input_word, word), 3) for word in word_list}
    return similar_words


def remove_empty_lines(text: str):
    lines = text.splitlines()
    non_empty_lines = [line for line in lines if line.strip() != '']
    return '\n'.join(non_empty_lines)


def is_row_valid(row: str):
    if row[0].isalpha() and row[-1].isdigit():
        return True
    else:
        return False


def extract_country_from_row(row: str):
    row = row.strip()
    country = ''
    for i in range(len(row)-2):
        if row[i].isalpha():
            country += row[i]
        elif not row[i].isalpha() and row[i+1].isalpha():
            country += row[i]
        elif not row[i].isalpha() and row[i+2].isalpha():
            country += row[i]
        else:
            break
    return country


def filter_out_garbage(country: str):
    elem_list = country.split()
    unwanted = ['(e', '(', ')', '(e:', '(f', '(r']
    for elem in elem_list:
        if elem in unwanted:
            elem_list.remove(elem)
    return ' '.join(elem_list)


def matches_pattern(string: str, patterns: list):
    for pattern in patterns:
        if re.match(pattern, string):
            return True
        else:
            return False


def extract_list_of_countries():
    pass


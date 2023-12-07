import re


def extract_header(line: str):
    header = line.replace('%', '4')
    header = re.sub(r'[i{]', '1', header)
    header = re.sub(r'[^\d\s]', ' ', header).strip().split()
    for i in range(len(header)):
        if len(header[i]) == 8:
            header.insert(i + 1, header[i][4:])
            header[i] = header[i][0:4]
    header = 'Country ' + ' '.join(header)
    return header


def is_element_in_string(string, string_list):
    return any(element in string for element in string_list)


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


def similar_words_with_jaccard_similarity(input_word, word_list, threshold_start=0.0, threshold_end=1.0):
    similar_words = {word: round(jaccard_similarity(input_word, word), 3) for word in word_list}
    similar_words = dict(filter(lambda item: threshold_start <= item[1] <= threshold_end, similar_words.items()))
    similar_words = dict(sorted(similar_words.items(), key=lambda item: item[1], reverse=True))
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


def extract_country_from_line(line: str):
    line = line.replace('C.1.S.', 'C.I.S.')
    line = line.replace('R.0.Korea', 'R.O.Korea')
    country = re.sub(r'[^a-zA-Z\s]', ' ', line).strip()
    country = re.sub(r'\b(\w) \b', r'\1', country)
    country = re.sub(r'\b[a-zA-Z]\b', '', country)
    country = re.sub(r'\b\w*?(\w)\1{2,}\w*\b', '', country)

    # Use re.split() with a regular expression
    country = re.split(r'\s{3,}', country)[0]
    country = country.strip()

    return country

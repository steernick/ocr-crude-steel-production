from pathlib import Path
import re
import json


# Functions definitions
def extract_header(line: str):
    """
    Processes a given string to format it into a specific header style.

    This function performs a series of string manipulations on the input line:
    - Replaces '%' characters with '4'.
    - Substitutes 'i' and '{' characters with '1'.
    - Removes all non-digit, non-space characters, replacing them with spaces.
    - Splits the modified string into segments.
    - Further processes these segments based on their length and specific content.
    - Constructs and returns a header string prefixed with 'Country '.

    Parameters:
    line (str): The input string to be transformed into a header.

    Returns:
    str: The transformed header string.
    """
    header = line.replace('%', '4')
    header = re.sub(r'[i{]', '1', header)
    header = re.sub(r'[^\d\s]', ' ', header).strip().split()
    for i in range(len(header)):
        if len(header[i]) == 8:
            header.insert(i + 1, header[i][4:])
            header[i] = header[i][0:4]
        elif header[i] == '1783':
            header[i] = '1983'
    header = 'Country ' + ' '.join(header)
    return header


def jaccard_similarity(str1, str2):
    """
    Calculates the Jaccard Similarity between two strings.

    The Jaccard Similarity is a measure of similarity between two sets. It is defined as
    the size of the intersection divided by the size of the union of the two sets.

    Parameters:
    str1 (str): The first string to compare.
    str2 (str): The second string to compare.

    Returns:
    float: The Jaccard Similarity between str1 and str2, ranging from 0 (no similarity)
    to 1 (identical).

    Examples:
    >>> jaccard_similarity("abc", "bcd")
    0.5

    >>> jaccard_similarity("same", "same")
    1.0
    """
    set1 = set(str1)
    set2 = set(str2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    similarity = intersection / union
    return similarity


def find_similar_words_jaccard(input_word, word_list, threshold: float):
    """
    Identifies and returns words from a list that are similar to a given input word,
    based on the Jaccard Similarity measure.

    This function computes the Jaccard Similarity between the input word and each word
    in the provided list. Words from the list with a similarity score equal to or
    greater than the specified threshold are considered similar.

    Parameters:
    input_word (str): The word against which other words are compared.
    word_list (list of str): A list of words to be compared with the input word.
    threshold (float): The minimum Jaccard Similarity score for a word to be
                        considered similar. Must be between 0 and 1.

    Returns:
    list of str: A list of words from word_list that have a Jaccard Similarity score
                 with input_word equal to or greater than the threshold.

    Examples:
    >>> find_similar_words_jaccard("apple", ["apply", "appeal", "happy"], 0.4)
    ["apply", "appeal"]

    >>> find_similar_words_jaccard("test", ["test", "tent", "toast"], 1.0)
    ["test"]
    """
    similar_words = [word for word in word_list if jaccard_similarity(input_word, word) >= threshold]
    return similar_words


def extract_country_from_line(line: str):
    """
    Extracts and returns the country name from a given string.

    This function processes a string that potentially contains a country name
    amidst other characters and formatting issues. It applies a series of string
    manipulations and regular expressions to isolate and clean up the country name.

    The process includes:
    - Correcting specific known abbreviations and formatting issues.
    - Removing non-letter characters, except for necessary spaces.
    - Cleaning up isolated single letters and repeated letter sequences.
    - Extracting the first substantial word or phrase, assumed to be the country name.

    Parameters:
    line (str): The string from which the country name is to be extracted.

    Returns:
    str: The extracted and cleaned country name.

    Examples:
    >>> extract_country_from_line("123 C.1.S. ABC DEF 456")
    "C.I.S."

    >>> extract_country_from_line("R.0.Korea GDP: 1.5 Trillion")
    "R.O.Korea"
    """
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


if __name__ == "__main__":

    # Path to .txt files from previous stage after preliminary filtering
    txt_directory = 'input-data/after-first-filter'
    files = Path(txt_directory).glob('*.txt files')

    # Loading .json file with mapping of countries
    with open('input-data/countries_mapping.json', 'r') as json_file:
        countries_mapping = json.load(json_file)

    # Loading manually corrected list of countries from previous stage into list variable
    with open('input-data/countries_correct_list.txt', 'r') as f_clc:
        lines = f_clc.readlines()
        countries_correct_list = [line.strip() for line in lines if line.strip()]

    # Main part of processing text and extracting needed data
    for file in files:
        with open(file, 'r') as f:
            lines = f.readlines()
            header = extract_header(lines[0])
            header_list = header.split()
            no_of_columns = len(header_list) - 1
            csv_fields_list = []
            for line in lines[1:]:
                # Extracting country from line
                if not line[0].isnumeric():
                    country = extract_country_from_line(line)
                country = country.casefold()

                # Extracting amounts from line
                if line.strip()[-4:] == header[-4:]:
                    continue
                else:
                    amounts = line.lower().replace(country, '').strip()

                # Filtering, cleaning and repairing amounts:
                # replacing all non-digits and non-spaces with space
                amounts = re.sub(r'[^0-9\s]', ' ', amounts).strip()
                # merging figures into correct form of amounts
                amounts = re.sub(r'(\b\w{1,3}\b)\s(\b\w{1,3}\b)', r'\1\2', amounts)
                # Repairing amounts depends on problem:
                amounts_list = amounts.split()
                if len(amounts_list) == no_of_columns:
                    pass

                # merging figures if separated
                elif len(amounts_list) == no_of_columns * 2:
                    amounts = ' '.join([amounts_list[i] + amounts_list[i + 1] for i in range(0, len(amounts_list), 2)])

                # cleaning if there are some unwanted figures
                elif len(amounts_list) > no_of_columns and country not in ('asia', 'world', 'france'):
                    amounts = re.sub(r'(\b\w{1,3}\b)\s{2}(\b\w{1,3}\b)', r'\1\2', amounts)
                    amounts = ' '.join(amounts.split()[-10:])

                # Replacing non-existent figures in blank spaces with '000':
                elif amounts.strip() and len(amounts_list) < no_of_columns:
                    amounts = re.sub(r'[^0-9\s]', ' ', line)
                    amounts = amounts.replace('\n', '')

                    # determine where are the blanks
                    whitespace_sequences = re.findall(r'\s+', amounts)
                    whitespace_counts = [len(sequence) for sequence in whitespace_sequences]
                    longest = max(whitespace_counts)
                    pos_of_longest = whitespace_counts.index(longest)

                    # filling in the blanks until the desired length is reached
                    while len(amounts_list) < no_of_columns:
                        amounts_list.insert(pos_of_longest, '000')
                    amounts = ' '.join(amounts_list)

                # taking care of the remaining cases
                else:
                    amounts = re.sub(r'(\b\w{1,4}\b)\s(\b\w{1,4}\b)', r'\1\2', amounts)
                    am_list = amounts.split()
                    if amounts.strip() and len(max(am_list, key=len)) > 7:
                        for i in range(len(am_list)-1):
                            if len(am_list[i]) == 8 and len(am_list[i+1]) == 6:
                                am_list[i+1] = am_list[i][-1] + am_list[i+1]
                                am_list[i] = am_list[i][:7]
                                amounts = ' '.join(am_list)
                amounts = re.sub(r'\s{2,}', ' ', amounts)

                # Filtering country
                country = country.replace('  ', ' ')
                country_similar = find_similar_words_jaccard(country, countries_correct_list, 0.85)
                if country in countries_correct_list:
                    pass
                elif country in countries_mapping:
                    country = countries_mapping[country]
                elif country not in countries_correct_list and country_similar:
                    # print(country, country_similar)
                    country = country_similar[0]
                else:
                    country = '???'

                if country in ('ussr', 'cis'):
                    country = country.upper()
                else:
                    country = country.title()

                # Merging corrected data into csv format
                if country != '???' and len(amounts.split()) == no_of_columns:
                    csv_fields = country + ',' + ','.join(amounts.split())
                    csv_fields_list.append(csv_fields)

            # Saving corrected csv files
            text_csv = ','.join(header_list) + '\n' + '\n'.join(csv_fields_list)
            with open(f'input-data/after-cleaning/{file.name[:-4]}.csv', 'w') as f_w:
                f_w.write(text_csv)

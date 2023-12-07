from pathlib import Path
from myfunctions import (extract_header, extract_country_from_line, find_similar_words_jaccard,
                         join_digits_into_numbers, similar_words_with_jaccard_similarity)
import re
import json

if __name__ == "__main__":

    txt_directory = 'input-data/after-first-filter'
    files = Path(txt_directory).glob('*.txt')

    with open('input-data/countries_mapping.json', 'r') as json_file:
        countries_mapping = json.load(json_file)

    with open('input-data/countries_correct_list.txt', 'r') as f_clc:
        lines = f_clc.readlines()
        countries_correct_list = [line.strip() for line in lines if line.strip()]

    garbage = set()
    count = 0

    for file in files:
        with open(file, 'r') as f:
            lines = f.readlines()
            header = extract_header(lines[0])
            header_list = header.split()
            no_of_columns = len(header_list) - 1
            matched = []
            no_match = []
            for line in lines[1:]:
                # Extracting country from line
                if line[0].isalpha():
                    country = extract_country_from_line(line)
                country = country.casefold()

                # Extracting amounts from line
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
                else:
                    amounts = re.sub(r'(\b\w{1,4}\b)\s(\b\w{1,4}\b)', r'\1\2', amounts)
                    am_list = amounts.split()
                    if amounts.strip() and len(max(am_list, key=len)) > 7:
                        for i in range(len(am_list)-1):
                            if len(am_list[i]) == 8 and len(am_list[i+1]) == 6:
                                am_list[i+1] = am_list[i][-1] + am_list[i+1]
                                am_list[i] = am_list[i][:7]
                                amounts = ' '.join(am_list)
                    # print(country, '---', no_of_columns, '---', amounts, '---', len(amounts.split()))
                amounts = re.sub(r'\s{2,}', ' ', amounts)

                # Filtering country
                country = country.replace('  ', ' ')

                country_similar = find_similar_words_jaccard(country, countries_correct_list, 0.85)
                if country in countries_correct_list:
                    pass
                elif country in countries_mapping:
                    country = countries_mapping[country]
                elif country not in countries_correct_list and country_similar:
                    country_similar = country_similar[0]
                else:
                    garbage.add(country)
                    country = '???'
                # if country == '???':
                #     count += 1

                country = country.title()


                # if len(amounts.split()) == no_of_columns:
                #     print(header)
                #     print(country, amounts)
                if country != '???':
                    fields = [country] + amounts.split()
                if len(fields) == no_of_columns+1:
                    matched.append(','.join(fields))
                else:
                    no_match.append(' '.join(fields))
                    print(amounts, '---', len(amounts.split()), '---', (no_of_columns-1), file.name, country)
            text = ','.join(header_list) + '\n' + '\n'.join(matched) + '\n' + '\n'.join(no_match)
            with open(f'input-data/after-cleaning/{file.name[:-4]}.csv', 'w') as f_w:
                f_w.write(text)
    print('Count is: ', count)

    # print(list(sorted(garbage)))
    # print(len(garbage))
    # lst = ['123', '9', '0000']
    # print(len(max(lst, key=len)))
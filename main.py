from pathlib import Path
from myfunctions import (is_element_in_string, extract_header, extract_country_from_line, filter_out_garbage,
                        find_similar_words_jaccard, join_digits_into_numbers)
from collections import Counter
import re

if __name__ == "__main__":

    txt_directory = 'input-data/raw-text-files'
    files = Path(txt_directory).glob('*.txt')

    countries_list = []
    ultimate_countries_list = []
    unwanted_str_list = ['total', 'table', 'includes', 'figure', 'figures', 'statistical', 'steel', 'which', 'estimated',
                         'crude', 'calculated', 'from', 'excluding', 'included', 'continued', 'eeSSSe']

    for file in files:
        with open(file, 'r') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines if line.strip()]
            lines = [line for line in lines if len(line) > 35]
            lines = [line for line in lines if not is_element_in_string(line.lower(), unwanted_str_list)]
            for line in lines[1:]:
                if line[0].isalpha():
                    country = extract_country_from_line(line).lower()
                if len(country) > 2:
                    countries_list.append(country)

    countries_counter = Counter(countries_list)
    filtered_countries = sorted([key for key, value in countries_counter.items() if value > 2])
    print(sorted(filtered_countries))
    print(len(filtered_countries))

    final_correct_countries = {
        'austtia': 'austria'
        'austfia': 'austria'
        'aorway': 'norway',
        'aly': 'italy',
        'algerla': 'algeria',
        'iniionesia': 'idnonesia',
        'byelorussia': 'belarus',
        'c.ls': 'CIS',
        'cls': 'CIS',
        'c.i.s': 'CIS',
        'd.p.r. korea': 'north korea',
        'dpr korea': 'north korea',
        'd.r. congo': 'congo',
        'ec total': 'e.c. total',
        'f.r. germany': 'west germany',
        'fr of germany': 'west germany',
        'f.r. yugoslavia': 'yugoslavia',
        'fr germany': 'west germany',
        'german dem rep': 'east germany',
        'german dem. rep': 'east germany',
        'german dem  rep': 'east germany',
        'tnoonesta': 'indonesia',
        'p.r. china': 'china',
        'r.o.korea': 'south korea',
        'republic of korea': 'south korea',
        'rhodesia': 'rhodesia',
        'sweden s': 'sweden',
        'switzerland s': 'switzerland',
        'taiwan (r.o.c': 'taiwan',
        'taiwan china': 'taiwan',
        'tran': 'iran',
        'trinidad': 'trinidad and tobago',
        'u.s.s.r': 'u.s.s.r.',
        'ussr': 'u.s.s.r.',
        'viet nam': 'vietnam'
        # 'western europe': 'western europe'
    }

    with open('countries_list.txt', 'w') as f_cl:
        for c in filtered_countries:
            f_cl.write("%s\n" % c)

    with open('countries_list_corrected.txt', 'r') as f_clc:
        lines = f_clc.readlines()
        countries_list_corrected = [line.strip() for line in lines if line.strip()]
        print(countries_list_corrected)

    files = Path(txt_directory).glob('*.txt')
    garbage = set()

    for file in files:
        with open(file, 'r') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines if line.strip()]
            lines = [line for line in lines if len(line) > 35]
            lines = [line for line in lines if not is_element_in_string(line.lower(), unwanted_str_list)]
            header = extract_header(lines[0])
            header_list = header.split()
            no_of_columns = len(header_list)
            matched = []
            no_match = []
            for line in lines[1:]:
                # Extracting country from line
                if line[0].isalpha():
                    country = extract_country_from_line(line)
                country = country.casefold()

                # line = re.sub(r'\s*\((.{0,4}?)\)\s*', '    ', line)
                # line = re.sub(r'[^\w\s]', '', line)
                # line = line.strip()
                # Extracting amounts from line
                # print(line)
                amounts = line.lower().replace(country, '').strip()
                amounts = re.sub(r'(?<=\d) (?=\d)', '', amounts)
                # print(amounts)
                # Filtering country

                # if country not in filtered_countries:
                #     for elem in country.split():
                #         if elem in filtered_countries:
                #             print(country)
                #             country = elem
                country = country.replace('  ', ' ')
                country_similar = find_similar_words_jaccard(country, countries_list_corrected, 0.85)
                if country in countries_list_corrected:
                    continue
                elif country in final_correct_countries:
                    country = final_correct_countries[country]
                elif country not in countries_list_corrected and country_similar:
                    country = country_similar[0]
                else:
                    garbage.add(country)

                country = country.title()
                ultimate_countries_list.append(country)

                # Filtering amounts
                amounts = re.sub(r'\s*\((.*?)\)\s*', '', amounts)
                amounts = re.sub(r'[^\d\s]', '', amounts).strip()
                amounts = join_digits_into_numbers(amounts, no_of_columns)

                fields = [country] + amounts.split()
                if len(fields) == no_of_columns:
                    matched.append(','.join(fields))
                else:
                    no_match.append(' '.join(fields))
                    # print(amounts, '---', len(amounts.split()), '---', (no_of_columns-1), file.name, country)
            text = ','.join(header_list) + '\n' + '\n'.join(matched) + '\n' + '\n'.join(no_match)
            with open(f'input-data/text-files/after-cleaning/{file.name[:-4]}.csv', 'w') as f_w:
                f_w.write(text)

    ultimate_countries_list = list(set(ultimate_countries_list))
    print(sorted(list(garbage)))

    # print(sorted(ultimate_countries_list))
    # print(len(ultimate_countries_list))
    # print(sorted(ultimate_countries_list))

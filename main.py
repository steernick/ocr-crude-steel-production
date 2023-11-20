from pathlib import Path
from myfunctions import *
from collections import Counter


if __name__ == "__main__":

    txt_directory = 'input-data/text-files'
    files = Path(txt_directory).glob('*.txt')

    countries_list = []

    for file in files:
        with open(file, 'r') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines if line.strip()]
            for line in lines[1:]:
                line = line.replace(',', '').lower()
                country = extract_country_from_row(line)
                country = filter_out_garbage(country)
                countries_list.append(country)

    countries_counter = Counter(countries_list)
    filtered_countries = [key for key, value in countries_counter.items() if value > 2]
    filtered_countries = list(sorted(filter(lambda x: len(x) > 3 and x not in ('cis', 'cls'), filtered_countries)))

    # print(*filtered_countries, sep='\n')
    # print(len(filtered_countries))

    files = Path(txt_directory).glob('*.txt')
    for file in files:
        with open(file, 'r') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines if line.strip()]
            header = lines[0] = 'Country ' + lines[0]
            header_list = header.split()
            matched = []
            no_match = []
            for line in lines[1:]:
                line = line.replace(',', '').lower()
                country = extract_country_from_row(line)
                amounts = line.replace(country, '').strip()
                country = filter_out_garbage(country)
                country_similar = find_similar_words_jaccard(country, filtered_countries, 0.9)
                for c in country_similar:
                    if country in country_similar:
                        continue
                    elif country not in country_similar and c in country:
                        country = f'!{country}--{c}!'
                    else:
                        country = f'!{country}!'
                amounts = filter_out_garbage(amounts)
                fields = [country] + amounts.split()
                if len(fields) == len(header_list):
                    matched.append(','.join(fields))
                else:
                    no_match.append(' '.join(fields))
            text = ','.join(header_list) + '\n' + '\n'.join(matched) + '\n' + '\n'.join(no_match)
            with open(f'input-data/text-files/after-cleaning/{file.name}', 'w') as f_w:
                f_w.write(text)
    print(text)

    # countries_list = list(set(countries_list))
    # countries_bad = [c for c in countries_list if c.startswith('?') and c.endswith('?')]
    # countries_bad2 = [c for c in countries_list if c.startswith('!') and c.endswith('!')]
    # countries_list = [c for c in countries_list if not c.startswith('?') and not c.endswith('?') and not c.startswith('!') and not c.endswith('!')]
    # print(list(sorted(countries_list)))
    # print(len(countries_list))
    # print(countries_bad)
    # print(len(countries_bad))
    # print(countries_bad2)
    # print(len(countries_bad2))


    # print(all_countries)
    # print(len(all_countries))
    # print(sorted(all_countries))
    # print(sorted(all_countries, key=len))

    # for file in files:
    #     with open(file, 'r') as f:
    #         text = f.read()
    #         text = remove_empty_lines(text)
    #         text = 'Country ' + text
    #         text = text.replace(',', '')
    #         lines = text.splitlines()
    #         header = lines[0].split()
    #         matched = []
    #         no_match = []
    #         list_of_countries = []
    #         for line in lines[1::]:
    #             country = extract_country_from_row(line)
    #             list_of_countries.append(country)
    #             fields = line.split()
    #             if len(fields) == len(header):
    #                 matched.append(','.join(fields))
    #             else:
    #                 no_match.append(' '.join(fields))
    #         text = ','.join(header) + '\n' + '\n'.join(matched) + '\n' + '\n'.join(no_match)
    #
    #         all_countries += list_of_countries
    #         all_countries = list(set(map(str.upper, all_countries)))
    #         all_countries = list(set(map(filter_out_garbage, all_countries)))
    #         all_countries = list(filter(lambda x: len(x) > 3, all_countries))
    #
    #         with open(f'input-data/text-files/after-cleaning/{file.name}', 'w') as f_w:
    #             f_w.write(text)

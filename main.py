from pathlib import Path
from myfunctions import extract_country_from_row, filter_out_garbage, find_similar_words_jaccard
from collections import Counter


if __name__ == "__main__":

    txt_directory = 'input-data/text-files'
    files = Path(txt_directory).glob('*.txt')

    countries_list = []
    ultimate_countries_list = []
    # count_of_lines1 = 0
    # count_of_lines2 = 0

    for file in files:
        with open(file, 'r') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines if line.strip()]
            for line in lines[1:]:
                line = line.replace(',', '').lower()
                country = extract_country_from_row(line)
                country = filter_out_garbage(country)
                countries_list.append(country)
                # count_of_lines1 += 1

    # re_country_patterns = [r'^(?:[A-Za-z.-]{3,}\s+){0,2}[A-Za-z.-]{3,}$']

    countries_counter = Counter(countries_list)
    filtered_countries = sorted([key for key, value in countries_counter.items() if value > 2])

    print(len(filtered_countries))
    print(filtered_countries)

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
                count_of_lines2 += 1
                line = line.replace(',', '').lower()
                country = extract_country_from_row(line)
                amounts = line.replace(country, '').strip()
                country = filter_out_garbage(country)
                for elem in country.split():
                    if elem in filtered_countries:
                        country = elem
                country_similar = find_similar_words_jaccard(country, filtered_countries, 0.85)
                # country_similar_dict = similar_words_with_jaccard_similarity(country, country_similar)
                if country not in filtered_countries and country_similar:
                    country = country_similar[0]
                elif country not in filtered_countries:
                    print(country, file.name)

                # else:
                #     for elem in country.split():
                #         if country_similar:
                #             country = country_similar[0]
                #         else:
                #             country = f'!{country}'
                ultimate_countries_list.append(country)
                amounts = filter_out_garbage(amounts)
                fields = [country] + amounts.split()
                if len(fields) == len(header_list):
                    matched.append(','.join(fields))
                else:
                    no_match.append(' '.join(fields))
            text = ','.join(header_list) + '\n' + '\n'.join(matched) + '\n' + '\n'.join(no_match)
            with open(f'input-data/text-files/after-cleaning/{file.name}', 'w') as f_w:
                f_w.write(text)

    ultimate_countries_list = list(set(ultimate_countries_list))
    diff = [x for x in filtered_countries if x not in ultimate_countries_list]

    print(sorted(ultimate_countries_list))
    print(len(ultimate_countries_list))
    print(diff)
    print(count_of_lines1)
    print(count_of_lines2)

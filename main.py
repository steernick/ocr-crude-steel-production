from pathlib import Path
from myfunctions import *

if __name__ == "__main__":

    txt_directory = 'input-data/text-files'
    files = Path(txt_directory).glob('*.txt')

    chars_to_remove = '''!@#$%^&*()-—=_+{}[]:;"'|\?/><~`£«»°'''
    pattern = '.{4}'

    all_countries = []
    for file in files:
        with open(file, 'r') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines if line.strip()]
            header = lines[0] = 'Country ' + lines[0]
            header_list = header.split()
            matched = []
            no_match = []
            for line in lines[1:]:
                line = line.replace(',', '')
                country = extract_country_from_row(line).lower()
                country = filter_out_garbage(country)
                fields = line.split()
                if country not in all_countries and len(country) > 3:
                    all_countries.append(country)
                    with open('input-data/all-countries-list.txt', 'a') as f_w:
                        f_w.write(country + '\n')
                if len(fields) == len(header_list):
                    matched.append(','.join(fields))
                else:
                    no_match.append(' '.join(fields))
            text = ','.join(header_list) + '\n' + '\n'.join(matched) + '\n' + '\n'.join(no_match)
            with open(f'input-data/text-files/after-cleaning/{file.name}', 'w') as f_w:
                f_w.write(text)


    print(all_countries)
    print(len(all_countries))
    print(sorted(all_countries))
    print(sorted(all_countries, key=len))

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

from pathlib import Path
import re
import string

txt_directory = 'input-data/text-files'
files = Path(txt_directory).glob('*.txt')

chars_to_remove = '''!@#$%^&*()-—=_+{}[]:;"'|\?/><~`£«»°'''
pattern = '.{4}'


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
    unwanted = ['(E', '(', ')', '(E:']
    for elem in elem_list:
        if elem in unwanted or len(elem) < 2:
            elem_list.remove(elem)
    return ' '.join(elem_list)


all_countries = []

for file in files:
    with open(file, 'r') as f:
        text = f.read()
        text = remove_empty_lines(text)
        text = 'Country ' + text
        text = text.replace(',', '')
        lines = text.splitlines()
        header = lines[0].split()
        matched = []
        no_match = []
        list_of_countries = []
        for line in lines[1::]:
            list_of_countries.append(extract_country_from_row(line))
            fields = line.split()
            if len(fields) == len(header):
                matched.append(','.join(fields))
            else:
                no_match.append(' '.join(fields))
        text = ','.join(header) + '\n' + '\n'.join(matched) + '\n' + '\n'.join(no_match)
        with open(f'input-data/text-files/after-cleaning/{file.name}', 'w') as f_w:
            f_w.write(text)
    all_countries += list_of_countries
print(all_countries)
print(len(all_countries))
all_countries = list(set(map(str.upper, all_countries)))
print(sorted(all_countries, key=len))
print(len(all_countries))
all_countries = list(set(map(filter_out_garbage, all_countries)))
print(sorted(all_countries, key=len))
print(len(all_countries))
all_countries = list(filter(lambda x: len(x) > 3, all_countries))
print(sorted(all_countries, key=len))
print(len(all_countries))



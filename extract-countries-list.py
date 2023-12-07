from pathlib import Path
from myfunctions import (is_element_in_string, extract_country_from_line)
from collections import Counter

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

    text = '\n'.join(lines)
    with open(f'input-data/after-first-filter/{file.name[:-4]}.txt', 'w') as f_w:
        f_w.write(text)

countries_counter = Counter(countries_list)
filtered_countries = sorted([key for key, value in countries_counter.items() if value > 2])

with open('input-data/countries_list.txt', 'w') as f_cl:
    for c in filtered_countries:
        f_cl.write("%s\n" % c)


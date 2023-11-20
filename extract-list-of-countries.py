from pathlib import Path
from myfunctions import extract_country_from_row, filter_out_garbage, matches_pattern

txt_directory = 'input-data/text-files'
files = Path(txt_directory).glob('*.txt')
# re_country_patterns = [r'^[A-Za-z.-]+(?:\s+[A-Za-z.-]+){0,2}$']
re_country_patterns = [r'^(?:[A-Za-z.-]{3,}\s+){0,2}[A-Za-z.-]{3,}$']

match = []
no_match = []

for file in files:
    with open(file, 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines if line.strip()]
        for line in lines[1:]:
            country = extract_country_from_row(line).lower()
            country = filter_out_garbage(country)
            if matches_pattern(country, re_country_patterns) and len(country) > 3:
                match.append(country)
            else:
                no_match.append(country)

match = sorted(list(set(match)))
no_match = sorted(list(set(no_match)))

with open('input-data/matched-countries1.txt', 'w') as f_w:
    for country in match:
        f_w.write(country + '\n')

with open('input-data/no-match-countries2.txt', 'w') as f_w:
    for country in no_match:
        f_w.write(country + '\n')


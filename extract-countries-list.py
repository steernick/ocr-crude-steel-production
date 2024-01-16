from pathlib import Path
from main import extract_country_from_line
from collections import Counter


# Function definition
def is_element_in_string(string, string_list):
    return any(element in string for element in string_list)


# Path to raw .txt files from previous stage
txt_directory = 'input-data/raw-text-files'
files = Path(txt_directory).glob('*.txt files')

# Declaration of lists variables
countries_list = []

# Declaration of unwanted words for filtering
unwanted_str_list = ['total', 'table', 'includes', 'figure', 'figures', 'statistical', 'steel', 'which', 'estimated',
                     'crude', 'calculated', 'from', 'excluding', 'included', 'continued', 'eeSSSe']

# Extracting countries names from files and saving them into list
for file in files:
    with open(file, 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines if line.strip()]
        lines = [line for line in lines if len(line) > 35]
        lines = [line for line in lines if not is_element_in_string(line.lower(), unwanted_str_list)]
        for line in lines[1:]:
            if not line[0].isnumeric():
                country = extract_country_from_line(line).lower()
            if len(country) > 2:
                countries_list.append(country)

    # saving text after preliminary filter into .txt files
    text = '\n'.join(lines)
    with open(f'input-data/after-first-filter/{file.name[:-4]}.txt files', 'w') as f_w:
        f_w.write(text)

# Creating Counter to count number of occurrences of each country in text
countries_counter = Counter(countries_list)

# Filtering countries list to reject countries or some string that have less than 3 occurrences
filtered_countries = sorted([key for key, value in countries_counter.items() if value > 2])

# saving list of countries into .txt file
with open('input-data/countries_list.txt', 'w') as f_cl:
    for c in filtered_countries:
        f_cl.write("%s\n" % c)


from itertools import accumulate
from collections import Counter
# from pathlib import Path
# from myfunctions import extract_country_from_row, filter_out_garbage, matches_pattern
#
# txt_directory = 'input-data/text-files'
# files = Path(txt_directory).glob('*.txt')
# re_country_patterns = [r'^[A-Za-z.-]+(?:\s+[A-Za-z.-]+){0,2}$']
# re_country_patterns = [r'^(?:[A-Za-z.-]{3,}\s+){0,2}[A-Za-z.-]{3,}$']
#
# match = []
# no_match = []
#
# for file in files:
#     with open(file, 'r') as f:
#         lines = f.readlines()
#         lines = [line.strip() for line in lines if line.strip()]
#         for line in lines[1:]:
#             country = extract_country_from_row(line).lower()
#             country = filter_out_garbage(country)
#             if matches_pattern(country, re_country_patterns) and len(country) > 3:
#                 match.append(country)
#             else:
#                 no_match.append(country)
#
# match = sorted(list(set(match)))
# no_match = sorted(list(set(no_match)))
#
# with open('input-data/matched-countries1.txt', 'w') as f_w:
#     for country in match:
#         f_w.write(country + '\n')
#
# with open('input-data/no-match-countries2.txt', 'w') as f_w:
#     for country in no_match:
#         f_w.write(country + '\n')
#
# list1 = ['Accession Countries', 'Africa', 'Albania', 'Algeria', 'Angola', 'Argentina', 'Armenia', 'Asia', 'Australia', 'Austria', 'Azerbaijan', 'Baltic States', 'Bangladesh', 'Belarus', 'Belgium', 'Bosnia-Herzegovina', 'Brazil', 'Bulgaria', 'C.I.S', 'Canada', 'Central America', 'Chile', 'China', 'Cis', 'Cls', 'Colombia', 'Congo', 'Croatia', 'Cuba', 'Czech Republic', 'Czechoslovakia', 'Denmark', 'Dominican Republic', 'E.C. Total', 'East Germany', 'Eastern Europe', 'Ecuador', 'Egypt', 'El Salvador', 'Estonia', 'European Union', 'Finland', 'Former U.S.S.R', 'France', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Guatemala', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Ireland', 'Israel', 'Italy', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Latin America', 'Latvia', 'Libya', 'Lithuania', 'Luxembourg', 'Macedonia', 'Malaysia', 'Mauritania', 'Mexico', 'Middle East', 'Moldova', 'Mongolia', 'Montenegro', 'Morocco', 'Myanmar', 'Netherlands', 'New Zealand', 'Nigeria', 'North America', 'North Korea', 'Norway', 'Oceania', 'Oman', 'Other', 'Other Africa', 'Other Europe', 'Other Western Europe', 'Pakistan', 'Panama', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Rhodesia', 'Romania', 'Russia', 'Saudi Arabia', 'Serbia', 'Serbia And Montenegro', 'Singapore', 'Slovak Republic', 'Slovenia', 'South Africa', 'South America', 'South Korea', 'Spain', 'Sri Lanka', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Thailand', 'Total Africa', 'Total Asia', 'Total Developing Cts', 'Total Eastern Europe', 'Total Industrial Cts', 'Total Latin America', 'Total Middle East', 'Total Western Europe', 'Total Western World', 'Trinidad And Tobago', 'Tunisia', 'Turkey', 'U.S.S.R.', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Venezuela', 'Vietnam', 'West Germany', 'Western Europe', 'World', 'World Total', 'Yugoslavia', 'Zaire', 'Zimbabwe']
# list2 = ['Accession Countries', 'Africa', 'Albania', 'Algeria', 'Angola', 'Argentina', 'Armenia', 'Asia', 'Australia', 'Austria', 'Azerbaijan', 'Baltic States', 'Bangladesh', 'Belarus', 'Belgium', 'Bosnia-Herzegovina', 'Brazil', 'Bulgaria', 'Canada', 'Central America', 'Chile', 'China', 'Cis', 'Cls', 'Colombia', 'Congo', 'Croatia', 'Cuba', 'Czech Republic', 'Czechoslovakia', 'Denmark', 'Dominican Republic', 'E.C. Total', 'East Germany', 'Eastern Europe', 'Ecuador', 'Egypt', 'El Salvador', 'Estonia', 'European Union', 'Finland', 'Former U.S.S.R', 'France', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Guatemala', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Ireland', 'Israel', 'Italy', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Latin America', 'Latvia', 'Libya', 'Lithuania', 'Luxembourg', 'Macedonia', 'Malaysia', 'Mauritania', 'Mexico', 'Middle East', 'Moldova', 'Mongolia', 'Montenegro', 'Morocco', 'Myanmar', 'Netherlands', 'New Zealand', 'Nigeria', 'North America', 'North Korea', 'Norway', 'Oceania', 'Oman', 'Other', 'Other Africa', 'Other Europe', 'Other Western Europe', 'Pakistan', 'Panama', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Rhodesia', 'Romania', 'Russia', 'Saudi Arabia', 'Serbia', 'Serbia And Montenegro', 'Singapore', 'Slovak Republic', 'Slovenia', 'South Africa', 'South America', 'South Korea', 'Spain', 'Sri Lanka', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Thailand', 'Total Africa', 'Total Asia', 'Total Developing Cts', 'Total Eastern Europe', 'Total Industrial Cts', 'Total Latin America', 'Total Middle East', 'Total Western Europe', 'Total Western World', 'Trinidad And Tobago', 'Tunisia', 'Turkey', 'U.S.S.R.', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Venezuela', 'Vietnam', 'West Germany', 'Western Europe', 'World', 'World Total', 'Yugoslavia', 'Zaire', 'Zimbabwe']
# print([x for x in list1 if x not in list2])

# strings = '10 331 10 172 11 331 11606 10818 10739 11425 10931 98834 11 636 10 762'
# string_list = ['1', '343', '429', '1', '238', '755', '1', '433', '433', '1', '538', '003', '1', '560', '131',
#                '1650', '354', '1669', '450', '1620001', '1626954', '1', '690', '479']
# len_list = [len(s) for s in string_list]
# max_len_figure = max(len_list)
# count_max_len_figure = len_list.count(max_len_figure)
# figures_list = ['']
#
# for i in range(len(string_list)):
#     while len(figures_list[i]) < max_len_figure - 1:
#         figures_list[i] += [string_list[i] for i in range(len(string_list))]
#
# print(figures_list)



# print(len_list)
# print(dict(sorted(len_list_counter.items())))
# print(max_len_figure)
# print(count_max_len_figure)

'''
string_list = ['1', '343', '429', '1', '238', '755', '1', '433', '433', '1', '538', '003', '1', '560', '131',
               '1650', '354', '1669', '450', '1620001', '1626954', '1', '690', '479']

# Find the length of the longest string in the list
max_length = max(map(len, string_list))

# Concatenate strings until they have the desired length
result_list = [''.join(string_list[i:i+max_length]) for i in range(0, len(string_list), max_length)]

print(max_length)

print(result_list)

string_list = ['1', '343', '429', '1', '238', '755', '1', '433', '433', '1', '538', '003', '1', '560', '131',
               '1650', '354', '1669', '450', '1620001', '1626954', '1', '690', '479']

max_length = 7

result_list = []

current_string = ''

for s in string_list:
    if len(current_string) + len(s) < max_length:
        current_string += s
    else:
        result_list.append(current_string)
        current_string = s

# Append the last segment if any
if current_string:
    result_list.append(current_string)

print(result_list)
'''

string_list = ['1', '343', '429', '1', '238', '755', '1', '433', '433', '1', '538', '003', '1', '560', '131',
               '1650', '354', '1669', '450', '1620001', '1626954', '1', '690', '479']

min_length = 6
max_length = 7
result_list = []

# for s in string_list:
#     result_list.append(reduce(lambda x, y: x + y if len(x + y) <= max_length else x, string_list))


result_list = accumulate(string_list, func=lambda x, y: x + y if len(x + y) <= max_length else x)

print(list(result_list))


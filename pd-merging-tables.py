import pandas as pd
from pathlib import Path

# Path to .csv files
csv_directory = 'input-data/after-cleaning'
files = sorted(Path(csv_directory).glob('*.csv'), reverse=True)

# Initializing base dataframe with data from 2009 to 2019
df_all = pd.read_csv(f'{csv_directory}/2019.csv', delimiter=',', on_bad_lines='warn')

# Year variable
year = 2008

# Looping through .csv files and merging base dataframe with columns representing next (actually previous) year
for file in files[1:]:
    df = pd.read_csv(file, delimiter=',', on_bad_lines='warn')
    if str(year) not in df:
        continue
    else:
        df_all = df_all.merge(df[['Country', str(year)]], on='Country', how='outer')
        year -= 1
    df_all.drop_duplicates(inplace=True, keep=False, ignore_index=True)

# Adding '1951' column from last file (1960.csv)
df = pd.read_csv(f'{csv_directory}/1960.csv', delimiter=',', on_bad_lines='warn')
df_all = df_all.merge(df[['Country', '1951']], on='Country', how='outer')

# Sorting dataframe columns
df_all = df_all[['Country'] + sorted(df_all.iloc[:, 1:])]

# Exporting dataframe into .csv file
df_all.to_csv('input-data/csv-files/merged-1951-2018.csv', index=False)

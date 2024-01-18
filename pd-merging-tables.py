import pandas as pd
from pathlib import Path

csv_directory = 'input-data/after-cleaning'
files = sorted(Path(csv_directory).glob('*.csv'), reverse=True)
df_all = pd.read_csv('input-data/after-cleaning/2019.csv', delimiter=',', on_bad_lines='warn')
year = 2008

for file in files[1:]:
    df = pd.read_csv(file, delimiter=',', on_bad_lines='warn')
    if str(year) not in df:
        continue
    else:
        df_all = df_all.merge(df[['Country', str(year)]], on='Country', how='outer')
        year -= 1
    df_all.drop_duplicates(inplace=True, keep=False, ignore_index=True)

df_all = df_all[['Country'] + sorted(df_all.iloc[:, 1:])]

df_all.to_csv('input-data/csv-files/concat_try.csv', index=False)

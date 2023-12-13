import pandas as pd
from pathlib import Path

csv_directory = 'input-data/ready-to-merge'
files = Path(csv_directory).glob('*.csv')
df_all = pd.DataFrame({'Country': []})

for file in files:
    df = pd.read_csv(file, delimiter=',', on_bad_lines='warn')
    df_all = pd.merge(df_all, df, on='Country', how='outer')
    df_all.drop_duplicates(inplace=True, keep=False, ignore_index=True)

# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', '{:.2f}'.format)

df_all.sort_index(axis=1, inplace=True)
df_all.insert(0, 'Country', df_all.pop('Country'))

df_all.reset_index(drop=True, inplace=True)
print(df_all)
df_all.to_csv('input-data/csv-files/crude-steel-production.csv', index=False)

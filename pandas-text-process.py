import pandas as pd
from pathlib import Path

txt_directory = 'input-data/ready-to-pandas'
files = Path(txt_directory).glob('*.csv')
df_all = pd.DataFrame({'Country': []})
merged_df = pd.DataFrame({'Country': []})

for file in files:
    # file_name = str(int(file.name[:-4]) - 10) + '.csv'
    # Read CSV files and select specified columns
    dfs = pd.read_csv(file, usecols=[0, 1])
    # dfs.to_csv(f'input-data/ready-to-pandas/{file_name}', index=False)

    merged_df = pd.merge(merged_df, dfs, on='Country', how='outer')

merged_df = merged_df.drop_duplicates()

merged_df.sort_index(axis=1, inplace=True)
merged_df.insert(0, 'Country', merged_df.pop('Country'))
merged_df.to_csv('merged_result.csv', index=False)





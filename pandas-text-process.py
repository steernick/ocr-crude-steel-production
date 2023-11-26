import pandas as pd
from pathlib import Path

txt_directory = 'input-data/text-files/ready-to-pandas'
files = Path(txt_directory).glob('*.csv')
df_all = pd.DataFrame()

for file in files:
    df = pd.read_csv(file, delimiter=',', on_bad_lines='skip')
    df_all = pd.concat([df_all, df]).drop_duplicates(keep=False)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

df_all.sort_index(axis=1, inplace=True)
df_all.insert(0, 'Country', df_all.pop('Country'))

df_all[df_all.columns.difference(['Country'])] = df_all[df_all.columns.difference(['Country'])].apply(pd.to_numeric, errors='coerce')

# grouped_df = df_all.groupby(['Country', '2001']).size().reset_index(name='Count')

grouped_df = df_all.groupby('Country')['1987'].value_counts(dropna=True).reset_index(name='Count')

filtered_df = grouped_df[grouped_df['Count'] > 2]

df_new_all = pd.DataFrame()

for column in df_all.columns:
    grouped_df = df_all.groupby('Country')[column].value_counts(dropna=True).reset_index(name='Count')
    filtered_df = grouped_df[grouped_df['Count'] > 2]
    print(filtered_df.iloc[:, :3])
    df_new_all = pd.concat([df_new_all, filtered_df[:, :2]]).drop_duplicates()

# print(filtered_df.iloc[:, :3])
print(df_new_all.info())
print(df_new_all)

# print(grouped_df.info())
# print(grouped_df)
# print(df_all)
# print(df_all.iloc[:, ])
# df_all['Country'] = df_all['Country'].astype(str)
# print(df_all.dtypes)
# print(df_all[df_all.duplicated()])

df_new_all.to_csv('filtered_concatenated_rows.csv', index=False)

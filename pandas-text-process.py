import pandas as pd
from pathlib import Path

txt_directory = 'input-data/text-files/ready-to-pandas'
files = Path(txt_directory).glob('*.csv')
df_all = pd.DataFrame({'Country': []})

for file in files:
    df = pd.read_csv(file, delimiter=',', on_bad_lines='warn')
    df_all = pd.concat([df_all, df])
    df_all.drop_duplicates(inplace=True, keep=False, ignore_index=True)

# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', '{:.2f}'.format)

df_all.sort_index(axis=1, inplace=True)
df_all.insert(0, 'Country', df_all.pop('Country'))

df_all[df_all.columns.difference(['Country'])] = df_all[df_all.columns.difference(['Country'])].apply(pd.to_numeric, errors='coerce')

df_all.reset_index(drop=True, inplace=True)

for column in df_all.columns:
    grouped_df = df_all.groupby('Country')[column].value_counts(dropna=True).reset_index(name='Count')
    # print(grouped_df)

# df_sample_all = pd.DataFrame({'Country': []})
# df_sample = df_all[['Country', '1984', '1985', '1986', '1987', '1988', '1999', '2000']].copy()
#
# for column in df_sample.columns:
#     grouped_df = df_sample.groupby('Country')[column].value_counts(dropna=True).reset_index(name='Count')
#     filtered_df = grouped_df[grouped_df['Count'] > 2]
#     # print(filtered_df)
#     # df_new_all = pd.concat([df_new_all, filtered_df]).drop_duplicates()
#     df_sample_all = pd.merge(df_sample_all, filtered_df.iloc[:, :2], on='Country', how='outer')

df_new_all = pd.DataFrame({'Country': []})

for column in df_all.columns[1:]:  # Exclude 'Country' column
    # Group by 'Country' and the current column, calculate value counts, and reset index
    grouped_df = df_all.groupby(['Country', column]).size().reset_index(name='Count')
    print(grouped_df)
    # Find the row with the maximum count for each 'Country'
    max_count_idx = grouped_df.groupby('Country')['Count'].idxmax()
    filtered_df = grouped_df.loc[max_count_idx, ['Country', column]]

    # Merge the results into the new DataFrame
    df_new_all = pd.merge(df_new_all, filtered_df, on='Country', how='outer')

# Drop duplicate rows from the new DataFrame
df_new_all = df_new_all.drop_duplicates()

print(df_new_all)

df_new_all.to_csv('filtered_concatenated_rows.csv', index=False)
# df_sample_all.to_csv('sample_concatenated_rows.csv', index=False)

df_all.to_csv('concatenated_rows.csv', index=False)

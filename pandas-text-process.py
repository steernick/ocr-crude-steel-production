import pandas as pd
from pathlib import Path

txt_directory = 'input-data/ready-to-pandas'
files = Path(txt_directory).glob('*.csv')
df_all = pd.DataFrame({'Country': []})
merged_df = pd.DataFrame({'Country': []})

for file in files:

    # Read CSV files and select specified columns
    dfs = pd.read_csv(file, usecols=[0, 2])

    # Merge dataframes horizontally
    merged_df = pd.merge(merged_df, dfs, how='outer')

# Save the merged dataframe to a new CSV file
# merged_df = merged_df[sorted(merged_df.columns)]
merged_df = merged_df.drop_duplicates()
df_2011_17 = pd.read_csv(f'{txt_directory}/2019.csv', usecols=[0, 3, 4, 5, 6, 7, 8, 9])
merged_df = pd.merge(merged_df, df_2011_17, on="Country", how='outer')
merged_df.sort_index(axis=1, inplace=True)
merged_df.insert(0, 'Country', merged_df.pop('Country'))
merged_df.to_csv('merged_result.csv', index=False)


# pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', '{:.2f}'.format)

# print(merged_df)

df_all.sort_index(axis=1, inplace=True)
df_all.insert(0, 'Country', df_all.pop('Country'))

# df_all[df_all.columns.difference(['Country'])] = df_all[df_all.columns.difference(['Country'])].apply(pd.to_numeric, errors='coerce')

df_all.reset_index(drop=True, inplace=True)

df_new_all = pd.DataFrame({'Country': []})

for column in df_all.columns[1:]:  # Exclude 'Country' column
    # Group by 'Country' and the current column, calculate value counts, and reset index
    grouped_df = df_all.groupby(['Country', column]).size().reset_index(name='Count')
    # print(grouped_df)
    # Find the row with the maximum count for each 'Country'
    max_count_idx = grouped_df.groupby('Country')['Count'].idxmax()
    filtered_df = grouped_df.loc[max_count_idx, ['Country', column]]
    # Merge the results into the new DataFrame
    # print(grouped_df)
    df_new_all = pd.merge(df_new_all, filtered_df, on='Country', how='outer')

# Drop duplicate rows from the new DataFrame
df_new_all = df_new_all.drop_duplicates()

# print(df_new_all)

df_new_all.to_csv('filtered_concatenated_rows.csv', index=False)
# df_sample_all.to_csv('sample_concatenated_rows.csv', index=False)

df_all.to_csv('concatenated_rows.csv', index=False)

# merged_df.to_csv('merged_tables.csv', index=False)
# _1980 = pd.read_csv(f'{txt_directory}/1980.csv')
# _1982 = pd.read_csv(f'{txt_directory}/1982.csv')
# merge_try_df = pd.merge(_1980, _1982, how='outer')
# print(merge_try_df)
# merge_try_df.to_csv('merge_try_df.csv', index=False)


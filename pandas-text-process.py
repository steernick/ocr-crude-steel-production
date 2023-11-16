import pandas as pd

txt_directory = 'input-data/text-files'

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

df = pd.read_csv(f'{txt_directory}/2001.txt', delimiter=',', on_bad_lines='warn')

print(df)

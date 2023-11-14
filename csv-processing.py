import numpy as np
import pandas as pd
from pathlib import Path


directory = 'crude-steel-production'
files = Path(directory).glob('*.csv')
file = f'{directory}/2000.csv'

df1 = pd.read_csv(file,)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

print(df1)
# pd.merge()
# for file in files:
#     pd.read_csv(file)
#     tabula.convert_into(file, output_path=f"{directory}/{file.name[-8:-4]}.csv", output_format="csv", pages='all')
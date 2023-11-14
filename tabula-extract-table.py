import tabula
import pandas as pd
from pathlib import Path

'''
directory = 'crude-steel-production'
text = ''
files = Path(directory).glob('*.pdf')

for file in files:
    tabula.convert_into(file, output_path=f"{directory}/{file.name[-8:-4]}.csv", output_format="csv", pages='all')
'''
pd.set_option('display.max_columns', None)

file = 'Steel-Statistical-Yearbook-1980-8-2.pdf'

df = tabula.read_pdf(file, stream=True, pages='all', multiple_tables=True)

df = pd.concat(df, ignore_index=True)


print(df.head(10))

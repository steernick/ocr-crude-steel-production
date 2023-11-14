from pypdf import PdfReader
from pathlib import Path
import re

directory = 'crude-steel-production'
text = ''
files = Path(directory).glob('*2005.pdf')

for file in files:
    reader = PdfReader(file)
    for page in reader.pages:
        text += page.extract_text()

csv_header = text.splitlines()[1]
csv_header = 'Country,'+csv_header.replace(' ', ',')

csv_lines = []
csv_garbage = []

for line in text.splitlines(keepends=True):
    if line[0].isalpha():
        csv_lines.append(line)
    else:
        csv_garbage.append(line)
print(csv_header)
for line in csv_lines:
    country = re.findall('\D+ \D*', line)
    figures = list(filter(len, re.findall('\d*', line)))
    if len(figures) == 20:
        figures = [figures[i] + figures[i+1] for i in range(0, len(figures), 2)]
    # elif 20 > len(figures) > 10:
        # for i in range(len(figures)):
        #     if len(figures[i+1]) == 3 < len(figures[i])-1:
        #         figures[i-1] += figures[i]
        #         figures.pop(i)
        # for i in reversed(range(len(figures))):
        #     if len(figures[i-1]) < len(figures[i])-1:
        #         figures[i-1] += figures[i]
        #         figures.pop(i)
    if len(figures) == 10:
        line = country[0].strip() + ',' + ','.join(figures)
    # print(country[0].strip(),figures)
    print(line)












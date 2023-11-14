from pypdf import PdfReader
from pathlib import Path


directory = 'crude-steel-production'
text = ''
files = Path(directory).glob('*2001.pdf')

for file in files:
    reader = PdfReader(file)
    for page in reader.pages:
        text += page.extract_text()

with open(f'{directory}/2001.txt', 'w') as f:
    f.write(text)

from pypdf import PdfWriter
from pathlib import Path

directory = 'crude-steel-production'

files = Path(directory).glob('*.pdf')

merger = PdfWriter()

for pdf in files:
    merger.append(pdf)

merger.write(stream=f'{directory}/crude-steel-production-merged.pdf')
merger.close()

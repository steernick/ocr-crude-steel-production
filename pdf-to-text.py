from pdf2image import convert_from_path
import pytesseract
from pathlib import Path

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'/Users/Robert/miniconda3/envs/sm/bin/tesseract'

# Path PDF file
pdf_directory = 'input-data/tables-in-pdf'
files = Path(pdf_directory).glob('*.pdf')

# Path txt files
txt_directory = 'input-data/text-files'

# Convert all PDFs in directory to images using pdf2image
# Extract text using pytesseract and save it into separate .txt files

for file in files:
    images = convert_from_path(file)
    for image in images:
        text = pytesseract.image_to_string(image, config='--psm 6')
        with open(f'input-data/text-files/{file.name[-8:-4]}.txt', 'a') as f:
            f.write(text)
'''
def tesseract_pdf_to_txt(pdf_path: str | PathLike[str],
                         output_folder = str | PathLike[str]):
                         
'''
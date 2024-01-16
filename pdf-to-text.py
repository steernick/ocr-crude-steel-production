from pdf2image import convert_from_path
import pytesseract
from pathlib import Path

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'/Users/Robert/miniconda3/envs/sm/bin/tesseract'

# Path to .pdf files
pdf_directory = 'input-data/tables-in-pdf/cropped'
files = Path(pdf_directory).glob('*.pdf')

# Path to .txt files
txt_directory = 'input-data/raw-text-files'

# Custom configuration of pytesseract
custom_config = r'--oem 3 --psm 6 -c preserve_interword_spaces=1'

# Convert all PDFs in directory to images using pdf2image
for file in files:
    images = convert_from_path(file)
    # Extract text using pytesseract and save it into separate .txt files
    for image in images:
        text = pytesseract.image_to_string(image, config=custom_config)
        with open(f'{txt_directory}/{file.name[-8:-4]}.txt', 'a') as f:
            f.write(text)

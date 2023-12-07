from pdf2image import convert_from_path
import pytesseract
from pathlib import Path

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'/Users/Robert/miniconda3/envs/sm/bin/tesseract'

# Path PDF file
pdf_directory = 'input-data/tables-in-pdf/cropped'
files = Path(pdf_directory).glob('*.pdf')

# Path txt files
txt_directory = 'input-data/text-files'

# Custom configuration of pytesseract
custom_config = r'--oem 3 --psm 6 -c preserve_interword_spaces=1'

# Convert all PDFs in directory to images using pdf2image
# Extract text using pytesseract and save it into separate .txt files
for file in files:
    images = convert_from_path(file)
    for image in images:
        text = pytesseract.image_to_string(image, config=custom_config)
        with open(f'input-data/raw-text-files/{file.name[-8:-4]}.txt', 'a') as f:
            f.write(text)

from pdf2image import convert_from_path
import pytesseract
import pandas as pd
from PIL import Image


# Path to the Tesseract executable (update with your path)
pytesseract.pytesseract.tesseract_cmd = r'/Users/Robert/miniconda3/envs/sm/bin/tesseract'

# Path to your PDF file
pdf_path = 'crude-steel-production/Steel-Statistical-Yearbook-1981.pdf'

# Convert the PDF to images using pdf2image
images = convert_from_path(pdf_path)

# Initialize an empty string to store extracted text
extracted_text = ''

df = pd.DataFrame

# Iterate over the images and extract text using Tesseract
'''for i, image in enumerate(images):
    text = pytesseract.image_to_string(image)
    extracted_text += f'Page {i+1}:\n{text}\n\n'
    extracted_text += text'''

for image in images:
    text = pytesseract.image_to_string(image, config='--psm 6')
    extracted_text += text

print(extracted_text)

# Print or use the extracted text as needed
# print(extracted_text)

# Save the extracted text to a file for reference (optional)
#with open('output.txt', 'w') as file:
    #file.write(extracted_text)

# Use tabula to extract tables from the OCR'd text
#tables = tabula.read_pdf('output.txt', pages='all', multiple_tables=True, columns=[2008.0,2009.0,2010.0,2011.0,2012.0,2013.0,2014.0,2015.0,2016.0,2017.0])

# Print or use the extracted tables as needed
#for i, table in enumerate(tables):
    #print(f'Table {i + 1}:\n{table}\n')
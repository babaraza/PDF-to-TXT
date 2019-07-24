from wand.image import Image
from PIL import Image as PIL_Image
import pytesseract
from pathlib import Path

# Requirements:
# Tesseract from https://github.com/UB-Mannheim/tesseract/wiki
# ImageMagick from https://imagemagick.org/script/download.php#windows
# GhostScript from https://www.ghostscript.com/download/gsdnld.html
# pip install wand
# pip install pillow
# pip install pytesseract

# Show where Tesseract is installed for pytesseract to work
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

source_dir = Path()
source_files = source_dir.glob('*.pdf')  # Search for all pdf files

# Go through each pdf file and convert to JPG
for file in source_files:
    with Image(filename=str(file), resolution=200) as pdf:
        pdf.compression_quality = 99
        pdf.format = 'jpg'
        pdf.save(filename=file.stem+'.'+pdf.format)  # file stem is name of file without ext

# Go through each JPG file, perform OCR on it, save as text file
for image in source_dir.glob('*.jpg'):
    text = pytesseract.image_to_string(PIL_Image.open(image))
    with open('Converted.txt', 'a') as txt:  # 'a' mode allows us to append to text file
        txt.write(text)

print("Done")

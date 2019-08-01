from wand.image import Image
from PIL import Image as PI
import pytesseract
from pathlib import Path
import numpy as np
import cv2

# Requirements:
# Tesseract from https://github.com/UB-Mannheim/tesseract/wiki
# ImageMagick from https://imagemagick.org/script/download.php#windows
# GhostScript from https://www.ghostscript.com/download/gsdnld.html
# pip install wand
# pip install pillow
# pip install pytesseract
# pip install numpy
# pip install opencv-python

# Show where Tesseract is installed for pytesseract to work
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

source_dir = Path()
source_files = source_dir.glob('*.pdf')  # Search for all pdf files

# to avoid creating and deleting a temporary file for each image we use numpy and OpenCV
# to extract the image as a blob, convert it to a numpy array and then turn it into a PIL image
# for pytesseract to perform OCR

# TODO: Get Page 2 to work

req_image = []
final_text = []

for file in source_files:
    with Image(filename=str(file), resolution=200) as img:
        for image in img.sequence:
            image.format = 'jpg'
            image.compression_quality = 99
            img_page = Image(image=image)
            img_buffer = np.asarray(bytearray(img_page.make_blob()))
            img_data = cv2.imdecode(img_buffer, cv2.IMREAD_GRAYSCALE)
            final_text.append(pytesseract.image_to_string(PI.fromarray(img_data)))
    filename = '{}.txt'.format(file.stem)
    with open(filename, 'a') as txt:
        txt.writelines(final_text)

print("Done")

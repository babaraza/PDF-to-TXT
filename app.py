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

# Set where Tesseract is installed for pytesseract to work
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
source_dir = Path()  # Setting Path to the app directory
final_text = []  # Empty array to hold the OCR data


def get_files():
    print("Finding all PDF files")
    source_files = source_dir.glob('*.pdf')  # Search for all pdf files

    for pdf_file in source_files:
        print(f"Converting {pdf_file} into JPG sequence")

        # Wand Image creates an image for each page of the pdf file as sequence
        with Image(filename=str(pdf_file), resolution=200) as img:

            # Going through each image[pdf file page] as SingleImage
            print("Converting and applying OCR on each page")
            for image in img.sequence:
                image.format = 'jpg'
                image.compression_quality = 99

                # Convert SingleImage to Wand Image
                img_page = Image(image=image)

                # Convert the Wand Image into a Blob, then into a Numpy Array
                img_buffer = np.asarray(bytearray(img_page.make_blob()))

                # Open Numpy Array image in CV2 and run grayscale filter
                img_data = cv2.imdecode(img_buffer, cv2.IMREAD_GRAYSCALE)

                # Convert the Numpy Array into a Pillow image for Pytesseract
                final_text.append(pytesseract.image_to_string(PI.fromarray(img_data)))

                # Add extra lines after each page
                final_text.append('\n\n')

        save_data(final_text, pdf_file)


def save_data(ocr_data, pdf_file_name):
    # Creating Text file with same name as the source pdf file
    filename = '{}.txt'.format(pdf_file_name.stem)

    print("Creating text file with OCR data")
    # 'a' mode allows us to append to text file
    with open(filename, 'a') as txt:
        txt.writelines(ocr_data)
    print("\n")


get_files()
print("Done")

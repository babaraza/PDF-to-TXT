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


def get_files():
    source_files = source_dir.glob('*.pdf')  # Search for all pdf files
    # Go through each pdf file and convert to JPG
    for file in source_files:
        with Image(filename=str(file), resolution=200) as img:
            print("Converting PDF to JPG")
            img.compression_quality = 99
            img.format = 'jpg'
            # file stem is name of file without ext
            img.save(filename="{}.{}".format(file.stem, img.format))
            ocr_file(file.stem)


# Go through each JPG file, perform OCR on it, save as text file
def ocr_file(orig_filename):
    print("Applying OCR on JPG (s)")
    for image in source_dir.glob(f'{orig_filename}*.jpg'):
        text = pytesseract.image_to_string(PIL_Image.open(image))
        filename = '{}.txt'.format(orig_filename)
        # 'a' mode allows us to append to text file
        with open(filename, "a") as txt:
            txt.write(f'{text}\n\n')
    if input("Delete JPG(s)? > ").lower() == "y":
        print("Deleting Temporary Images")
        for temp_img in source_dir.glob('*.jpg'):
            temp_img.unlink()  # Delete jpg(s) that were created
    else:
        print("Ending Program")


get_files()
print("Done")

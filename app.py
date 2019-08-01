from wand.image import Image
from PIL import Image as PIL_Image
import pytesseract
from pathlib import Path
import shutil

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
temp_dir = Path('temp/')


def get_files():
    try:
        temp_dir.mkdir()
        print("Creating Temporary Folder")
    except:
        print("Received an Error when trying to create Temporary Folder")

    print("Finding all PDF files")
    source_files = source_dir.glob('*.pdf')  # Search for all pdf files

    # Go through each pdf file and convert to JPG
    for file in source_files:
        with Image(filename=str(file), resolution=200) as img:
            print("Converting PDF(s) to JPG(s)")
            img.compression_quality = 99
            img.format = 'jpg'

            # Saving jpg with the same name as the source pdf file
            # File stem is name of file without extension
            img.save(filename="{}/{}.{}".format(temp_dir, file.stem, img.format))

            # Sending filename of the pdf file to next function
            # Since images will have the same name
            ocr_file(file.stem)


# Go through each JPG file, perform OCR on it, save as text file
def ocr_file(orig_filename):
    print("Applying OCR on JPG(s)")

    # Using source pdf file name to search for same named images
    for image in temp_dir.glob(f'{orig_filename}*.jpg'):

        # Using Wand to open jpg, casting into Pillow
        # Since pytesseract accepts PIL images
        text = pytesseract.image_to_string(PIL_Image.open(image))

        # Creating text file with the same name as source pdf
        filename = '{}/{}.txt'.format(source_dir, orig_filename)

        print("Creating text file with OCR data")
        # 'a' mode allows us to append to text file
        with open(filename, "a") as txt:
            txt.write(f'{text}\n\n')

    # Ask to delete Temp folder with JPG(s)
    if input("Delete JPG(s)? > ").lower() == "y":
        print("Deleting Temporary Folder")
        shutil.rmtree(temp_dir, ignore_errors=True)
    else:
        print("Ending Program")


get_files()
print("Done")

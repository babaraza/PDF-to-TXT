[![Python 3.7](https://img.shields.io/badge/Python-3.6-blue.svg)](https://www.python.org/downloads/release/python-374/)

# PDF to TXT
Convert PDF files to Text by performing OCR powered by `Tesseract`

### Requirements
- Tesseract from https://github.com/UB-Mannheim/tesseract/wiki
- ImageMagick from https://imagemagick.org/script/download.php#windows
- GhostScript from https://www.ghostscript.com/download/gsdnld.html
- Wand `pip install wand`
- Pillow `pip install pillow`
- PyTesseract `pip install pytesseract`
- Numpy `pip install numpy`
- OpenCV `pip install opencv-python`

### Usage

Run `app.py` in folder with PDF files

Script will follow these steps:
- Search for all PDF files in folder using `glob()`
- Wand `Image()` creates an image for each page of the pdf file as sequence
- Goes through each image in above sequence as `SingleImage`
- Convert `SingleImage` to Wand `Image`
- Convert the Wand `Image` into a Blob using `make_blob()`
- Convert `Blob` into a Numpy Array `np.asarray()`
- Open Numpy Array image in `CV2` using `cv2.imdecode()`
- Run grayscale filter on image `cv2.IMREAD_GRAYSCALE`
- Convert the Numpy Array into a `Pillow` image
- Run `Pytesseract` on `Pillow` image
- Append each page to a text file

*The Text file is created with the same name as the source **PDF file***
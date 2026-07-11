"""
morph.converters.image_converter - Convert images to text using OCR.

This module uses Tesseract OCR (via pytesseract) to extract text
from image files. Useful for reading text from screenshots,
scanned documents, or photos of text.

Requirements:
    - pytesseract (Python library)
    - Tesseract OCR (system package) must be installed
      Install with: sudo apt install tesseract-ocr (Linux)
                    brew install tesseract (macOS)
"""

import os

# We use try/except for imports to give clear error messages
# if the required libraries are not installed
try:
    # 'pytesseract' is a Python wrapper for the Tesseract OCR engine
    import pytesseract

    # 'PIL' (Pillow) is used to open and process image files
    from PIL import Image

    # Flag to track if OCR libraries are available
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


def image_to_text(image_path):
    """
    Extract text from an image file using OCR (Optical Character Recognition).

    This function:
        1. Checks that the required libraries are installed
        2. Opens the image file
        3. Runs OCR to detect and extract text
        4. Returns the extracted text

    Parameters:
        image_path (str): Path to the image file to process.

    Returns:
        dict: A dictionary containing:
            - 'success' (bool): Whether the conversion succeeded.
            - 'image_path' (str): The path to the image that was processed.
            - 'text' (str): The extracted text content.
            - 'word_count' (int): Number of words found.
            - 'error' (str or None): Error message if conversion failed.
    """

    # ---- Step 1: Check that OCR libraries are installed ----
    if not OCR_AVAILABLE:
        return {
            "success": False,
            "image_path": image_path,
            "text": "",
            "word_count": 0,
            "error": (
                "OCR libraries not installed. "
                "Please install them with: pip install pytesseract Pillow\n"
                "Also install Tesseract OCR: sudo apt install tesseract-ocr"
            ),
        }

    # ---- Step 2: Check that the image file exists ----
    if not os.path.exists(image_path):
        return {
            "success": False,
            "image_path": image_path,
            "text": "",
            "word_count": 0,
            "error": f"Image file not found: '{image_path}'",
        }

    try:
        # ---- Step 3: Open the image ----
        image = Image.open(image_path)

        # ---- Step 4: Run OCR to extract text ----
        # pytesseract.image_to_string() sends the image to Tesseract
        # and returns the detected text
        extracted_text = pytesseract.image_to_string(image)

        # ---- Step 5: Clean up the text ----
        clean_text = extracted_text.strip()

        # ---- Step 6: Count words ----
        word_count = len(clean_text.split()) if clean_text else 0

        return {
            "success": True,
            "image_path": image_path,
            "text": clean_text,
            "word_count": word_count,
            "error": None,
        }

    except Exception as error:
        return {
            "success": False,
            "image_path": image_path,
            "text": "",
            "word_count": 0,
            "error": f"OCR failed: {str(error)}",
        }

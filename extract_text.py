import pytesseract
from PIL import Image
import os
import shutil
import sys
import cv2
import numpy as np
from typing import Union


# --- Tesseract Configuration ---
_TESSERACT_CONFIGURED = False

def configure_tesseract(tesseract_cmd_path=None):
    """
    Sets the command for Tesseract OCR, checking in a sensible order.
    """
    global _TESSERACT_CONFIGURED
    if _TESSERACT_CONFIGURED:
        return

    if tesseract_cmd_path and os.path.exists(tesseract_cmd_path):
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd_path
    elif shutil.which("tesseract"):
        pass  # It's in the PATH, no need to set it.
    elif sys.platform == "win32" and os.path.exists(r"C:\Program Files\Tesseract-OCR\tesseract.exe"):
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    else:
        raise OSError(
            "Tesseract is not installed or not in your PATH. "
            "Please install it or provide the path using the --tesseract-path argument."
        )
    _TESSERACT_CONFIGURED = True

# --- Wordlist Preparation for Kannada ---
WORDLIST_SOURCE = "kannada_wordList_with_freq.txt"
TESSERACT_WORDLIST = "kannada_words.txt"

if not os.path.exists(TESSERACT_WORDLIST) and os.path.exists(WORDLIST_SOURCE):
    print(f"[INFO] One-time setup: Preparing Tesseract wordlist from '{WORDLIST_SOURCE}'...")
    try:
        with open(WORDLIST_SOURCE, "r", encoding="utf-8") as f_in, \
             open(TESSERACT_WORDLIST, "w", encoding="utf-8") as f_out:
            for line in f_in:
                word = line.strip().split(" ")[0]
                if word:
                    f_out.write(word + "\n")
        print(f"[INFO] Wordlist '{TESSERACT_WORDLIST}' created successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to create Tesseract wordlist: {e}", file=sys.stderr)

def extract_text(image_source: Union[str, np.ndarray, Image.Image], lang: str = "kan") -> str:
    """
    Extract text from an image using Tesseract OCR.
    Accepts a file path, a NumPy array, or a PIL Image object.
    Uses a custom wordlist for Kannada to improve accuracy.
    """
    configure_tesseract()  # Ensure Tesseract is configured before use

    img = None
    if isinstance(image_source, str):
        if not os.path.exists(image_source):
            raise FileNotFoundError(f"❌ Image not found: {image_source}")
        img = Image.open(image_source)
    elif isinstance(image_source, np.ndarray):
        # pytesseract can handle numpy arrays, but let's ensure it's a PIL Image
        # for consistent preprocessing.
        img = Image.fromarray(image_source)
    elif isinstance(image_source, Image.Image):
        # It's already a PIL Image
        img = image_source
    else:
        raise TypeError(f"Unsupported image source type: {type(image_source)}")

    # --- Robust Image Pre-processing for better OCR ---
    # 1. Convert to grayscale PIL image, then to numpy array for OpenCV processing.
    img_gray = img.convert('L')
    img_np = np.array(img_gray)

    # 2. Denoise the image. This is particularly useful for camera-captured images
    #    which may have digital noise. A median blur is effective at removing
    #    salt-and-pepper noise while preserving edges, which is crucial for OCR.
    #    A kernel size of 3 is a safe choice.
    img_denoised = cv2.medianBlur(img_np, 3)

    # 3. Binarize the image using adaptive thresholding. This is more robust
    #    to varying lighting conditions than a fixed global threshold, which is
    #    especially important for camera-captured images.
    img_binary = cv2.adaptiveThreshold(
        img_denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    # --- Tesseract Configuration for better accuracy ---
    # --psm 4: Assume a single column of text of variable sizes. This is often
    # more robust than psm 6 for images with paragraph or line breaks, and can
    # help prevent the last line from being skipped.
    custom_config = r'--oem 3 --psm 4'
    if lang == "kan" and os.path.exists(TESSERACT_WORDLIST):
        custom_config += f' --user-words "{TESSERACT_WORDLIST}"'

    # OCR
    text = pytesseract.image_to_string(img_binary, lang=lang, config=custom_config)

    text = text.strip()
    if not text:
        print("⚠️ OCR returned no text. The image might be blank or unclear.")
        return ""

    return text

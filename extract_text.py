import pytesseract
from PIL import Image
import cv2
import numpy as np
import os


def preprocess_image(image_path):
    """
    Preprocesses images (especially from camera) to improve OCR accuracy.
    - Grayscale
    - Noise removal
    - Thresholding
    - Deskew (if rotated)
    """
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("❌ Could not read image for preprocessing")

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Denoise
    gray = cv2.medianBlur(gray, 3)

    # Threshold (Binarization)
    _, thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # Deskew
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = thresh.shape
    M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    deskewed = cv2.warpAffine(
        thresh, M, (w, h),
        flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
    )

    return deskewed


def extract_text(image_path):
    """
    Extract Kannada text from image using Tesseract OCR.
    Falls back to raw OCR if preprocessing fails.
    """
    try:
        # Try with preprocessing (better for camera images)
        processed = preprocess_image(image_path)
        text = pytesseract.image_to_string(processed, lang="kan")
    except Exception as e:
        print(f"[WARN] Preprocessing failed: {e}. Falling back to raw OCR.")
        text = pytesseract.image_to_string(Image.open(image_path), lang="kan")

    text = text.strip()
    if not text:
        raise ValueError("❌ OCR returned no text")

    return text

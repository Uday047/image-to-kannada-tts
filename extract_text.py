import pytesseract
from PIL import Image
import cv2
import numpy as np

def preprocess_image(image_path):
    """Preprocess camera images to improve OCR accuracy."""
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("❌ Could not read image")

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Resize if too large
    h, w = gray.shape
    if max(h, w) > 1500:
        scale = 1500 / max(h, w)
        gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

    # Denoise & sharpen
    gray = cv2.medianBlur(gray, 3)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # Adaptive threshold (better for uneven lighting)
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 31, 10
    )

    return thresh

def extract_text(image_path):
    """Extract Kannada text from image using Tesseract OCR."""
    try:
        processed = preprocess_image(image_path)
        text = pytesseract.image_to_string(processed, lang="kan")
    except Exception as e:
        print(f"[WARN] Preprocessing failed: {e}. Falling back to raw OCR.")
        text = pytesseract.image_to_string(Image.open(image_path), lang="kan")

    text = text.strip()
    if not text:
        raise ValueError("❌ OCR returned no text")

    return text

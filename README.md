# Chitravachaka: Kannada Text-to-Speech from Images

**Chitravachaka (ಚಿತ್ರವಾಚಕ)** is an AI-powered application that extracts Kannada text from images and converts it into speech using Google's Text-to-Speech (gTTS) library.

---

## 🧠 Tech Stack
- 🖼️ **Tesseract** – Kannada text recognition from images
- 🗣️ **gTTS (Google Text-to-Speech)** – Simple and effective Text-to-Speech
- � **Streamlit** – Web-based UI for user interaction
- 🐍 **Python** – Core programming language

---

## 🚀 Features
- Upload or capture an image containing Kannada text
- Extract Kannada text using Tesseract OCR
- Enhance the image with brightness/contrast controls
- Convert final text to audio and play or download
- Streamlit-powered modern UI for accessibility

---

## 💻 How to Run the Project

### 1. Prerequisites
- **Python 3.8+**
- **Tesseract OCR Engine**: You must install Tesseract on your system.
  - **Windows**: Download and run the installer from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki). Make sure to add it to your system's PATH.
  - **macOS**: `brew install tesseract tesseract-lang`
  - **Linux (Debian/Ubuntu)**: `sudo apt-get install tesseract-ocr tesseract-ocr-kan`
- You also need the **Kannada language data** for Tesseract.

### 2. Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/chitravachaka-kannada-tts
cd chitravachaka-kannada-tts

# Install Python dependencies
pip install -r requirements.txt

Make sure you have the following:
- `kannada_wordList_with_freq.txt` file in your project root for SymSpell
- Python 3.8+ installed

---

## 📸 Demo
Add screenshots or a Loom/Youtube video here.

---

## 📄 License
MIT License

---

## 🙏 Acknowledgements
- Tesseract OCR
- gTTS (Google Text-to-Speech)
- Streamlit

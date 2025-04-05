# extract_text.py
import easyocr
from spell_checker import correct_spelling, load_symspell

# Load SymSpell once
sym_spell = load_symspell()

def extract_text(image_path):
    reader = easyocr.Reader(['kn'], gpu=False)
    result = reader.readtext(image_path, detail=0)

    filtered_result = [text.replace('1', '').strip() for text in result if not text.strip().isdigit()]
    extracted_text = ' '.join(filtered_result)

    print('\nRaw Extracted Kannada Text:', extracted_text)

    corrected_text = correct_spelling(extracted_text, sym_spell)

    print('\nCorrected Kannada Text:', corrected_text)

    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write(corrected_text)

    return corrected_text

# spell_checker.py
from symspellpy import SymSpell, Verbosity
import os

def load_symspell():
    sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)

    # Use absolute path relative to this script's directory
    base_path = os.path.dirname(__file__)
    dictionary_path = os.path.join(base_path, "kannada_wordList_with_freq.txt")

    if not os.path.exists(dictionary_path):
        raise FileNotFoundError(f"Dictionary file not found at: {dictionary_path}")

    # Use load_dictionary instead of load_dictionary_stream
    sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1, encoding='utf-8')

    return sym_spell

def correct_spelling(text, sym_spell):
    words = text.split()
    corrected_words = []
    for word in words:
        suggestions = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
        best_match = suggestions[0].term if suggestions else word
        corrected_words.append(best_match)
    return ' '.join(corrected_words)

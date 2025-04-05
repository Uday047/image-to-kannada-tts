# spell_checker.py
from symspellpy import SymSpell, Verbosity

def load_symspell():
    sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
    dictionary_path = "kannada_wordList_with_freq.txt"  # UTF-8 Kannada wordlist with frequency

    with open(dictionary_path, 'r', encoding='utf-8') as f:
        sym_spell.load_dictionary_stream(f, term_index=0, count_index=1, separator=' ')

    return sym_spell

def correct_spelling(text, sym_spell):
    words = text.split()
    corrected_words = []
    for word in words:
        suggestions = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
        best_match = suggestions[0].term if suggestions else word
        corrected_words.append(best_match)
    return ' '.join(corrected_words)

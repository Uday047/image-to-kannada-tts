# fix_dict_format.py
input_file = "kannada_wordList_with_freq.txt"
output_file = "cleaned_kannada_dict.txt"

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile:
        line = line.strip()
        if ',' in line:
            word, freq = line.split(',', 1)
        elif '-' in line:
            word, freq = line.split('-', 1)
        else:
            continue
        word = word.strip().replace("‌", "")  # Remove invisible ZWNJ/ZWNW chars
        freq = freq.strip()
        if word and freq.isdigit():
            outfile.write(f"{word} {freq}\n")

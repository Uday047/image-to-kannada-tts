# main.py
from extract_text import extract_text
from text_to_speech import text_to_speech
import time

def split_text(text, max_length=500):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

if __name__ == "__main__":
    image_path = "image2.jpg"
    extract_text(image_path)
    
    with open("output.txt", "r", encoding="utf-8") as f:
        kannada_text = f.read()
    
    timestamp = int(time.time())
    for i, chunk in enumerate(split_text(kannada_text)):
        output_file = f"output_part_{i+1}_{timestamp}.mp3"
        text_to_speech(chunk, output_file)

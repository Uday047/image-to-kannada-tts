from gtts import gTTS
import time

def text_to_speech(text, output_file='kannada_speech.mp3', retries=3):
    if not text.strip():
        raise ValueError("Text is empty — nothing to convert to speech.")
    
    for attempt in range(retries):
        try:
            tts = gTTS(text, lang='kn')
            tts.save(output_file)
            return output_file  # Return filename for Streamlit to use
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {repr(e)}")
            if attempt < retries - 1:
                time.sleep(2)
            else:
                raise Exception("TTS failed after all retries")

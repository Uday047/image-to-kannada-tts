# text_to_speech.py
from gtts import gTTS
import subprocess
import time
import platform

def text_to_speech(text, output_file='kannada_speech.mp3', retries=3, timeout=10):
    for attempt in range(retries):
        try:
            tts = gTTS(text, lang='kn', timeout=timeout)
            tts.save(output_file)

            # Cross-platform audio playback
            if platform.system() == 'Windows':
                subprocess.run(['start', output_file], shell=True)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['afplay', output_file])
            else:  # Linux
                subprocess.run(['xdg-open', output_file])
            break
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2)
            else:
                raise Exception("TTS failed after all retries")

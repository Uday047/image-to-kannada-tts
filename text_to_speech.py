from gtts import gTTS
from io import BytesIO

def text_to_speech(text: str, lang: str = 'kn', filename: str = None) -> bytes:
    """
    Convert text into speech using the gTTS API.
    Returns the audio bytes. If a filename is provided, it also saves the audio.
    """
    if not text.strip():
        raise ValueError("❌ No text provided for TTS")

    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        audio_bytes = fp.read()
    except Exception as e:
        raise ConnectionError(f"❌ Failed to generate audio with gTTS: {e}")

    if filename:
        with open(filename, 'wb') as f:
            f.write(audio_bytes)

    return audio_bytes

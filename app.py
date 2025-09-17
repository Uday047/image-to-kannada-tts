# app.py
import streamlit as st
import time
import numpy as np
import cv2
from PIL import Image
from extract_text import extract_text
from text_to_speech import text_to_speech
import os
import base64

# Helper function to generate and autoplay audio
def autoplay_audio(audio_bytes: bytes, hidden: bool = False):
    """
    Generates an HTML audio player that autoplays.
    If hidden, the player controls are not shown.
    """
    b64 = base64.b64encode(audio_bytes).decode()

    # Determine style for visibility
    style = "display:none;" if hidden else "width:100%;"

    audio_html = f"""
        <audio controls autoplay style="{style}">
          <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
          Your browser does not support the audio element.
        </audio>
        """
    st.components.v1.html(audio_html, height=None if hidden else 50)

def main():
    st.set_page_config(
        page_title="ಚಿತ್ರವಾಚಕ (Chitravachaka)",
        page_icon="📖", 
        layout="centered",
        initial_sidebar_state="collapsed" # Collapse sidebar for this persona
    )

    # Custom CSS for a high-contrast, simple UI and a huge camera button
    st.markdown(
        """
        <style>
            body {
                background-color: #000000;
                color: #ffffff;
            }
            .main {
                background-color: #000000;
            }
            h1, h4 {
                color: #FFFF00; /* Bright yellow for high contrast */
                text-align: center;
            }
            /* Make the camera input button huge and unmissable */
            div[data-testid="stCameraInput"] button {
                background-color: #FFFF00;
                color: black;
                font-size: 24px;
                font-weight: bold;
                padding: 25px;
                border-radius: 15px;
                border: 3px solid white;
                display: block;
                margin: 20px auto;
                width: 90%;
                height: 120px;
            }
            /* Hide the "Drag and drop file" text */
            div[data-testid="stCameraInput"] small {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<h1>ಚಿತ್ರವಾಚಕ</h1>", unsafe_allow_html=True)

    # --- State Management and Audio Announcements ---

    # 1. Welcome message on first load
    if 'welcome_played' not in st.session_state:
        welcome_text = "ಚಿತ್ರವಾಚಕ ಅಪ್ಲಿಕೇಶನ್‌ಗೆ ಸ್ವಾಗತ. ಚಿತ್ರವನ್ನು ಸೆರೆಹಿಡಿಯಲು ದಯವಿಟ್ಟು ಕೆಳಗಿನ ದೊಡ್ಡ ಕ್ಯಾಮೆರಾ ಬಟನ್ ಒತ್ತಿರಿ."
        try:
            audio_bytes = text_to_speech(welcome_text, lang='kn')
            autoplay_audio(audio_bytes, hidden=True)
        except Exception as e:
            st.warning(f"Could not play welcome message: {e}")
        st.session_state.welcome_played = True

    # --- Main UI: The Camera Button ---
    
    # The camera input is the main interaction point.
    captured_image = st.camera_input(
        "ಕ್ಯಾಮೆರಾ ಬಟನ್ (Camera Button)", 
        key="camera_input"
    )

    # --- Processing Logic ---

    # Process the image only if a new one is captured
    if captured_image is not None and captured_image != st.session_state.get('last_image_processed'):
        st.session_state.last_image_processed = captured_image

        # 2. Announce image capture and processing
        processing_text = "ಚಿತ್ರವನ್ನು ಸೆರೆಹಿಡಿಯಲಾಗಿದೆ, ಈಗ ಪ್ರಕ್ರಿಯೆಗೊಳಿಸಲಾಗುತ್ತಿದೆ."
        try:
            audio_bytes = text_to_speech(processing_text, lang='kn')
            autoplay_audio(audio_bytes, hidden=True)
        except Exception as e:
            st.warning(f"Could not play processing message: {e}")

        with st.spinner("🔄 ಪ್ರಕ್ರಿಯೆಗೊಳಿಸಲಾಗುತ್ತಿದೆ... (Processing...)"):
            try:
                image = Image.open(captured_image)
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                image_np = np.array(image)

                # Extract text
                extracted_text = extract_text(image_np)

                if not extracted_text or not extracted_text.strip():
                    # 3a. Announce if no text is found
                    no_text_message = "ಕ್ಷಮಿಸಿ, ಚಿತ್ರದಲ್ಲಿ ಯಾವುದೇ ಪಠ್ಯ ಕಂಡುಬಂದಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ."
                    st.warning("⚠️ " + no_text_message)
                    audio_bytes = text_to_speech(no_text_message, lang='kn')
                    autoplay_audio(audio_bytes, hidden=True)
                else:
                    # 3b. Announce and read the extracted text
                    st.success("✅ ಪಠ್ಯವನ್ನು ಯಶಸ್ವಿಯಾಗಿ ಓದಲಾಗಿದೆ! (Text read successfully!)")
                    
                    # Combine announcement and result for seamless playback
                    result_announcement = f"ಪಠ್ಯವನ್ನು ಗುರುತಿಸಲಾಗಿದೆ. {extracted_text}"
                    audio_bytes = text_to_speech(result_announcement, lang='kn')
                    
                    # Display the player with controls and autoplay
                    st.markdown("### 🔊 ಫಲಿತಾಂಶವನ್ನು ಆಲಿಸಿ (Listen to the Result)")
                    autoplay_audio(audio_bytes, hidden=False)

                    # Provide a download button for the audio
                    st.download_button(
                        label="📥 ಆಡಿಯೋ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ (Download Audio)",
                        data=audio_bytes,
                        file_name="kannada_speech.mp3",
                        mime="audio/mpeg"
                    )
                    # For sighted users, also display the text
                    st.info(f"**ಗುರುತಿಸಲಾದ ಪಠ್ಯ (Recognized Text):**\n\n{extracted_text}")

            except Exception as e:
                error_message = f"ಒಂದು ದೋಷ ಸಂಭವಿಸಿದೆ: {str(e)}"
                st.error(error_message)
                audio_bytes = text_to_speech("ಕ್ಷಮಿಸಿ, ಪ್ರಕ್ರಿಯೆಗೊಳಿಸುವಾಗ ದೋಷ ಕಂಡುಬಂದಿದೆ.", lang='kn')
                autoplay_audio(audio_bytes, hidden=True)

if __name__ == "__main__":
    # This is a workaround for a Streamlit issue where it might re-run the script
    # unnecessarily when new files are created. This disables the file watcher.
    if "server.fileWatcherType" not in st._config.get_options_for_section("server"):
        st._config.set_option("server.fileWatcherType", "none")
    main()
    

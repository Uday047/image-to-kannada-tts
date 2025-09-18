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
            /* Style for the main 'Open Camera' button */
            div[data-testid="stButton"] > button {
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
            /* Style for the camera view to make it feel more full-screen */
            div[data-testid="stCameraInput"] {
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            div[data-testid="stCameraInput"] video {
                width: 100%;
                border-radius: 15px;
            }
            div[data-testid="stCameraInput"] button {
                /* Make the capture button huge and circular */
                background-color: #FF4B4B; /* Red color for capture */
                color: white;
                font-size: 20px;
                font-weight: bold;
                border-radius: 50%; /* Make it circular */
                width: 100px;
                height: 100px;
                margin-top: 20px;
            }
            /* Hide the "Drag and drop file" text */
            div[data-testid="stCameraInput"] small {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- State Management ---
    if 'view' not in st.session_state:
        st.session_state.view = 'home'  # Can be 'home' or 'camera'
    if 'captured_image' not in st.session_state:
        st.session_state.captured_image = None

    # 1. Welcome message on first load
    if 'welcome_played' not in st.session_state:
        welcome_text = "ಚಿತ್ರವಾಚಕ ಅಪ್ಲಿಕೇಶನ್‌ಗೆ ಸ್ವಾಗತ. ಚಿತ್ರವನ್ನು ಸೆರೆಹಿಡಿಯಲು ದಯವಿಟ್ಟು ಕೆಳಗಿನ ದೊಡ್ಡ ಕ್ಯಾಮೆರಾ ಬಟನ್ ಒತ್ತಿರಿ."
        try:
            audio_bytes = text_to_speech(welcome_text, lang='kn')
            autoplay_audio(audio_bytes, hidden=True)
        except Exception as e:
            st.warning(f"Could not play welcome message: {e}")
        st.session_state.welcome_played = True

    # --- UI ROUTING ---

    if st.session_state.view == 'camera':
        # --- CAMERA VIEW ---
        st.markdown("<h4>ಚಿತ್ರವನ್ನು ಸೆರೆಹಿಡಿಯಿರಿ (Capture the image)</h4>", unsafe_allow_html=True)
        
        captured_image = st.camera_input(
            "ಕ್ಯಾಮೆರಾ (Camera)", 
            key="camera_main_view",
            label_visibility="collapsed"
        )
        
        if captured_image:
            st.session_state.captured_image = captured_image
            st.session_state.view = 'home'  # Switch back to home view for processing
            st.rerun()

    elif st.session_state.view == 'home':
        # --- HOME / RESULTS VIEW ---
        st.markdown("<h1>ಚಿತ್ರವಾಚಕ</h1>", unsafe_allow_html=True)

        # Check if an image was just captured
        if st.session_state.captured_image is not None:
            image_to_process = st.session_state.captured_image
            st.session_state.captured_image = None # Clear the state to avoid reprocessing

            # Announce processing
            processing_text = "ಚಿತ್ರವನ್ನು ಸೆರೆಹಿಡಿಯಲಾಗಿದೆ, ಈಗ ಪ್ರಕ್ರಿಯೆಗೊಳಿಸಲಾಗುತ್ತಿದೆ."
            try:
                audio_bytes = text_to_speech(processing_text, lang='kn')
                autoplay_audio(audio_bytes, hidden=True)
            except Exception as e:
                st.warning(f"Could not play processing message: {e}")

            with st.spinner("🔄 ಪ್ರಕ್ರಿಯೆಗೊಳಿಸಲಾಗುತ್ತಿದೆ... (Processing...)"):
                try:
                    image = Image.open(image_to_process)
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    image_np = np.array(image)

                    # Extract text
                    extracted_text = extract_text(image_np)

                    if not extracted_text or not extracted_text.strip():
                        no_text_message = "ಕ್ಷಮಿಸಿ, ಚಿತ್ರದಲ್ಲಿ ಯಾವುದೇ ಪಠ್ಯ ಕಂಡುಬಂದಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ."
                        st.warning("⚠️ " + no_text_message)
                        audio_bytes = text_to_speech(no_text_message, lang='kn')
                        autoplay_audio(audio_bytes, hidden=True)
                    else:
                        st.success("✅ ಪಠ್ಯವನ್ನು ಯಶಸ್ವಿಯಾಗಿ ಓದಲಾಗಿದೆ! (Text read successfully!)")
                        result_announcement = f"ಪಠ್ಯವನ್ನು ಗುರುತಿಸಲಾಗಿದೆ. {extracted_text}"
                        audio_bytes = text_to_speech(result_announcement, lang='kn')
                        
                        st.markdown("### 🔊 ಫಲಿತಾಂಶವನ್ನು ಆಲಿಸಿ (Listen to the Result)")
                        autoplay_audio(audio_bytes, hidden=False)

                        st.download_button(
                            label="📥 ಆಡಿಯೋ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ (Download Audio)",
                            data=audio_bytes,
                            file_name="kannada_speech.mp3",
                            mime="audio/mpeg"
                        )
                        st.info(f"**ಗುರುತಿಸಲಾದ ಪಠ್ಯ (Recognized Text):**\n\n{extracted_text}")

                except Exception as e:
                    error_message = f"ಒಂದು ದೋಷ ಸಂಭವಿಸಿದೆ: {str(e)}"
                    st.error(error_message)
                    audio_bytes = text_to_speech("ಕ್ಷಮಿಸಿ, ಪ್ರಕ್ರಿಯೆಗೊಳಿಸುವಾಗ ದೋಷ ಕಂಡುಬಂದಿದೆ.", lang='kn')
                    autoplay_audio(audio_bytes, hidden=True)

        # Show the button to open the camera
        if st.button("ಕ್ಯಾಮೆರಾ ತೆರೆಯಿರಿ (Open Camera)", key="open_camera_btn"):
            camera_open_text = "ಕ್ಯಾಮೆರಾ ತೆರೆಯಲಾಗುತ್ತಿದೆ. ಚಿತ್ರವನ್ನು ಸೆರೆಹಿಡಿಯಲು ಸಿದ್ಧರಾಗಿ."
            try:
                audio_bytes = text_to_speech(camera_open_text, lang='kn')
                autoplay_audio(audio_bytes, hidden=True)
            except Exception as e:
                st.warning(f"Could not play camera open message: {e}")
            
            st.session_state.view = 'camera'
            st.rerun()

if __name__ == "__main__":
    # This is a workaround for a Streamlit issue where it might re-run the script
    # unnecessarily when new files are created. This disables the file watcher.
    if "server.fileWatcherType" not in st._config.get_options_for_section("server"):
        st._config.set_option("server.fileWatcherType", "none")
    main()
    

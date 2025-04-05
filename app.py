import streamlit as st
import time
import numpy as np
import cv2
from PIL import Image
from extract_text import extract_text
from text_to_speech import text_to_speech

def main():
    st.set_page_config(
        page_title="Kannada TTS App", 
        page_icon="📖", 
        layout="centered",
        initial_sidebar_state="expanded"
    )

    # Custom background and heading style
    st.markdown(
        """
        <style>
            body {
                background-color: #121212;
                color: #ffffff;
            }
            .main {
                background-color: #121212;
            }
            h1 {
                color: #FFAB00;
            }
            h4 {
                color: #FFD54F;
            }
            .stTextInput, .stFileUploader, .stButton, .stSelectbox {
                color: black !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Banner
    st.markdown(
        """
        <h1 style='text-align: center; font-family: "Arial Black", sans-serif;'>ಚಿತ್ರವಾಚಕಕ್ಕೆ ಸ್ವಾಗತ</h1>
        <h4 style='text-align: center; font-family: "Arial", sans-serif;'>ಚಿತ್ರದಿಂದ ಪಠ್ಯವನ್ನು ಸುಲಭವಾಗಿ ಹೊರತೆಗೆಯಿರಿ ಮತ್ತು ಕನ್ನಡ ಆಡಿಯೋವಾಗಿ ಪರಿವರ್ತಿಸಿ!</h4>
        """,
        unsafe_allow_html=True
    )

    # Sidebar for language selection
    st.sidebar.title("🌐 Language Settings")
    lang_options = ["Kannada", "English", "Hindi", "Tamil", "Telugu"]
    selected_lang = st.sidebar.selectbox("Choose Language", lang_options)

    # Upload or capture image section
    uploaded_file = st.file_uploader("📷 Upload an Image", type=["png", "jpg", "jpeg"])
    picture = st.camera_input("Take a picture")
    image_source = uploaded_file if uploaded_file else picture

    if image_source is not None:
        st.image(image_source, caption="Uploaded/Captured Image", use_column_width=True)

        # Convert and enhance image
        image = Image.open(image_source)
        image_np = np.array(image)

        st.sidebar.title("🖼 Image Enhancement")
        brightness = st.sidebar.slider("Adjust Brightness", 0.5, 2.0, 1.0)
        contrast = st.sidebar.slider("Adjust Contrast", 0.5, 2.0, 1.0)
        image_np = cv2.convertScaleAbs(image_np, alpha=contrast, beta=brightness)

        # OCR
        with st.spinner("🔄 Processing image..."):
            time.sleep(1)
            extracted_text = extract_text(image_np)
            st.success("✅ ಪಠ್ಯ ಉಗಮಿಸಲು ಮುಗಿದಿದೆ!")
            st.write("**ಹಿಡಿದ ಪಠ್ಯ:**", extracted_text)

            # Editable text
            st.subheader("✏️ ಹಿಡಿದ ಪಠ್ಯವನ್ನು ಸಂಪಾದಿಸಿ")
            edited_text = st.text_area("ಈ ಕೆಳಗಿನ ಪಠ್ಯವನ್ನು ಸಂಪಾದಿಸಿ:", extracted_text)

            # Translation (dummy)
            if selected_lang != "Kannada":
                st.subheader("🔄 ಅನುವಾದಿತ ಪಠ್ಯ")
                translated_text = f"[Translated to {selected_lang}] {edited_text}"
                st.write(translated_text)
            else:
                translated_text = edited_text

            # TTS
            with st.spinner("🎶 ಆಡಿಯೋ ತಯಾರಿಸಲಾಗುತ್ತಿದೆ..."):
                audio_file = "output.mp3"
                text_to_speech(translated_text, audio_file)
                st.success("🔊 ಆಡಿಯೋ ಸಿದ್ಧವಾಗಿದೆ!")
                st.audio(audio_file, format="audio/mp3", start_time=0)

                st.download_button(
                    label="📥 ಆಡಿಯೋ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ",
                    data=open(audio_file, "rb").read(),
                    file_name="output.mp3",
                    mime="audio/mpeg"
                )

if __name__ == "__main__":
    main()

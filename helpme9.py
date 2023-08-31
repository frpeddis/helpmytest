import streamlit as st
import openai
from PIL import Image
import pytesseract

# Initialize GPT API (Replace with your actual API key)
openai.api_key = st.secrets["API_KEY"]

# Set tesseract cmd path and config
tessdata_dir = './tessdata'  # Update this path to your tessdata directory
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
custom_oem_psm_config = f'--tessdata-dir {tessdata_dir}'

st.title("OCR with GPT-3 Analysis")

# Language selection
lang_option = st.selectbox("Select OCR Language", ['English', 'Italiano'])
ocr_lang = 'eng' if lang_option == 'English' else 'ita'

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.write("")
    st.write("Recognized Text")

    # Perform OCR based on selected language
    text = pytesseract.image_to_string(image, lang=ocr_lang, config=custom_oem_psm_config)
    st.write(text)

    # The rest of the code remains unchanged...

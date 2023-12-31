import streamlit as st
from PIL import Image, ImageOps
import pytesseract
import openai

# Initialize GPT API
openai.api_key = st.secrets["API_KEY"]

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Initialize Streamlit session state
if 'rotation' not in st.session_state:
    st.session_state.rotation = 0

st.title("OCR with GPT-3 Analysis and Image Rotation")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

language = st.selectbox('Select OCR Language', ['English', 'Italian'])
lang_code = 'eng' if language == 'English' else 'ita'

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')

    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button('Rotate'):
        st.session_state.rotation = (st.session_state.rotation + 90) % 360

    if st.button('Perform OCR'):
        # Apply the rotation right before OCR
        rotated_image = ImageOps.exif_transpose(image).rotate(st.session_state.rotation)
        
        st.write("Recognized Text")
        # Perform OCR based on selected language
        text = pytesseract.image_to_string(rotated_image, lang=lang_code)
        st.write(text)

        if st.button('Analyze'):
            prompt = f"This is a text to analyze: {text}. Look for any questions contained in the text. First think step by step, try to understand what the context of the topic is. then act as a super expert in that topic. then give me the answer you consider correct"
            response = openai.Completion.create(
              engine="text-davinci-002",
              prompt=prompt,
              max_tokens=150
            )

            st.write("GPT-3 Analysis")
            st.write(response.choices[0].text.strip())

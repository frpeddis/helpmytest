import streamlit as st
import openai
from PIL import Image
import pytesseract
import pyheif

# Initialize GPT API (Replace with your actual API key)
openai.api_key = st.secrets["API_KEY"]

# Set Tesseract cmd path
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

st.title("OCR with GPT-3 Analysis")

# Language selection
lang_option = st.selectbox("Select OCR Language", ['English', 'Italian'])
ocr_lang = 'eng' if lang_option == 'English' else 'ita'

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "heic"])

if uploaded_file is not None:
    if uploaded_file.type == "image/heic":
        heif_file = pyheif.read(uploaded_file.read())
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
    else:
        image = Image.open(uploaded_file)
        
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.write("")
    st.write("Recognized Text")
    
    # Perform OCR based on the selected language
    text = pytesseract.image_to_string(image, lang=ocr_lang)
    st.write(text)

    # Analyze text using ChatGPT and provide an opinion
    if st.button('Analyze with ChatGPT'):
        prompt = f"This is a text to analyze: {text}. First think step by step, then understand what is the topic of the text. You are an expert on that topic. Now give me your opinion about that topic."
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=200,
            temperature=0.2  # Lower temperature means less randomness
        )

        st.write("GPT-3 Analysis - overview")
        st.write(response.choices[0].text.strip())

        prompt = f"Now look for any questions contained in the text {text}. If you find a question, a quiz, a multiple-choice question, etc., give me the answer you consider correct to that question, quiz, or multiple-choice question. Do not end your output without giving an answer to questions contained in the text. If you do not find any question simply tell me that no questions found"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=300,
            temperature=0.2  # Lower temperature means less randomness
        )

        st.write("GPT-3 Analysis - answer suggestion (if any)")
        st.write(response.choices[0].text.strip())

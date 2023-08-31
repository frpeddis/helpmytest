import streamlit as st
import openai
from PIL import Image
import pytesseract

# Initialize GPT API (Replace with your actual API key)
openai.api_key = st.secrets["API_KEY"]
#openai.api_key = "your-openai-api-key"

# Set tesseract cmd path
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

st.title("OCR with GPT-3 Analysis")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.write("")

    st.write("Recognized Text")

    # Perform OCR
    text = pytesseract.image_to_string(image)
    st.write(text)

    # Analyze text using ChatGPT and provide an opinion
    if st.button('Analyze with ChatGPT'):
        prompt = f"This is a text to analyze: {text}. First think step by step, then understand what is the topic of the text. You are an expert on that topic. Now give me your opinion about that topic. Then it is very important to look for any questions contained in the text. If you find a question, a quiz, a multichoise questions, etc give me the answer you consider correct to that question, that quiz, that multiple choise question. Do not end your output without giving a answer to questions contained in the text"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=400,
            temperature=0.2  # Lower temperature means less randomness
        )

        st.write("GPT-3 Analysis")
        st.write(response.choices[0].text.strip())

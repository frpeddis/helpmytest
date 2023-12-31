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
        # Replace with an actual API call to OpenAI GPT
        prompt = f"This is a text to analyze: {text}. Look for any questions contained in the text. First think step by step, try to understand what the context of the topic is. then act as a super expert in that topic. then give me the answer you consider correct"
        response = openai.Completion.create(
          engine="text-davinci-002",
          prompt=prompt,
          max_tokens=200
        )

        st.write("GPT-3 Analysis")
        st.write(response.choices[0].text.strip())

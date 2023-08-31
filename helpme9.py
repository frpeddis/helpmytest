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

if 'crop_coords' not in st.session_state:
    st.session_state.crop_coords = (0, 0, 100, 100)

st.title("OCR with GPT-3 Analysis and Image Rotation")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

language = st.selectbox('Select OCR Language', ['English', 'Italian'])
lang_code = 'eng' if language == 'English' else 'ita'

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button('Rotate'):
        st.session_state.rotation = (st.session_state.rotation + 90) % 360
        image = image.rotate(st.session_state.rotation)
        st.image(image, caption="Rotated Image", use_column_width=True)
    
    x1, y1, x2, y2 = st.session_state.crop_coords
    x1 = st.slider("Left (x1)", min_value=0, max_value=image.size[0]-1, value=x1)
    y1 = st.slider("Top (y1)", min_value=0, max_value=image.size[1]-1, value=y1)
    x2 = st.slider("Right (x2)", min_value=0, max_value=image.size[0], value=x2)
    y2 = st.slider("Bottom (y2)", min_value=0, max_value=image.size[1], value=y2)

    if st.button('Crop'):
        st.session_state.crop_coords = (x1, y1, x2, y2)
        image = image.crop(st.session_state.crop_coords)
        st.image(image, caption="Cropped Image", use_column_width=True)

    if st.button('Perform OCR'):
        # Apply the rotation right before OCR
        rotated_image = ImageOps.exif_transpose(image).rotate(st.session_state.rotation)
        
        st.write("Recognized Text")
        # Perform OCR based on selected language
        text = pytesseract.image_to_string(rotated_image, lang=lang_code)
        st.write(text)

        if st.button('Analyze'):
            prompt = f"This is a text to analyze: {text}. Look for any questions contained in the text. First think step by step, try to understand what the context of the topic is. Then act as a super expert in that topic. Then give me the answer you consider correct"
            response = openai.Completion.create(
              engine="text-davinci-002",
              prompt=prompt,
              max_tokens=150
            )

            st.write("GPT-3 Analysis")
            st.write(response.choices[0].text.strip())

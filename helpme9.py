import streamlit as st
from PIL import Image, ImageOps
import pytesseract
import openai

# Initialize GPT API
openai.api_key = st.secrets["API_KEY"]

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Initialize Streamlit session state
if 'image' not in st.session_state:
    st.session_state.image = None

if 'crop_coords' not in st.session_state:
    st.session_state.crop_coords = (0, 0, 100, 100)

st.title("OCR with GPT-3 Analysis and Image Rotation")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

language = st.selectbox('Select OCR Language', ['English', 'Italian'])
lang_code = 'eng' if language == 'English' else 'ita'

if uploaded_file is not None:
    st.session_state.image = Image.open(uploaded_file).convert('RGB')

if st.session_state.image is not None:
    st.image(st.session_state.image, caption="Uploaded Image", use_column_width=True)

    if st.button('Rotate'):
        rotated_image = st.session_state.image.transpose(Image.Transpose.ROTATE_90)  # Rotate 90 degrees
        st.session_state.image = rotated_image  # Update session state
        st.session_state.crop_coords = (0, 0, rotated_image.size[0], rotated_image.size[1])  # Update crop coordinates
        st.image(rotated_image, caption="Rotated Image", use_column_width=True)

    x1, y1, x2, y2 = st.session_state.crop_coords
    x1 = st.slider("Left (x1)", min_value=0, max_value=st.session_state.image.size[0]-1, value=x1)
    y1 = st.slider("Top (y1)", min_value=0, max_value=st.session_state.image.size[1]-1, value=y1)
    x2 = st.slider("Right (x2)", min_value=0, max_value=st.session_state.image.size[0], value=x2)
    y2 = st.slider("Bottom (y2)", min_value=0, max_value=st.session_state.image.size[1], value=y2)

    if st.button('Crop'):
        st.session_state.crop_coords = (x1, y1, x2, y2)
        cropped_image = st.session_state.image.crop(st.session_state.crop_coords)
        st.session_state.image = cropped_image  # Update session state
        st.image(cropped_image, caption="Cropped Image", use_column_width=True)

    if st.button('Perform OCR'):
        st.write("Recognized Text")
        text = pytesseract.image_to_string(st.session_state.image, lang=lang_code)
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

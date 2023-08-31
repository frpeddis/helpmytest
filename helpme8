import streamlit as st
import openai
import cv2
import numpy as np
import pytesseract

# Initialize GPT API (Replace with your actual API key)
openai.api_key = st.secrets["API_KEY"]

# Set tesseract cmd path
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

st.title("OCR with GPT-3 Analysis")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Load the image using OpenCV
    bytes_data = uploaded_file.read()
    nparr = np.frombuffer(bytes_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Create rotation buttons
    rotate = st.sidebar.selectbox('Rotate Image', ['0', '90', '180', '270'], 0)
    if rotate:
        angle = int(rotate)
        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        image = cv2.warpAffine(image, M, (w, h))

    # Display the image
    st.image(image, caption="Uploaded Image", channels="RGB", use_column_width=True)

    # ROI Selection
    st.sidebar.write("Select ROI")
    x1 = st.sidebar.slider('x1', 0, image.shape[1], 0)
    x2 = st.sidebar.slider('x2', 0, image.shape[1], image.shape[1])
    y1 = st.sidebar.slider('y1', 0, image.shape[0], 0)
    y2 = st.sidebar.slider('y2', 0, image.shape[0], image.shape[0])

    # Crop the ROI
    cropped_image = image[y1:y2, x1:x2]

    # Display the cropped image
    st.image(cropped_image, caption="Cropped Image", channels="RGB", use_column_width=True)

    st.write("Recognized Text")

    # Perform OCR on the cropped image
    text = pytesseract.image_to_string(cv2.cvtColor(cropped_image, cv2.COLOR_RGB2GRAY))
    st.write(text)

    # Analyze text using ChatGPT and provide an opinion
    if st.button('Analyze with ChatGPT'):
        prompt = f"This is a text to analyze: {text}. Look for any questions contained in the text. First think step by step, try to understand what the context of the topic is. then act as a super expert in that topic. then give me the answer you consider correct"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=200
        )
        st.write("GPT-3 Analysis")
        st.write(response.choices[0].text.strip())

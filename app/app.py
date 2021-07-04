import os
import io
import sys
import numpy as np
from array import array
import cv2
from PIL import Image, ImageDraw
import streamlit as st
from image_processing import *
from azure_api import * 

MAGE_EMOJI_URL = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/twitter/259/mage_1f9d9.png"

# Set page title and favicon.
st.set_page_config(
    page_title="OCR Generator", page_icon=MAGE_EMOJI_URL,
)

st.title('A web app for OCR on images')

image = st.file_uploader('Upload an image', type=['png', 'jpg'])

subscription_key = os.environ.get('subscription_key')
endpoint = os.environ.get('endpoint')

if image is not None:
    st.image(image)

    boxes, texts = get_ocr(image, subscription_key, endpoint)
    polygons = encode_bboxes(boxes)

    image = np.array(Image.open(image)) 

    image = overlay_rect(image, polygons)
    image = overlay_text(image, boxes, texts)

    st.image(image)

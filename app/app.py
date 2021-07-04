import os
import cv2
import sys
import numpy as np
from array import array
from PIL import Image, ImageDraw

from image_processing import *
from azure_api import * 

subscription_key = os.environ.get('subscription_key')
endpoint = os.environ.get('endpoint')

read_image_url = "https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/master/articles/cognitive-services/Computer-vision/Images/readsample.jpg"

im = cv2.imread('images/readsample.jpg')

boxes, texts = get_ocr(read_image_url, subscription_key, endpoint)
polygons = encode_bboxes(boxes)

im = overlay_rect(im, polygons)
im = overlay_text(im, boxes, texts)

cv2.imwrite('OCR.jpg', im)


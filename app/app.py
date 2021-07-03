from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

import os
import cv2
import sys
import time
import numpy as np
from array import array
from PIL import Image, ImageDraw

'''
Authenticate
Authenticates your credentials and creates a client.
'''
subscription_key = os.environ.get('subscription_key')
endpoint = os.environ.get('endpoint')

computervision_client = ComputerVisionClient(endpoint, 
                                             CognitiveServicesCredentials(subscription_key))

print("===== Read File - remote =====")
# Get an image with text
read_image_url = "https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/master/articles/cognitive-services/Computer-vision/Images/readsample.jpg"

# Call API with URL and raw response (allows you to get the operation location)
read_response = computervision_client.read(read_image_url,  raw=True)

# Get the operation location (URL with an ID at the end) from the response
read_operation_location = read_response.headers["Operation-Location"]
# Grab the ID from the URL
operation_id = read_operation_location.split("/")[-1]

# Call the "GET" API and wait for it to retrieve the results 
while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

boxes = list()
texts = list()

# log detected text, line by line
if read_result.status == OperationStatusCodes.succeeded:
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            boxes.append(line.bounding_box)
            texts.append(line.text)

im = cv2.imread('images/readsample.jpg')

polygons = list()

for box in boxes:
    polygon = list()

    for idx in range(0, len(box), 2):
        polygon.append([box[idx], box[idx+1]])

    polygons.append(polygon)

polygons = np.array(polygons, dtype=np.int32)


# create polygon around the detected text
cv2.polylines(im, polygons, True, (0,255,255))

font = cv2.FONT_HERSHEY_SIMPLEX

# put text on top of the drawn polygon
for idx in range(len(texts)):
    cv2.putText(im, texts[idx], (int(boxes[idx][0]), int(boxes[idx][1])), font, 4, (255,255,255), 2, cv2.LINE_AA)

cv2.imwrite('OCR.jpg', im)


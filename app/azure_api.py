import time

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

def get_ocr(read_image_url, subscription_key, endpoint):
    """[This function queries azure OCR API on an image to get OCR texts and location (rectangles)]

    Args:
        read_image_url ([String]): [URL to where the image is hosted]
        subscription_key ([String]): [private subscription_key specific to azure cognitive services]
        endpoint ([String]): [URL to where API endpoint for cognitive services is deployed]

    Returns:
        [list, list]: [list of x, y coords of rectangles and corresponding texts]
    """
    computervision_client = ComputerVisionClient(endpoint, 
                                                CognitiveServicesCredentials(subscription_key))

    read_response = computervision_client.read(read_image_url,  raw=True)

    read_operation_location = read_response.headers["Operation-Location"]
    operation_id = read_operation_location.split("/")[-1]

    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    boxes, texts = list(), list()

    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                boxes.append(line.bounding_box)
                texts.append(line.text)

    return boxes, texts
import cv2
import numpy as np

def overlay_rect(im, polygons):
    """[This function overlays rectangles defined in polygons [list of x y coords] on an image]

    Args:
        im ([np.ndarray]): [image]
        polygons ([list]): [x y coords of rectangles]

    Returns:
        [np.ndarray]: [image with rectangles drawn]
    """
    # create polygon around the detected text
    cv2.polylines(im, polygons, True, (0,255,255))

    return im

def overlay_text(im, boxes, texts):
    """[This function renders corresponding text detected from OCR for each rectangle, positioned at first x, y coord]

    Args:
        im ([np.ndarray]): [image]
        boxes ([list]): [x y coords of rectangles]
        texts ([list]): [list of OCR detected texts]

    Returns:
        [np.ndarray]: [image with text rendered]
    """
    font = cv2.FONT_HERSHEY_SIMPLEX

    # put text on top of the drawn polygon
    for idx in range(len(texts)):
        cv2.putText(im, texts[idx], (int(boxes[idx][0]), int(boxes[idx][1])), font, 4, (255,255,255), 2, cv2.LINE_AA)

    return im 

def encode_bboxes(boxes):
    """[This function processes rectangles from Azure API and converts it to cv2.polylines format]

    Args:
        boxes ([list]): [list of x, y coordinates of rectangles]

    Returns:
        [list]: [np.array of formatted for use with cv2.polylines function call]
    """
    
    polygons = list()

    for box in boxes:
        polygon = list()
        for idx in range(0, len(box), 2):
            polygon.append([box[idx], box[idx+1]])
        polygons.append(polygon)

    polygons = np.array(polygons, dtype=np.int32)

    return polygons
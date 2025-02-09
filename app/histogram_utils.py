import os
import cv2
import json
from app.config import Configuration

conf = Configuration()

def calculate_histogram(image_id):
    image_path = os.path.join(conf.image_folder_path, image_id)
    image = cv2.imread(image_path)

    histograms = {}
    for i, color in enumerate(['blue', 'green', 'red']):
        hist = cv2.calcHist([image], [i], None, [256], [0, 256])
        histograms[color] = hist.flatten().tolist()

    result = histograms
    return json.dumps(result)
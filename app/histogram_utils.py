import os
import cv2
import json
from app.config import Configuration

conf = Configuration()


def calculate_histogram(image_id) -> str:
    """
    Calculate histograms for each color channel (RGB) of an image.
    Parameters:
    ----------
    image_id : str
        The identifier/filename of the image to process.
    Returns:
    -------
    str
        JSON string containing the histogram data with the following structure:
        {
            'blue': list of 256 values,
            'green': list of 256 values,
            'red': list of 256 values
        }
        Each list contains the pixel counts for intensity values 0-255 for that color channel.
    Note: The image is expected to be in the configured image folder path.
    """
    image_path = os.path.join(conf.image_folder_path, image_id)
    image = cv2.imread(image_path)

    histograms = {}
    for i, color in enumerate(['blue', 'green', 'red']):
        hist = cv2.calcHist([image], [i], None, [256], [0, 256])
        histograms[color] = hist.flatten().tolist()

    result = histograms
    return json.dumps(result)
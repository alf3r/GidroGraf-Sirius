import cv2


def convert_range(data):
    dst=cv2.convertScaleAbs(src=data, alpha=5000, beta=10)
    return dst
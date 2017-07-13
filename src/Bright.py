import cv2


def convert_range(data):
    dst=cv2.convertScaleAbs(src=data, alpha=10000, beta=0)
    return dst
import cv2


def convert_range(data):
    dst=cv2.convertScaleAbs(src=data, alpha=10000, beta=10)
    clahe = cv2.createCLAHE(clipLimit=10.0, tileGridSize=(8, 8))
    dst = clahe.apply(dst)
    return dst
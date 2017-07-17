import cv2


def convert_range(data):
    # dst=cv2.convertScaleAbs(src=data, alpha=5000, beta=0)
    clahe = cv2.createCLAHE(clipLimit=10.0, tileGridSize=(20, 20))
    dst = clahe.apply(data)
    return dst
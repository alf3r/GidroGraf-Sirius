import cv2
import numpy as np
import test_openDB


def Bin(data):
    # Выделение линии дна = retval2, thres = cv2.threshold(data, 50,70,cv2.THRESH_BINARY) thres = cv2.blur(thres, (50, 50))
    # Выделение объектов  =

    # retval2, thres = cv2.threshold(data,240,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # thres =cv2.adaptiveThreshold(data, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 0)
    retval2, thres = cv2.threshold(data, 120,127,cv2.THRESH_BINARY)
    # thres = cv2.blur(thres, (50, 50))
    return thres

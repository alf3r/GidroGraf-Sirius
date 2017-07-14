import cv2
import numpy as np
import test_openDB


def Bin(data):
    #retval2, otsu = cv2.threshold(data,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    gaus =cv2.adaptiveThreshold(data, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 155, 1)
    #retval2, treshold2 = cv2.threshold(data, 12,225,cv2.THRESH_BINARY)
    #return treshold2
    return gaus
    #return otsu




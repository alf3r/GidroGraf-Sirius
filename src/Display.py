import cv2
import numpy as np


def display(data_port, data_starboard, img_name):
    data_port = cv2.flip(data_port, 1)
    img = np.concatenate((data_port, data_starboard), axis=1)

    cv2.imshow(img_name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return img
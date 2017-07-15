import cv2
import numpy as np
import matplotlib.pyplot as plt


def display(data_port, data_starboard, img_name, time2show):
    data_port = cv2.flip(data_port, 1)
    img = np.concatenate((data_port, data_starboard), axis=1)

    plt.imshow(img, cmap='bone', interpolation='bicubic')
    # fig, ax = plt.subplots()
    # ax.imshow(img, cmap='bone', interpolation='bicubic')
    # ax.grid(True)
    plt.show()

    # dx, dy = 100, 100
    # grid_color = [0, 0, 0]
    # img[:, ::dy, :] = grid_color
    # img[::dx, :, :] = grid_color
    #
    # cv2.imshow(img_name, img)
    # cv2.waitKey(time2show)
    return img
import cv2
import numpy as np
import matplotlib.pyplot as plt


def display(data_starboard, data_port, img_name, time2show):
    data_starboard = cv2.flip(data_starboard, 1)
    img = np.concatenate((data_starboard, data_port), axis=1)

    plt.imshow(img, cmap='plasma', interpolation='bicubic')
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
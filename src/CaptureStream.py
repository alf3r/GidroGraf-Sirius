import cv2
import numpy as np
import gidroGraf_DBreader as gg
import sqlite3
from matplotlib import pyplot as plt

if __name__ == "__main__":
    c = 1420
    track_name = 'Track01'
    datarate = 72411

    wrapper = gg.Hyscan5wrapper('/home/white-out/hyscan/bin', 'file:///home/white-out/Hyscan5_projects', 'echo2')

    data = wrapper.get_aqoustic_data(track_name, 102)
        # Преобразование изображения (полосок изображения в картинку) а - количество строк, st - это коэффициент
    img0 = np.asarray(data)
    V = 2
    Ln = img0.shape[0]
    Lm = 100
    time0 = 2*Ln/c
    st = Ln/Lm
    img = img0[0:Ln-1, :]

    a = Lm/time0*V
    time = time0*a
    d_points = Ln / a

    scale = a / d_points / st



    screen_width = 600
    screen_height = round(screen_width * scale)
    screen_height = 800
    screen_width = round(screen_height / scale)
    dim = (screen_width, screen_height)


    converted = cv2.convertScaleAbs(src=img, alpha=2000, beta=100)
    resized = cv2.resize(converted, dim, interpolation=cv2.INTER_AREA)



    plt.imshow(resized, interpolation='bicubic')
    plt.show()











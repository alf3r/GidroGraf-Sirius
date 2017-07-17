import cv2
import matplotlib.pyplot as plt
import numpy as np
import Capture


class Sonar_data():

    def __init__(self, id, source_type, datarate, v, c):
        self.id          = id          # Идентификатор источника данных в БД
        self.source_type = source_type # Имя источника данных
        self.datarate    = datarate    # Частота дискретизации, Гц
        self.v           = v           # Скорость движения гидролокатора
        self.c           = c           # Скорость звука в воде

    def set_data(self, data):
        self.data = data
        self.calculate_scale()
        self.data = cv2.flip(self.data, 0)

    def apply_left(self):
        self.data = cv2.flip(self.data, 1)

    def points2range(self, n_points):
        time0 = n_points / self.datarate
        range = self.c * time0 / 2
        return range

    def range2points(self, range):
        return round(2 * self.datarate * range / self.c)

    def calculate_scale(self):
        n_points = self.data.shape[1]
        m_lines  = self.data.shape[0]

        time0 = n_points / self.datarate
        Ltotal = self.points2range(n_points)

        Lpx = Ltotal / n_points
        Hpx = self.v * time0 / 2

        Htotal = Hpx * m_lines

        self.scale = Hpx / Lpx

    def get_image(self, screen_width, screen_height):
        if screen_width == -1:
            screen_width = round(screen_height / self.scale)
        elif screen_height == -1:
            screen_height = round(screen_width * self.scale)
        image_dimention = (screen_width, screen_height)
        return cv2.resize(self.data, image_dimention, interpolation=cv2.INTER_AREA)

    def binarize(self):
        # Выделение линии дна = retval2, thres = cv2.threshold(data, 50,70,cv2.THRESH_BINARY) thres = cv2.blur(thres, (50, 50))
        # Выделение объектов  =
        # retval2, thres = cv2.threshold(data,240,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        # thres =cv2.adaptiveThreshold(data, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 0)
        retval2, thres = cv2.threshold(self.data, 60, 80, cv2.THRESH_BINARY)
        # thres = cv2.blur(thres, (50, 50))
        self.data = thres

    def convert_range(self):
        # clahe = cv2.createCLAHE(clipLimit=90, tileGridSize=(33, 33))
        # a = self.data.view((np.uint8, 4))
        # a = a[:, :, 3]
        # a = clahe.apply(a)
        # a = cv2.convertScaleAbs(self.data, alpha=35000, beta=-150)
        # self.data = a

        # Коррекция яркости по диапазону
        figure, axes = plt.subplots(1, 4, sharey=True)
        for i in range(0, 4):
            k = (i+0)*2000 + 30000
            a = cv2.convertScaleAbs(self.data, alpha=k, beta=-120)
            a1 = np.median(a, 0)
            axes[i].hist(a1, 256, fc='k', ec='k')
            axes[i].set_title('beta=' + str(k))
        plt.show()
        self.data = a

        # Исследование коррекции яркости Клахе
        # figure, axes = plt.subplots(1, 4, sharey=True)
        # for i in range(0, 4):
        #     k = (i)*3 + 30
        #     clahe = cv2.createCLAHE(clipLimit=90, tileGridSize=(33 , 33))
        #     a1 = clahe.apply(a)
        #     a1 = np.median(a1, 0)
        #     axes[i].hist(a1, 256, range=(0.0, 1.0), fc='k', ec='k')
        #     axes[i].set_title('clipLimit=' + str(k))
        # plt.show()

        # Исследование динамического диапазона
        # figure, axes = plt.subplots(1, 4, sharey=True)
        # ay = 0
        # iy = 0
        # for i in range(0,4):
        #     a1 = a[:, :, i]
        #     a1 = Capture.data2image(a1, self.scale, 1000, -1)
        #     a1 = clahe.apply(a1)
        #     axes[i].imshow(a1, cmap='bone', interpolation='bicubic')
        #     ax = np.median(np.mean(a1, 0)) - 127
        #     if abs(ax) > abs(ay):
        #         ay = ax
        #         iy = i
        # self.data = a[:, :, iy]
        # plt.show()


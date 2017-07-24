import cv2
import matplotlib.pyplot as plt
import numpy as np
import Capture

class Sonar():

    def set_port(self, port):
        self.port = port

    def set_starboard(self, starboard):
        self.starboard = starboard


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
        self.data = cv2.resize(self.data, image_dimention, interpolation=cv2.INTER_AREA)

    def binarize(self):
        # Выделение линии дна = retval2, thres = cv2.threshold(data, 50,70,cv2.THRESH_BINARY) thres = cv2.blur(thres, (50, 50))
        # Выделение объектов  =
        a = cv2.adaptiveThreshold(self.data, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 125, 1)

        # a = cv2.adaptiveThreshold(a, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 55, 1)
        # retval2, a = cv2.threshold(self.data, 90, 255, cv2.THRESH_BINARY)
        # a1 = np.median(a, 0)
        # plt.hist(a1, 256, range=[0, 255], fc='k', ec='k')
        # plt.show()
        self.data = a

    def blur(self):
        px = 5
        self.data = cv2.blur(self.data, (px, px))
        # self.data = cv2.medianBlur(self.data, px)

    def find_contours(self):
        im2, contours, hierarchy = cv2.findContours(self.data, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.data = cv2.cvtColor(self.data, cv2.COLOR_GRAY2RGB)
        cv2.drawContours(self.data, contours, -1, (255, 0, 0), 20)

    def convert_range(self):
        for i in range(1,30):
            alpha = 1000*i
            a = cv2.convertScaleAbs(self.data, alpha=alpha, beta=0)
            beta = 127 - np.median(a, [0, 1])
            a = cv2.convertScaleAbs(self.data, alpha=alpha, beta=beta)

            condition = np.mod(a, 255) == 0
            K = np.sum(condition) / a.size
            if K > 0.1:
                break
        self.data = a

    def extend_data(self, zeros_arr):
        zeros_arr += zeros_arr + 30
        self.data = np.hstack((self.data, zeros_arr))


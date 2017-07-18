import os
import matplotlib.pyplot as plt
import cv2
import numpy as np

from gidroGraf_DBreader import Hyscan5wrapper
from Sonar_data import Sonar_data


if __name__ == "__main__":
    # Задаем исходные данные
    source_starboard = 101 # Правый борт
    source_port      = 102 # Левый борт

    source = source_starboard
    c = 1500  # скорость звука
    v = 1     # скорость гидролокатора
    depth = 0 # глубина под гидролокатором
    current_path = os.getcwd()
    path2hyscanbin = r'/media/alf/Storage/hyscan-builder-linux/bin'
    path2hyscanprj = r'/media/alf/Storage/Hyscan5_projects'
    project_name = 'echo2'
    track_name = 'Track08'

    try:
        # ============================РАБОТА С БАЗОЙ ДАННЫХ=============================================================
        # Читалка БД, созадем экземпляр класса gidroGraf_DBreader
        DB = Hyscan5wrapper(path2hyscanbin, path2hyscanprj, project_name)

        # Читаем информацию о галсе [id, начаьный индекс строк, конечный индекс строк]
        track = DB.get_track_id(track_name, source)
        track_id = track[0]
        track_size = track[1:]
        datarate = DB.read_datarate(track_name, source)

        # Экземпляр класса - Обработчик данных от гидролокатора
        sonar_data = Sonar_data(track_id, 'Sonar_Data', datarate, v, c)

        # Определяем число строк, которое нужно считать
        count_totalLines = track_size[1] - track_size[0] # ОБщее число строк в БД
        count_lines2read = count_totalLines # Число строк, которое мы хотим считать

        # Считываем строки из БД и сохраняем их в оперативную память в объект data_starboard
        data      = DB.read_lines(sonar_data.id, track_size[0], count_lines2read)
        N = sonar_data.range2points(depth) # Начальный индекс точек, которые мы будем обрабатывать (в зависимости от глубины)
        M = 0  # Начальный индекс строк, который мы будем обрабатывать
        sonar_data.set_data(data[M:, N:])
        # sonar_data.apply_left()
        data = []


        # ============================ОБРАБОТКА ДАННЫХ==================================================================
        # Совершаем обработку
        alpha = 20000
        a = cv2.convertScaleAbs(self.data, alpha=alpha, beta=0)
        beta = 127 - np.median(a, [0, 1])
        a = cv2.convertScaleAbs(self.data, alpha=alpha, beta=beta)
        # a = clahe.apply(a)
        self.data = a


        sonar_data.convert_range() # Переводим данные в 8бит и корректируем яркость
        sonar_data.binarize()      # Переводим данные в 2бит
        # sonar_data.blur()
        #
        # Выделяем контуры
        sonar_data.find_contours()

        img = sonar_data.get_image(1000, -1)
        #
        plt.imshow(img, cmap='bone', interpolation='bicubic', clim=(0, 255))
        plt.show()

    except Exception as err:
        raise err
import os
import matplotlib.pyplot as plt
import numpy as np
import cv2

from gidroGraf_DBreader import Hyscan5wrapper
from Sonar_data import Sonar_data


def range2points(range, datarate, c):
        return round(2 * datarate * range / c)

def points2range(n_points, datarate, c):
        time0 = n_points / datarate
        range = c * time0 / 2
        return range


if __name__ == "__main__":
    # Задаем исходные данные
    source_starboard = 101 # Правый борт
    source_port      = 102 # Левый борт

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
        track_port = DB.get_track_id(track_name, source_port)
        track_starboard = DB.get_track_id(track_name, source_starboard)

        track_id_port = track_port[0]
        track_size_port = track_port[1:]
        datarate_port = DB.read_datarate(track_name, source_port)

        track_id_starboard = track_starboard[0]
        track_size_starboard = track_starboard[1:]
        datarate_starboard = DB.read_datarate(track_name, source_starboard)

        # Экземпляр класса - Обработчик данных от гидролокатора
        sonar_port      = Sonar_data(track_id_port,      'Sonar_Port',      datarate_port, v, c)
        sonar_starboard = Sonar_data(track_id_starboard, 'Sonar_Starboard', datarate_starboard, v, c)

        # Определяем число строк, которое нужно считать
        count_totalLines = track_size_port[1] - track_size_port[0] # ОБщее число строк в БД
        count_lines2read = count_totalLines # Число строк, которое мы хотим считать

        # Считываем строки из БД и сохраняем их в оперативную память в объект data_starboard
        data_port      = DB.read_lines(sonar_port.id, track_size_port[0], count_lines2read)
        data_starboard = DB.read_lines(sonar_starboard.id, track_size_starboard[0], count_lines2read)


        N_port = sonar_port.range2points(depth) # Начальный индекс точек, которые мы будем обрабатывать (в зависимости от глубины)
        N_starboard = sonar_starboard.range2points(depth)  # Начальный индекс точек, которые мы будем обрабатывать (в зависимости от глубины)
        M = 0  # Начальный индекс строк, который мы будем обрабатывать

        sonar_port.set_data(data_port[M:, N_port:])
        sonar_starboard.set_data(data_starboard[M:, N_starboard:])
        sonar_port.apply_left()
        data_port = []
        data_starboard = []



       # ============================ОБРАБОТКА ДАННЫХ==================================================================
        sonar_port.convert_range()
        sonar_starboard.convert_range()

        sonar_port.get_image(-1, 6000)
        sonar_starboard.get_image(-1, 6000)

        if sonar_port.data.size > sonar_starboard.data.size:
            zeros_arr = np.zeros((sonar_port.data.shape[0], sonar_port.data.shape[1] - sonar_starboard.data.shape[1]))
            sonar_starboard.extend_data(zeros_arr)
            img_datarate = sonar_starboard.datarate
        else:
            zeros_arr = np.zeros((sonar_starboard.data.shape[0], sonar_starboard.data.shape[1] - sonar_port.data.shape[1]))
            sonar_port.extend_data(zeros_arr)
            img_datarate = sonar_port.datarate

        img = np.concatenate((sonar_port.data, sonar_starboard.data), axis=1).astype('uint8')

        sonar_port.data = []
        sonar_starboard.data = []
        zeros_arr = []

        # Совершаем обработку
        clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(30, 30))
        img = clahe.apply(img)
        a1 = np.median(img, 0)
        plt.hist(a1, 256, range=[0, 255], fc='k', ec='k')
        plt.show()
        a = cv2.blur(img, (20, 20))
        # a = cv2.adaptiveThreshold(a, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 201, 1)
        retval2, a = cv2.threshold(a, 160, 255, cv2.THRESH_BINARY)

        im2, contours, hierarchy = cv2.findContours(a, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        object_areaMin_px = range2points(500, img_datarate, c)
        object_areaMax_px = range2points(1200, img_datarate, c)
        new_boxes = []
        new_contours = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if (area < object_areaMax_px) & (area > object_areaMin_px):
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                # convert all coordinates floating point values to int
                box = np.int0(box)
                # draw a red 'nghien' rectangle
                new_contours.append(cnt)
                new_boxes.append(box)
                area_m = "%.1f" % (points2range(area, img_datarate, c))
                cv2.putText(img, area_m, (box[0][0], box[0][1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        contours = []

        cv2.drawContours(img, new_contours, -1, (0, 255, 0), 2)
        cv2.drawContours(img, new_boxes,    -1, (255, 0, 0), 10)

        figure, axes = plt.subplots(1, 2, sharey=True)
        axes[0].imshow(a, cmap='inferno', interpolation='bicubic', clim=(0, 255))
        axes[1].imshow(img, interpolation='bicubic', clim=(0, 255))
        plt.show()


    except Exception as err:
        raise err


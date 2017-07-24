import gidroGraf_DBreader as gg
import cv2
import Bright
import Capture
import numpy as np
import Display
import Binarize
import os
import matplotlib.pyplot as plt


if __name__ == "__main__":
    # Задаем исходные данные
    c = 1420 #скорость звука
    v = 5    #скорость гидролокатора
    current_path   = os.getcwd()
    path2hyscanbin = r'/media/alf/Storage/hyscan-builder-linux/bin'
    path2hyscanprj = r'/media/alf/Storage/Hyscan5_projects'
    project_name   = 'echo2'
    track_name     = 'Track08'

    # Созадем экземпляр класса gidroGraf_DBreader
    DB = gg.Hyscan5wrapper(path2hyscanbin, path2hyscanprj, project_name)
    try:
        datarate = DB.read_datarate(track_name)
    except Exception as err:
        raise err

    # Читаем информацию о галсе [id, начаьный индекс строк, конечный индекс строк]
    track_port      = DB.get_track_id(track_name, 101)
    track_starboard = DB.get_track_id(track_name, 102)

    # Считываем строки из БД
    count_totalLines = track_port[2] - track_port[1]
    count_lines2read = count_totalLines
    count_reads      = round(count_totalLines / count_lines2read)

    step = 100
    i    = 0

    while True:
        data_port      = DB.read_lines(track_port[0],      track_port[1] + round(count_lines2read*i/step), count_lines2read)
        data_starboard = DB.read_lines(track_starboard[0], track_starboard[1] + round(count_lines2read*i/step), count_lines2read)

        N = Capture.range2points(30, datarate, c)
        M = 200
        data_port      = data_port[M:, N:]
        data_starboard = data_starboard[M:, N:]

        data_port      = Bright.convert_range(data_port)
        data_starboard = Bright.convert_range(data_starboard)

        data_port      = Capture.CalculateDim(data_port,      v, c, 1600, -1, datarate)
        data_starboard = Capture.CalculateDim(data_starboard, v, c, 1600, -1, datarate)

        img = Display.display(data_port, data_starboard, project_name + '-' + track_name, 0)

        img_processed = Binarize.Bin(img)

        if i == (count_reads - 1) * step:
            break
        else:
            Display.display(data_port, data_starboard, project_name + '-' + track_name, 10)
            i += 1

    im2, contours, hierarchy = cv2.findContours(img_processed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    cv2.drawContours(img, contours, -1, (255, 0, 0), 20)

    plt.imshow(img, cmap='plasma', interpolation='bicubic')
    plt.show()
    cv2.imwrite(current_path + '/' + 'test.png', img)

    cv2.destroyAllWindows()


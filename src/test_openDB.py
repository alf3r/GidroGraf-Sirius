import gidroGraf_DBreader as gg
import cv2
import Bright
import Capture
import time
import  numpy as np


if __name__ == "__main__":
    # Задаем исходные данные
    c = 1420 #скорость звука
    v = 1    #скорость гидролокатора
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

    step = 50
    i    = 0

    while True:
        data_port       = DB.read_lines(track_port[0],      track_port[1] + round(count_lines2read*i/step), count_lines2read)
        data_starboard  = DB.read_lines(track_starboard[0], track_starboard[1] + round(count_lines2read*i/step), count_lines2read)

        dim = Capture.CalculateDim(data_port, 2, 1420, count_lines2read, 800, -1)

        data_port       = Bright.convert_range(data_port)
        data_starboard  = Bright.convert_range(data_starboard)

        data_port      = cv2.resize(data_port,      dim, interpolation=cv2.INTER_AREA)
        data_starboard = cv2.resize(data_starboard, dim, interpolation=cv2.INTER_AREA)



        if i == (count_reads - 1) * step:
            break
        else:
            cv2.imshow('PORT', data_port)
            cv2.imshow('STARBOARD', data_starboard)
            cv2.waitKey(10)
            i += 1

    # # Адаптивное выравнивание яркости и контраста
    # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    # processed = clahe.apply(converted)

    ret, thresh = cv2.threshold(data_port, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(data_port, contours, -1, (0, 255, 0), 2)

    cv2.imshow('PORT', data_port)
    cv2.imshow('thresh', thresh)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
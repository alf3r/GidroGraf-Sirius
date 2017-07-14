import gidroGraf_DBreader as gg
import cv2
import Bright
import Capture
import numpy as np
import Display


if __name__ == "__main__":
    # Задаем исходные данные
    path2hyscanbin = '/home/sirius/hyscan/bin'
    path2hyscanprj = '/home/sirius/Hyscan5_projects'
    project_name = 'echo2'
    track_name = 'Track08'

    # Созадем экземпляр класса gidroGraf_DBreader
    DB = gg.Hyscan5wrapper(path2hyscanbin, path2hyscanprj, project_name)
    try:
        datarate = DB.read_datarate(track_name)
    except Exception as err:
        raise err

    # Читаем информацию о галсе [id, начаьный индекс строк, конечный индекс строк]
    track_port = DB.get_track_id(track_name, 101)
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

    data_port      = Capture.CalculateDim(data_port, 5, 1500, -1, 640, datarate)
    data_starboard = Capture.CalculateDim(data_starboard, 5, 1500, -1, 640, datarate)

    Display.display(data_port, data_starboard, project_name + ' - ' + track_name)
    # # Адаптивное выравнивание яркости и контраста


    # Отображение картинок



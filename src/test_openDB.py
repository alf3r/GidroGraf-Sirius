import gidroGraf_DBreader as gg
import cv2
import Bright
import Capture
import numpy as np


if __name__ == "__main__":
    # Задаем исходные данные
    c = 1420 #скорость звука
    v = 1    #скорость гидролокатора
    path2hyscanbin = '/home/sirius/hyscan/bin'
    path2hyscanprj = '/home/sirius/Hyscan5_projects'
    project_name   = 'echo2'
    track_name     = 'Track01'

    # Созадем экземпляр класса gidroGraf_DBreader
    DB = gg.Hyscan5wrapper(path2hyscanbin, path2hyscanprj, project_name)
    try:
        datarate   = DB.read_datarate(track_name)
    except Exception as err:
        raise err

    # Читаем информацию о галсе [id, начаьный индекс строк, конечный индекс строк]
    track_port = DB.get_track_id(track_name, 101)
    track_starboard = DB.get_track_id(track_name, 102)

    # Считываем строки из БД
    count_lines2read = 1000
    data_port = DB.read_lines(track_port[0], track_port[1], count_lines2read)
    data_starboard = DB.read_lines(track_starboard[0], track_starboard[1], count_lines2read)

    data_port = Bright.convert_range(data_port)
    data_starboard = Bright.convert_range(data_starboard)

    data_port = Capture.CalculateDim(data_port,      2, 1420, 1000, 800)
    data_starboard = Capture.CalculateDim(data_starboard, 2, 1420, 1000, 800)

    data_port = cv2.flip(data_port, 1)

    img = np.concatenate((data_port,data_starboard), axis = 1)
    # # Адаптивное выравнивание яркости и контраста
    # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    # processed = clahe.apply(converted)

    # Отображение картинок

    cv2.imshow('IMG', img)


    cv2.waitKey(0)
    cv2.destroyAllWindows()

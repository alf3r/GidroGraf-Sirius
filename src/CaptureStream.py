import cv2
import numpy as np
import gidroGraf_DBreader as gg
import sqlite3
from matplotlib import pyplot as plt
import Capture


def read_datarate(filename):
    filestring = open(filename, 'r').read()
    idx_beg = filestring.find('/data/rate=') + 11
    idx_end = filestring[idx_beg:idx_beg+7].find('\n') + idx_beg
    if idx_beg == -1:
        raise Exception('Невозможно прочитать проект, не найдена частота дискретизации')
    a = int(filestring[idx_beg:idx_end])
    return a


if __name__ == "__main__":
    c = 1420
    track_name = 'Track01'
    path2hyscanbin = '/home/sirius/hyscan/bin'
    path2hyscanprj = '/home/sirius/Hyscan5_projects'
    project_name = 'echo2'
    file4params = path2hyscanprj + '/' + project_name + '/' + track_name + '/' + 'track.prm'
    try:
        datarate   = read_datarate(file4params)
    except Exception as err:
        raise err

    DB = gg.Hyscan5wrapper(path2hyscanbin, 'file://' + path2hyscanprj, project_name)
    # Читаем информацию о галсе [id, начаьный индекс строк, конечный индекс строк]
    track_port = DB.get_track_id(track_name, 101)
    track_starboard = DB.get_track_id(track_name, 102)
    # Считываем строки из БД
    count_lines2read = 250
    data_port = DB.read_lines(track_port[0], track_port[1], count_lines2read)
    data_starboard = DB.read_lines(track_starboard[0], track_starboard[1], count_lines2read)


    img = Capture.CalculateDim(data_port,2, 1420, 200, datarate )
    cv2.imshow('PORT', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

















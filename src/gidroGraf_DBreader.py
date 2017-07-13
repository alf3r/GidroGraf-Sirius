import ctypes
import numpy as np
from ctypes import *
import os.path

class Hyscan5wrapper():
    def __init__(self, path2Hyscan5bin, path2hyscanprj, Project_name):
        """ КОНСТРУКТОР """
        # path2Hyscan5bin = '/media/alf/Storage/hyscan-builder-linux/bin'
        # path2hyscanprj  = '/media/alf/Storage/Hyscan5_projects'
        # DB_name = 'file://D:/Hyscan5_projects'
        # project_name = 'line'
        self.path2Hyscan5bin = path2Hyscan5bin
        self.path2hyscanprj  = path2hyscanprj
        self.DB_name = ('file://' + path2hyscanprj).encode('ascii', 'replace')
        self.Project_name = Project_name
        os.chdir(self.path2Hyscan5bin)

        # Загружаем DLL для чтения БД ГидроГраф
        if os.name == 'nt':
            suffix = 'dll'
        else:
            suffix = 'so'
        dllname_db = os.path.join(self.path2Hyscan5bin, 'libcpp_bd_wrap.' + suffix)
        dllname_db = os.path.normpath(dllname_db)
        dllname_ra = os.path.join(self.path2Hyscan5bin, 'libcpp_acoustic_wrap.' + suffix)
        dllname_ra = os.path.normpath(dllname_ra)
        self.DB = ctypes.CDLL(dllname_db)
        self.RA = ctypes.CDLL(dllname_ra)

        # Подключаемся к БД
        try:
            if 0 != self.DB.connect_to_bd(self.DB_name):
                msg = 'Fatal error: connect_to_database: connection to database failed or HyScanRawData was not created'
                raise Exception(msg)
        except Exception as err:
            raise err

    def get_track_id(self, track_name, source_type):
        # track_name =  'Track01'
        # source_type = 101 - для Port
        # source_type = 102 - для Starboard
        is_raw = True
        trk = track_name.encode('ascii', 'replace')
        prj = self.Project_name.encode('ascii', 'replace')
        id = self.RA.acoustic_data_new(prj, trk, source_type, is_raw)
        idx_first = self.RA.get_first_index_in_range(id)
        idx_last = self.RA.get_last_index_in_range(id)
        return id, idx_first, idx_last

    def read_lines(self, track_id, offset, count):
        lines = []
        for i in range(0, count - 1):
            num_values = self.RA.get_values_count(track_id, i) #найти число точек в строке
            buffer_output = (c_float * num_values)() #резервируем место в памяти
            num_values = self.RA.get_values(track_id, offset + i, byref(buffer_output), num_values) #читаем строки из БД
            lines.append(buffer_output)
        return np.asarray(lines)

    def read_datarate(self, track_name):
        # filename = path2hyscanprj + '/' + project_name + '/' + track_name + '/' + 'track.prm'
        filename = os.path.join(self.path2hyscanprj, self.Project_name, track_name, 'track.prm')
        filestring = open(filename, 'r').read()
        idx_beg = filestring.find('/data/rate=') + 11
        idx_end = filestring[idx_beg:idx_beg + 7].find('\n') + idx_beg
        if idx_beg == -1:
            raise Exception('Невозможно прочитать проект, не найдена частота дискретизации')
        a = int(filestring[idx_beg:idx_end])
        return a

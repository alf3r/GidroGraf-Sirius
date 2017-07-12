import ctypes
import numpy as np
from ctypes import *
import os.path

class Hyscan5wrapper():
    def __init__(self, path2Hyscan5bin, DB_name, Project_name):
        """ КОНСТРУКТОР """
        # DB_name = 'file://D:/Hyscan5_projects'
        # project_name = 'line'
        # track =  'Track01'
        self.path2Hyscan5bin = path2Hyscan5bin
        self.DB_name = DB_name.encode('ascii', 'replace')
        self.Project_name = Project_name.encode('ascii', 'replace')
        os.chdir(self.path2Hyscan5bin)

        # Загружаем DLL для чтения БД ГидроГраф
        dllname_db = os.path.join(self.path2Hyscan5bin, 'libcpp_bd_wrap.so')
        dllname_db = os.path.normpath(dllname_db)
        dllname_ra = os.path.join(self.path2Hyscan5bin, 'libcpp_acoustic_wrap.so')
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
        is_raw = True
        trk = track_name.encode('ascii', 'replace')
        id = self.RA.acoustic_data_new(self.Project_name, trk, source_type, is_raw)
        idx_first = self.RA.get_first_index_in_range(id)
        idx_last = self.RA.get_last_index_in_range(id)
        return id, idx_first, idx_last

    def read_lines(self, track_id, offset, count):
        lines = []
        for i in range(offset + count - 1):
            num_values = self.RA.get_values_count(track_id, i) #найти число точек в строке
            buffer_output = (c_float * num_values)() #резервируем место в памяти
            num_values = self.RA.get_values(track_id, i, byref(buffer_output), num_values) #читаем строки из БД
            lines.append(buffer_output)
        return np.asarray(lines)

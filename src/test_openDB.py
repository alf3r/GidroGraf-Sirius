import gidroGraf_DBreader as gg
import cv2
import Bright


if __name__ == "__main__":
    # Задаем исходные данные
    c = 1420 #скорость звука
    v = 1    #скорость гидролокатора
    path2hyscanbin = '/media/alf/Storage/hyscan-builder-linux/bin'
    path2hyscanprj = '/media/alf/Storage/Hyscan5_projects'
    project_name   = 'line'
    track_name     = 'Track01'

    # Созадем экземпляр класса gidroGraf_DBreader
    DB = gg.Hyscan5wrapper(path2hyscanbin, path2hyscanprj, project_name)
    try:
        datarate   = DB.read_datarate(track_name)
    except Exception as err:
        raise err

    # Читаем информацию о галсе [id, начаьный индекс строк, конечный индекс строк]
    track_port      = DB.get_track_id(track_name, 101)
    track_starboard = DB.get_track_id(track_name, 102)

    # Считываем строки из БД
    count_lines2read = 100
    data_port       = DB.read_lines(track_port[0], track_port[1], count_lines2read)
    data_starboard  = DB.read_lines(track_starboard[0], track_starboard[1], count_lines2read)

    data_port       = Bright.convert_range(data_port)
    data_starboard  = Bright.convert_range(data_starboard)

    # # Сжатие динамического диапазона
    # converted = cv2.convertScaleAbs(src=data_port, alpha=2000, beta=0)
    #
    # # Адаптивное выравнивание яркости и контраста
    # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    # processed = clahe.apply(converted)

    # Отображение картинок
    cv2.imshow('PORT', data_port)
    cv2.imshow('STARBOARD', data_starboard)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # # Вычисляем параметры масштабирования
    # m_lines_orig = img0.shape[0]
    # m_lines_wanted = 1000
    # scale_lines = round(m_lines_orig/m_lines_wanted)
    #
    # img = img0[0:m_lines_wanted-1, :]
    # m_lines = img.shape[0]
    # n_points = img.shape[1]
    #
    # time = n_points / datarate
    # distance = c * time
    # d_points = distance / n_points
    # d_lines = time * v
    # scale = d_lines / d_points / scale_lines
    #
    # screen_width = 600
    # screen_height = round(screen_width * scale)
    #
    # # screen_height = 800
    # # screen_width  = round(screen_height / scale)
    #
    # dim = (screen_width, screen_height)
    #
    # # Обрабатываем изображение
    # converted = cv2.convertScaleAbs(src=img, alpha=2000, beta=100)
    #
    # # r = 100.0 / img.shape[1]
    # # dim = (100, int(img.shape[0] * r))
    #
    # resized = cv2.resize(converted, dim, interpolation=cv2.INTER_AREA)
    #
    # # cv2.imshow("converted", converted)
    # # cv2.waitKey(0)
    #
    # # img1 = cv2.resize(src=img, dsize=0, fx=0.1, fy=10)
    # # img2 = cv2.convertScaleAbs(src=img, alpha=1000, beta=0)
    # #
    # # # img = img - img.min()
    # # img = img * 255 / img.max()
    #
    # # retval, th = cv2.threshold(img, 40, 255, cv2.THRESH_BINARY)
    #
    # plt.imshow(resized, interpolation='bicubic')
    # plt.show()
    #
    # # cv2.imshow("original", resized)
    # # # cv2.imshow("threshold", th)
    # # #
    # # while True:
    # #     keycode = cv2.waitKey()
    # #     if keycode == 27: # ESC
    # #         break
    # #
    # # cv2.distroyAllWindows

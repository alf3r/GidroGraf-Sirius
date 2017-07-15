import cv2

def points2range(n_points, datarate, c):
    return n_points * c / 2 / datarate

def range2points(range, datarate, c):
    return round(2 * datarate * range / c)

def CalculateDim(data, V, c, screen_width, screen_height, datarate):
    # Lm - число строк

    # Ln = data.shape[0] #Количество точек в строке
    # Lm = data.shape[1]  # Количество строк
    # time0 = c/(datarate*Ln*V) #Время за которое проявляетс 1 строка
    # img = data[0:Ln - 1, :]
    # # КОличество строк это Lm
    # S = time0*Lm*V # Путь, который проходит корабль с гидролокатором
    # N = time0*c #Путь который пройдет луч
    #
    # #screen_height = round((N*screen_width)/S)

    n_points = data.shape[0]
    m_lines  = data.shape[1]

    time0 = n_points / datarate

    Lpx   = c / datarate
    Hpx   = V * time0
    scale = Hpx / Lpx

    if screen_width == -1:
        screen_width = round(screen_height / scale)
    elif screen_height == -1:
        screen_height = round(screen_width * scale)


    dim = (screen_width,screen_height)
    data = cv2.resize(data, dim, interpolation=cv2.INTER_AREA)
    return data


import cv2

def points2range(n_points, datarate, c):
    time0 = n_points / datarate
    range = c * time0 / 2
    return range

def range2points(range, datarate, c):
    return round(2 * datarate * range / c)

def CalculateDim(data, V, c, screen_width, screen_height, datarate):
    n_points = data.shape[1]
    m_lines  = data.shape[0]

    time0 = n_points / datarate
    Ltotal = points2range(n_points, datarate, c)

    Lpx   = Ltotal / n_points
    Hpx   = V * time0 / 2

    Htotal = Hpx * m_lines

    scale = Hpx / Lpx

    if screen_width == -1:
        screen_width = round(screen_height / scale)
    elif screen_height == -1:
        screen_height = round(screen_width * scale)

    dim = (screen_width,screen_height)
    # data = cv2.resize(data, dim, interpolation=cv2.INTER_AREA)
    return dim


def data2image(data, scale, screen_width, screen_height):
    if screen_width == -1:
        screen_width = round(screen_height / scale)
    elif screen_height == -1:
        screen_height = round(screen_width * scale)
    return cv2.resize(data, (screen_width, screen_height), interpolation=cv2.INTER_AREA)
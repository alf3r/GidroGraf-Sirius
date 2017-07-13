import cv2

def CalculateDim(data, V, c, Lm, screen_height):
    # Lm - число строк

    Ln = data.shape[0]
    time0 = 2 * Ln / c
    st = Ln / Lm
    img = data[0:Ln - 1, :]
    a = Lm / time0 * V
    d_points = Ln / a

    screen_width = round(screen_height * st * d_points)
    dim = (screen_width, screen_height)
    data = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return data


import cv2

def CalculateDim(data, V, c, Lm, screen_height, screen_width):
    # Lm - число строк

    Ln = data.shape[0]
    time0 = 2 * Ln / c
    st = Ln / Lm
    img = data[0:Ln - 1, :]
    a = Lm / time0 * V
    d_points = Ln / a

    if screen_width == -1:
        screen_width = round(screen_height * st * d_points)
    elif screen_height == -1:
        screen_height = round(screen_width / st / d_points)
    dim = (screen_width, screen_height)
    return dim


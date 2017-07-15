import cv2

def CalculateDim(data, V, c, screen_width,screen_height,datarate):
    # Lm - число строк

    Ln = data.shape[0] #Количество точек в строке
    Lm = data.shape[1]  # Количество строк
    time0 = c/(datarate*Ln*V) #Время за которое проявляетс 1 строка
    img = data[0:Ln - 1, :]
    # КОличество строк это Lm
    S = time0*Lm*V # Путь, который проходит корабль с гидролокатором
    N = time0*c #Путь который пройдет луч

    #screen_height = round((N*screen_width)/S)

    if screen_width == -1:
        screen_width = round(((N*screen_height)/S)+200)
    elif screen_height == -1:
        screen_height = round(((S*screen_height)/N)+200)


    dim = (screen_width,screen_height)
    data = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return data


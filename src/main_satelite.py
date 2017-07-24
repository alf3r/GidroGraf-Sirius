import cv2
import numpy as np
import matplotlib.pyplot as plt

from scipy import ndimage as sc

# Загрузка
filename = '../img/satelite.tif'

img = sc.imread(filename)
# img = img[0:8000, 0:8000]

# # Коррекция гистограммы
for i in range(1, 30):
    alpha = 1 * i
    a = cv2.convertScaleAbs(img, alpha=alpha, beta=0)
    beta = 127 - np.median(a, [0, 1])
    a = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

    condition = np.mod(a, 255) == 0
    K = np.sum(condition) / a.size
    if K > 0.1:
        break

# a1 = np.median(a, 0)
# plt.hist(a1, 256, range=[0, 255], fc='k', ec='k')
# plt.show()

img = []

clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(30, 30))
img = clahe.apply(a)
#
#
# Размытие и бинаризация
a = []

a = cv2.blur(img, (20, 20))
# a = cv2.adaptiveThreshold(a, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 201, 1)
retval2, a = cv2.threshold(a, 80, 255, cv2.THRESH_BINARY)


# Поиск контуров
im2, contours, hierarchy = cv2.findContours(a, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

new_boxes = []
new_contours = []
for cnt in contours:
    area = cv2.contourArea(cnt)
    if (area < 1000000) & (area > 1000):
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        # convert all coordinates floating point values to int
        box = np.int0(box)
        # draw a red 'nghien' rectangle
        new_contours.append(cnt)
        new_boxes.append(box)
        area = float(area)/9698
        area_m = "%.1f km2" % area
        cv2.putText(img, area_m, (box[0][0] + 50, box[0][1] + 50), cv2.FONT_HERSHEY_COMPLEX, 4, (0, 0, 0), 8, cv2.LINE_AA)

# 5.35
# 51883

contours = []

cv2.drawContours(img, new_contours, -1, (0, 255, 0), 2)
cv2.drawContours(img, new_boxes, -1, (255, 0, 0), 10)

# Отображение
# figure, axes = plt.subplots(1, 2, sharey=True)
# axes[0].imshow(a, cmap='inferno', interpolation='bicubic', clim=(0, 255))
# axes[1].imshow(img, interpolation='bicubic', clim=(0, 255))
plt.imshow(img, interpolation='bicubic', clim=(0, 255))
plt.show()



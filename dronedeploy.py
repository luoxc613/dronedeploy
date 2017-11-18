import math

import cv2
import numpy as num
imgpath = 'Camera Localization/IMG_6726.jpg'
img = cv2.imread(imgpath)
print("Processing image: ", imgpath)
img = cv2.resize(img, (500, 900))
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

re, threshold = cv2.threshold(imgray, 150, 255, cv2.THRESH_BINARY)

contourimage, contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
cv2.imshow("contoured image", img)
cv2.imwrite("process/during.PNG", img)


areas = [cv2.contourArea(contour) for contour in contours]

max_area_index = num.argmax(areas)

patterncontour = contours[max_area_index]

dirc = {}
for c in contours:
    
    value = cv2.moments(c)
    if value["m00"] == 0:
        continue
    cX = int(value["m10"] / value["m00"])
    cY = int(value["m01"] / value["m00"])
    if dirc.get((cX, cY), 0):
        dirc[(cX, cY)] += 1  
    else:
        dirc[(cX, cY)] = 1  
three_hits = []
two_hits = []
for key in dirc:
    if dirc[key] == 3:
        three_hits.append(key)
    if dirc[key] == 2:
        two_hits.append(key)

if len(three_hits) == 3:
    pass
elif len(three_hits) == 2:
    pass
else:
    pass


rect = cv2.minAreaRect(patterncontour)

box = cv2.boxPoints(rect)


box = num.int0(box)

cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
rotatedangle = rect[2]

print("Rotation Angle : {0:.2f} ".format(rotatedangle))
def mid_point(point_X, point_Y):
    return [(point_X[0] + point_Y[0]) / 2, (point_X[1] + point_Y[1]) / 2]


def distance(point_X, point_Y):
    return math.sqrt((point_X[0] - point_Y[0]) ** 2 + (point_X[1] - point_Y[1]) ** 2)



min_dist = 1000

for point in box:
    temp_dist = distance(patterncontour[0][0], point)
    min_dist = min(min_dist, temp_dist)

print("Degree :  {0:.2f} ".format(min_dist))


P = box[0]
Q = box[1]
R = box[2]
S = box[3]


P_Q = mid_point(P, Q)
R_S = mid_point(R, S)
P_S = mid_point(P, S)
Q_R = mid_point(Q, R)


PS_QR_dist = distance(P_S, Q_R)
PQ_RS_dist = distance(P_Q, R_S)

if PS_QR_dist > PQ_RS_dist:
    width = PS_QR_dist
    height = PS_QR_dist
else:
    width = PS_QR_dist
    height = PS_QR_dist


width_ratio1 = 300
height_ratio1 = 600

width_ratio2 = 130
height_ratio2= 250


one_foot_height = 1 / (height / height_ratio1)
one_foot_width = 1 / (width / width_ratio1)

two_foot_height = 2 / (height / height_ratio2)
two_foot_width = 2 / (width / width_ratio2)

distance_away = (one_foot_width + one_foot_height + two_foot_width + two_foot_height) / 4

print("Image move {0:.2f} feet ".format(distance_away, min_dist, rotatedangle))

cv2.drawContours(img, contours, max_area_index, (0, 125, 0), 3)
cv2.imshow("result image", img)
cv2.imwrite("process/result.PNG", img); 
cv2.waitKey(0)
cv2.destroyAllWindows()
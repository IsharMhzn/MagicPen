import cv2 as cv
import numpy as np

pen = (0, 113, 0, 120, 255, 158), (0, 255, 0)

capture = cv.VideoCapture(0)
capture.set(10, 150)

canvas = []

while True:
    success, frame = capture.read()

    mask = cv.inRange(frame, pen[0][:3], pen[0][3:])
    contours, heirarchy = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    for c in contours:
        area = cv.contourArea(c)
        if int(area) in range(200, 500):
            x, y, w, h = cv.boundingRect(c)
            cv.circle(frame, (x+w//2, y), 5, pen[1])
            cv.rectangle(frame, (x, y), (x+w, y+h), pen[1], 2)
            canvas.append((x+w//2, y))
    
    for c in canvas:
        cv.circle(frame, c, 3, pen[1], -1)

    cv.imshow('Camera', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

    
capture.release()
cv.destroyAllWindows()
quit()
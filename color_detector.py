import cv2 as cv
import numpy as np


def hsv_tracker():
    cv.namedWindow('HSV Tracker')
    cv.resizeWindow('HSV Tracker', 600, 400)

    cv.createTrackbar('Hue Min', 'HSV Tracker', 0, 179, lambda a: None)
    cv.createTrackbar('Hue Max', 'HSV Tracker', 179, 179, lambda a: None)
    cv.createTrackbar('Sat Min', 'HSV Tracker', 0, 255, lambda a: None)
    cv.createTrackbar('Sat Max', 'HSV Tracker', 255, 255, lambda a: None)
    cv.createTrackbar('Val Min', 'HSV Tracker', 0, 255, lambda a: None)
    cv.createTrackbar('Val Max', 'HSV Tracker', 255, 255, lambda a: None)


def gethsvrange():
    hue_min = cv.getTrackbarPos('Hue Min', 'HSV Tracker')
    hue_max = cv.getTrackbarPos('Hue Max', 'HSV Tracker')
    sat_min = cv.getTrackbarPos('Sat Min', 'HSV Tracker')
    sat_max = cv.getTrackbarPos('Sat Max', 'HSV Tracker')
    val_min = cv.getTrackbarPos('Val Min', 'HSV Tracker')
    val_max = cv.getTrackbarPos('Val Max', 'HSV Tracker')

    return (hue_min, sat_min, val_min), (hue_max, sat_max, val_max)


hsv_tracker()
video = cv.VideoCapture(0)

video.set(3, 1000)
video.set(4, 800)

while True:
    success, frame = video.read()

    lower, upper = gethsvrange()
    mask = cv.inRange(frame, lower, upper)

    mix = cv.bitwise_and(frame, frame, mask=mask)

    # cv.imshow('Camera', frame)
    cv.imshow('Mask', mask)
    # cv.imshow('HSV', mix)

    if cv.waitKey(20) & 0xFF==ord('q'):
        break

video.release()
cv.destroyAllWindows()
quit()
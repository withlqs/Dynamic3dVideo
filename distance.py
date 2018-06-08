#!/usr/bin/env python3

import queue
import threading
import time

import cv2
import numpy as np

x_data = [100,83,71,63,56,50,42,33,25,24,22,20]
y_data = [0,-0.5,-1,-1.5,-2,-2.5,-3.5,-5,-7.5,-8,-9,-10]

poly = np.polyfit(x_data, y_data, deg=6)
poly_func = np.poly1d(poly)

cam = cv2.VideoCapture(0)
cam.set(3, int(640 * 1.5))  # width
cam.set(4, int(480 * 1.5))  # height

mouth_detector = cv2.CascadeClassifier('xml/haarcascade_mcs_mouth.xml')
nose_detector = cv2.CascadeClassifier('xml/haarcascade_mcs_nose.xml')

q = queue.Queue()


def show_img_from_queue():
    img = q.get()
    show(img)


def show(img):
    cv2.imshow('Distance', img)
    cv2.waitKey(1)


measure_time = 0
last_pixel_dis = 0
first_pixel_dis = 0

standard = 5

last_offset = int(poly_func(100 - standard) * -169.45)
first_offset = last_offset


def measure():
    global q
    global measure_time
    global last_pixel_dis
    global first_pixel_dis

    global last_offset

    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    mouth = mouth_detector.detectMultiScale(gray, 1.3, 32)
    nose = nose_detector.detectMultiScale(gray, 1.3, 12)

    x1 = 0
    y1 = 0

    x2 = 0
    y2 = 0

    min_d = img.shape[0] ** 2 + img.shape[1] ** 2
    dest_mouth = []
    dest_nose = []

    for (x, y, w, h) in mouth:
        # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        x1 = x + w / 2
        y1 = y + h / 2
        for (xx, yy, ww, hh) in nose:
            # cv2.rectangle(img, (xx, yy), (xx + ww, yy + hh), (0, 255, 0), 2)
            x2 = xx + ww / 2
            y2 = yy + hh / 2
            if (x1 - x2) ** 2 + (y1 - y2) ** 2 < min_d:
                dest_mouth = (x, y, w, h)
                dest_nose = (xx, yy, ww, hh)

    if len(dest_mouth) != 0:
        cv2.rectangle(img, (dest_mouth[0], dest_mouth[1]),
                      (dest_mouth[0] + dest_mouth[2], dest_mouth[1] + dest_mouth[3]), (255, 0, 0), 2)
        cv2.rectangle(img, (dest_nose[0], dest_nose[1]), (dest_nose[0] + dest_nose[2], dest_nose[1] + dest_nose[3]),
                      (0, 255, 0), 2)
        x1 = dest_mouth[0] + dest_mouth[2] / 2
        y1 = dest_mouth[1] + dest_mouth[3] / 2
        x2 = dest_nose[0] + dest_nose[2] / 2
        y2 = dest_nose[1] + dest_nose[3] / 2

    q.put(img)

    if len(dest_mouth) == 0:
        return last_offset

    pixel_dis = int(((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5)

    if measure_time == 1:
        first_pixel_dis = pixel_dis

    if measure_time > 1:
        # last_offset = int(
        #     -169.45 *
        #     poly_func(100-standard * 100 / (100 * pixel_dis / first_pixel_dis))
        # )
        last_offset = int(
            first_offset * first_pixel_dis / pixel_dis
        )

    print(last_offset)
    measure_time += 1
    return last_offset


show_img_thread = threading.Thread(target=show_img_from_queue)


if __name__ == '__main__':
    while True:
        measure()
        show_img_from_queue()
        time.sleep(1)

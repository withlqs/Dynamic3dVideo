import threading
from multiprocessing import Process, Queue, Value

import cv2

import distance as detection


def stylize(img, offset):
    splits = cv2.split(img)
    width = img.shape[1]

    if offset >= 0:
        B = splits[0][0:, offset:width]
        G = splits[1][0:, offset:width]
        R = splits[2][0:, 0:width - offset]
        BGR = cv2.merge([B, G, R])
    else:
        B = splits[0][0:, 0:width + offset]
        G = splits[1][0:, 0:width + offset]
        R = splits[2][0:, -offset:width]
        BGR = cv2.merge([B, G, R])

    return BGR


def producer(rq, pq, distance):
    while True:
        try:
            fid, img = rq.get(timeout=5)
        except:
            print("producer hungry!")
            continue
        img = stylize(img, int(distance.value))
        pq.put((fid, img))


def getDistance(distance):
    while True:
        dis = detection.measure() - 25
        # dis = 100
        print(dis)
        distance.value = dis
        detection.show_img_from_queue()
        detection.time.sleep(0.2)


class Producer():
    def __init__(self, thread_num, queue_enum_num):
        self.thread_num = thread_num
        self.queue_enum_num = queue_enum_num
        self.distance = Value('d', 0.0)

        self.dis_thread = threading.Thread(target=getDistance, args=(self.distance,))
        self.dis_thread.setDaemon(True)

        self.raw_queue = list()
        self.product_queue = list()
        self.producer_thread = list()

        for i in range(thread_num):
            rq = Queue(maxsize=queue_enum_num)
            pq = Queue(maxsize=queue_enum_num)
            self.raw_queue.append(rq)
            self.product_queue.append(pq)
            t = Process(target=producer, args=(rq, pq, self.distance,))
            t.daemon = True
            self.producer_thread.append(t)

    def getQueue(self):
        return self.raw_queue, self.product_queue

    def start(self):
        self.dis_thread.start()
        for t in self.producer_thread:
            t.start()


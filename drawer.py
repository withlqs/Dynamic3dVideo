from multiprocessing import Process
import time
import cv2
import utils

class Consumer:
    def __init__(self, video_path, thread_num, product_queue):
        self.thread_num = thread_num
        self.product_queue = product_queue
        self.delay = utils.getDelay(video_path)
        self.consumer_thread = Process(target=self.consumer, args=(thread_num, product_queue,))
        self.consumer_thread.daemon = True

    def start(self):
        self.consumer_thread.start()

    def consumer(self, thread_num, product_queue):
        cv2.namedWindow("capture")
        i = 0
        start_time = time.time() * 1000
        should_time = start_time
        while True:
            fid, img = product_queue[i].get()
            cv2.imshow('capture', img)
            i = (i + 1) % thread_num
            should_time = should_time + self.delay
            cur_time = time.time() * 1000
            wait_time = int(should_time - cur_time)
            print("wait " + str(wait_time))
            if wait_time <= 0:
                wait_time = 1

            if cv2.waitKey(wait_time) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

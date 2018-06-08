import cv2

import audio
import drawer
import stylize

thread_num = 4
queue_enum_num = 8
video_path = "demo.mp4"

if __name__ == "__main__":
    cap = cv2.VideoCapture(video_path)

    player = audio.Audio(video_path)
    producer = stylize.Producer(thread_num, queue_enum_num)
    raw_queue, product_queue = producer.getQueue()
    consumer = drawer.Consumer(video_path, thread_num, product_queue)

    producer.start()
    consumer.start()
    player.start()

    fid = 0
    while True:
        # get a frame
        ret, frame = cap.read()
        raw_queue[fid % thread_num].put((fid, frame))
        print("Fid: " + str(fid) + " Queue: " + str(fid % thread_num) + " size " + str(
            raw_queue[fid % thread_num].qsize()))
        fid = fid + 1

    # cap.release()

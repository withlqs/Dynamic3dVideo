import subprocess
import cv2

def getFrameNum(video_path):
    cap = cv2.VideoCapture(video_path)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return length
    # cmd = "ffmpeg -i " + video_path + " -vcodec copy -f rawvideo -y /dev/null 2>&1 | tr ^M '\n' | grep 'frame'"
    # p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # val = p.stdout.readline().decode("utf-8")
    # print(val)
    # val = ' '.join(val.split())
    # val = val.split(" ")
    # if val[0] == "frame=":
    #     print(val[1])
    #     return int(val[1])
    # else:
    #     print(val[0].split("=")[1])
    #     return int(val[0].split("=")[1])


def getDuration(video_path):
    # get cmd output
    cmd = "ffmpeg -i " + video_path
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    outs = p.stdout.readlines()

    # get duration str
    tar = None
    for out in outs:
        # out = str(out)
        out = out.decode("gbk")
        if "Duration" in out:
            tar = out
            break
    if tar is None:
        raise IOError("Please install FFmpeg first!")

    start_pos = tar.find("Duration:") + len("Duration:")
    end_pos = tar.find(",")
    if start_pos == -1 or end_pos == -1:
        raise ValueError("error when calculate video duration")

    tar = tar[start_pos: end_pos].strip().split(':')
    return int(tar[0]) * 3600000 + int(tar[1]) * 60000 + int(float(tar[2]) * 1000)

def getDelay(video_path):
    frame = getFrameNum(video_path)
    dur = getDuration(video_path)
    return dur / frame
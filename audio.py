import os
import wave
from multiprocessing import Process

import pyaudio

class Audio:
    def __init__(self, video_path):
        audio_path = os.path.splitext(video_path)[0] + ".wav"
        if not os.path.exists(audio_path):
            os.system("ffmpeg -i " + video_path + " -b:a 128k " + audio_path)

        self.audio_thread = Process(target=self.playAudioThread, args=(audio_path,))
        self.audio_thread.daemon = True

    def playAudioThread(self, audio_path):
        chunk = 1024
        wf = wave.open(audio_path, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        while True:
            audio_data = wf.readframes(chunk)
            if audio_data == "": break;
            stream.write(audio_data)

    def start(self):
        self.audio_thread.start()


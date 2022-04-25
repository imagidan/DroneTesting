from threading import Thread
import jetson.utils as utils

class WebcamVideoStreamCuda:
    def __init__(self, src=0):
        self.stream = utils.videoSource('/dev/video0')

        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self
    
    def update(self):
        while True:
            if self.stopped:
                return
            
            self.frame = self.stream.Capture()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
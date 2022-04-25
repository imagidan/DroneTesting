from webcam_video_stream import WebcamVideoStream
from fps import FPS
from my_inference_functions import *
import jetson.utils as utils
import imutils
import cv2

vs = WebcamVideoStream(src=0).start()
fps = FPS().start()
net = getNet("../models/license_plate_v5", 0.5)

while fps._numFrames < 100:
    frame = vs.read()
    frame = utils.cudaFromNumpy(frame)
    detections = net.Detect(frame)
    errorX = detections[0].Center[0] - 640
    fps.update()

    #if cv2.waitKey(1) & 0xFF == ord('q'):
        #break

fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
vs.stop()
#import cv2
import jetson.inference
import jetson.utils
from math import floor, ceil

net = jetson.inference.detectNet(argv=['--model=../models/license_plate_v5/ssd-mobilenet.onnx', '--labels=../models/license_plate_v5/labels.txt', '--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes', '--overlay=none'], threshold = 0.5)
cam = jetson.utils.videoSource("/dev/video0")
display = jetson.utils.glDisplay()

while True:
    #try:
        img = cam.Capture()
        detections = net.Detect(img)
        display.Render(img)
        display.SetTitle("License Plate Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

        if len(detections) == 1:
            detection = detections[0]
            xError = detection.Center[0] - 640
            yError = detection.Center[1] - 360

    #except Exception as e:
        #print(e)

    #if cv2.waitKey(1) == ord('q'):
        #break

#cam.release()
#cv2.destroyAllWindows()
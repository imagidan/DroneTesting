import jetson.inference
import jetson.utils
from math import floor, ceil
import cv2

dispW = 1280
dispH = 720
flip = 2
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

cam = cv2.VideoCapture(camSet)
net = jetson.inference.detectNet(argv=['--model=../models/license_plate_v5/ssd-mobilenet.onnx', '--labels=../models/license_plate_v5/labels.txt', '--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes', '--overlay=none'], threshold = 0.5)

while True:
    try:
        ret, frame = cam.read()
        print(frame)
        img = jetson.utils.cudaFromNumpy(frame)
        detections = net.Detect(img)
        img = jetson.utils.cudaToNumpy(img)
        cv2.imshow("License Plate Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()), img)

        if len(detections) == 1:
            detection = detections[0]
            xError = detection.Center[0] - 640
            yError = detection.Center[1] - 360

    except Exception as e:
        print(e)

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
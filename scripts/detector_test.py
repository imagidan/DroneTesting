from detector import Detector
from reader import Reader
import cv2

licensePlateDetector = Detector("../models/license_plate_v5", 0.26)
reader = Reader()
cap = cv2.VideoCapture(0)
avg = 0
count = 0

while True:
    ret, img = cap.read()
    detections, detectionsImg = licensePlateDetector.detect(img)
    if len(detections) == 1:
        cropImg = licensePlateDetector.cropDetection(img, detections[0])
        resizedImg = licensePlateDetector.resizeImg(cropImg)
        plateNumber = reader.read(resizedImg)
        print(plateNumber)
        cv2.imshow("Frame", resizedImg)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
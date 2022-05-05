from detector import Detector
from reader import Reader
import cv2

licensePlateDetector = Detector("../models/license_plate_v5", 0.26)
reader = Reader()
cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()

    detections, detectionsImg = licensePlateDetector.detect(img)

    if len(detections) == 1:

        detection = detections[0]

        if detection.Confidence > 0.9:
            
            licensePlate = licensePlateDetector.getReaderInputImg(img, detection)
            plateNumber = reader.read(licensePlate)
            print(plateNumber)

    cv2.imshow("Frame", detectionsImg)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
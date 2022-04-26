from detector import Detector
import cv2

licensePlateDetector = Detector("../models/license_plate_v5")
cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    detections, detectionsImg = licensePlateDetector.detect(img)
    print(detections[0].Width)

    cv2.imshow("Frame", detectionsImg)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
from detector import Detector
from reader import Reader
from danbus import DanBus
from gamepad import Gamepad
from db import DroneDB
import cv2
import time

detector = Detector("../models/license_plate_v5", 0.26)
reader = Reader()
danbus = DanBus()
gamepad = Gamepad(danbus, "saved_constants.txt")
dronedb = DroneDB()

cap = cv2.VideoCapture(0)
errorI = 0
verticalAngle = 0
lastVerticalAngle = 0
pastTime = time.time()

while True:
    _, img = cap.read()
    
    detections, detectionsImg = detector.detect(img)

    if len(detections) == 1:

        detection = detections[0]

        if detection.Confidence > 0.98 or (detection.Center[0] < 200 and detection.Center[0] > 1000):

            licensePlate = detector.getReaderInputImg(img, detection)
            plateNumber = reader.read(licensePlate)
            print(plateNumber)

            lastVerticalAngle = verticalAngle
            verticalAngle = detector.getVerticalAngle(detection)
            horizontalAngle = detector.getHorizontalAngle(detection)
            distance = detector.getDistance(detection)

            if len(plateNumber) == 6:
                if dronedb.check_plate(plateNumber) == []:
                    dronedb.add_plate(plateNumber, horizontalAngle, verticalAngle, distance, 1)
                    dronedb.commit()
                else:
                    dronedb.update_plate(plateNumber, "horizontalAngle", horizontalAngle)
                    dronedb.update_plate(plateNumber, "verticalAngle", verticalAngle)
                    dronedb.update_plate(plateNumber, "distance", distance)
                    dronedb.update_plate(plateNumber, "isVisible", 1)
                    dronedb.commit()
            else:
                dronedb.update_plates("isVisible", 0)
                dronedb.commit()

            if gamepad.zMode == 1:
                danbus.setZ(horizontalAngle)

            if gamepad.tMode == 1:
                
                if gamepad.throttle < 1300:
                    gamepad.throttle, pastTime = detector.smooth(gamepad.throttle, pastTime, 0.1, 20, gamepad.minThrottle, gamepad.maxThrottle)
                    danbus.setT(gamepad.throttle)
                else:
                    gamepad.throttle, errorI = detector.trackPlateHeightAngle(gamepad.constants[9], gamepad.constants[2], gamepad.constants[5], gamepad.constants[8], verticalAngle, lastVerticalAngle, gamepad.minThrottle, gamepad.maxThrottle, errorI)
                    danbus.setT(gamepad.throttle)
        
        else:

            if gamepad.zMode == 1:
                danbus.setZ(0)

            if gamepad.tMode == 1:
                gamepad.throttle, pastTime = detector.smooth(gamepad.throttle, pastTime, 0.1, -20, gamepad.minThrottle, gamepad.maxThrottle)
                danbus.setT(gamepad.throttle)

    cv2.imshow("Frame", detectionsImg)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
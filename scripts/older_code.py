import cv2
import jetson.utils as utils
from scripts.cuda_engine_functions import *
#from hc_12_functions import *
from my_inference_functions import *
from scripts.serial import *
import configurator
from dbInteract import *

horizontalAngle = 0
verticalAngle = 0
distance = 0
cur, conn = start_conn()

#serial_port = getSerial()
labels, context, buffers = getEngineLabelsContextBuffers("../lpr/us_lp_characters.txt", "../lpr/lpr_us_onnx_b16.engine")
net = getNet("../models/license_plate_v5", 0.5)
cap = cv2.VideoCapture(0)
isOn = True
screenW = 1280
screenH = 720
once = True
sum_error = 0
startT = 0
pErrorX = 0
yawSpeed = 0
interval = 0.1
halfFOV = 37
loopPrevT = time.time()

#app = configurator.App(serial_port)
#yawKp, yawKi, yawKd, yawS = app.ReturnVals()

time.sleep(3)

while(True):

    #msg = getMsg(serial_port)
    #print(msg)
    #if msg == "go/stop":
    #    print("go/stop")
    #    if isOn == True:
    #        isOn = False
    #    else:
    #        isOn = True
    #elif msg == "license":
    #    print("license")

    if isOn == True:
        ret, rgb = cap.read()

        cuda_rgb = utils.cudaFromNumpy(rgb)
        cuda_rgb_intact = utils.cudaFromNumpy(rgb)
        detections = net.Detect(cuda_rgb)
        rgb_with_detections = utils.cudaToNumpy(cuda_rgb)
        #resized_rgb_with_detections = cv2.resize(rgb_with_detections, (800, 450))
        
        if len(detections) == 1 and detections[0].Confidence > 0.9:
            if once == True:
                once = False
                startT = time.time()
            detection = detections[0]
            #yawSpeed, pErrorX, sum_error, startT = trackPlateAngle(screenW, detection.Center[0], yawKp, yawKi, yawKd, pErrorX, sum_error, startT)
            #print(yawSpeed)
            cropped_license_plate = getCroppedLicensePlate(cuda_rgb_intact, detection)
            inputs, outputs, bindings, stream = buffers
            outputs = getOutputs(inputs, outputs, bindings, stream, context, (1,3,48,96), cropped_license_plate)
            #print(outputs)
            license_plate_chars = outputsToLicenseNumber(outputs, labels)
            #print(license_plate_chars + "\n")
            horizontalAngle = (detection.Center[0] - screenW/2)/(screenW/2)*halfFOV
            verticalAngle = (detection.Center[1] - screenH/2)/(screenH/2)*halfFOV
            distance = 1/detection.Width

            print(str(horizontalAngle) + "\t" + str(verticalAngle) + "\t" + str(distance) + "\n")
            if len(license_plate_chars) == 6:
                #sendMsg(serial_port, license_plate_chars[0:3] + " " + license_plate_chars[3:6] + "\n")
                print(license_plate_chars + "\n")
                if check_plate(cur, license_plate_chars) == []:
                    add_plate(cur, license_plate_chars, horizontalAngle, verticalAngle, distance, 1)
                    commit(conn)
                else:
                    update_plate(cur, license_plate_chars, "horizontalAngle", horizontalAngle)
                    update_plate(cur, license_plate_chars, "verticalAngle", verticalAngle)
                    update_plate(cur, license_plate_chars, "distance", distance)
                    update_plate(cur, license_plate_chars, "isVisible", 1)
                    commit(conn)
            else:
                update_plates(cur, "isVisible", 0)
                commit(conn)
                #print(net.GetNetworkFPS())
        else:
            once = True
            sum_error = 0
        if time.time() - loopPrevT >= interval:
            loopPrevT = time.time()
            #sendMsg(serial_port, "t," + str(0-yawSpeed) + "\n")
            #app.sendImage(resized_rgb_with_detections)
            #app.getVals()
            #yawKp, yawKi, yawKd, yawS = app.ReturnVals()
        cv2.imshow("Frame", rgb_with_detections)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
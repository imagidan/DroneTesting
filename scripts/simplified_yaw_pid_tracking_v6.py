import cv2
import jetson.utils as utils
from cuda_functions import *
from my_inference_functions import *
from scripts.serialConnection import *
from gamepad_go import *

danbus = DanBus()
relay = Gamepad_Relay(danbus)
relay.start()
labels, context, buffers = getEngineLabelsContextBuffers("../lpr/us_lp_characters.txt", "../lpr/lpr_us_onnx_b16.engine")

def threaded(labels, context, buffers):

    horizontalAngle = 0
    lastVerticalAngle = 0
    pastTime = time.time()
    b = 1300
    verticalAngle = 0
    net = getNet("../models/license_plate_v5", 0.5)
    cap = cv2.VideoCapture(0)
    isOn = True
    screenW = 1280
    screenH = 720
    halfFOV = 37
    errorI = 0

    time.sleep(3)

    while(True):
        if isOn == True:
            ret, rgb = cap.read()

            cuda_rgb = utils.cudaFromNumpy(rgb)
            cuda_rgb_intact = utils.cudaFromNumpy(rgb)
            detections = net.Detect(cuda_rgb)
            rgb_with_detections = utils.cudaToNumpy(cuda_rgb)
            
            if len(detections) == 1:
                detection = detections[0]
                #print(detection.Center[0])
                if detection.Confidence > 0.98:
                    cropped_license_plate = getCroppedLicensePlate(cuda_rgb_intact, detection)
                    inputs, outputs, bindings, stream = buffers
                    outputs = getOutputs(inputs, outputs, bindings, stream, context, (1,3,48,96), cropped_license_plate)
                    license_plate_chars = outputsToLicenseNumber(outputs, labels)
                    horizontalAngle = (detection.Center[0] - screenW/2)/(screenW/2)*halfFOV
                    lastVerticalAngle = verticalAngle
                    verticalAngle = (screenH/2-detection.Center[1])/(screenH/2)*halfFOV
                    print(verticalAngle)
                    if relay.altMode == True:
                        if relay.throttle < b:
                            relay.throttle, pastTime = smooth(relay.throttle, pastTime, 0.1, 20, relay.minThrottle, relay.maxThrottle)
                        else:
                            relay.throttle, errorI = trackPlateHeightAngle(relay.hover, relay.tp, relay.ti, relay.td, verticalAngle, lastVerticalAngle, relay.minThrottle, relay.maxThrottle, errorI)
                        print(relay.throttle)
                        danbus.throttle(relay.throttle)
                    if relay.stabilize_yaw == True:
                        danbus.yaw(horizontalAngle)
                elif detection.Center[0] < 200 or detection.Center[0] > 1000:
                    horizontalAngle = (detection.Center[0] - screenW/2)/(screenW/2)*halfFOV
                    lastVerticalAngle = verticalAngle
                    verticalAngle = (screenH/2-detection.Center[1])/(screenH/2)*halfFOV
                    if relay.altMode == True:
                        if relay.throttle < b:
                            relay.throttle, pastTime = smooth(relay.throttle, pastTime, 0.1, 20, relay.minThrottle, relay.maxThrottle)
                        else:
                            relay.throttle, errorI = trackPlateHeightAngle(relay.hover, relay.tp, relay.ti, relay.td, verticalAngle, lastVerticalAngle, relay.minThrottle, relay.maxThrottle, errorI)
                        print(relay.throttle)
                        danbus.throttle(relay.throttle)
                    if relay.stabilize_yaw == True:
                        danbus.yaw(horizontalAngle)
                        #print(str(horizontalAngle) + "\n")
                else:
                    if relay.altMode == True:
                        if relay.throttle > b:
                            relay.throttle, pastTime = smooth(relay.throttle, pastTime, 0.1, -20, relay.minThrottle, relay.maxThrottle)
                        else:
                            relay.throttle = 1000
                        danbus.throttle(relay.throttle)
            else:
                if relay.altMode == True:
                    if relay.throttle > b:
                        relay.throttle, pastTime = smooth(relay.throttle, pastTime, 0.1, -20, relay.minThrottle, relay.maxThrottle)
                    else:
                        relay.throttle = 1000
                    danbus.throttle(relay.throttle)

            cv2.imshow("Frame", rgb_with_detections)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

threading.Thread(target=threaded, args=(labels, context, buffers)).start()
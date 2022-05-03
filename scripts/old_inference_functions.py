import jetson.inference as inference
import jetson.utils as utils
from math import ceil, floor
import cv2
import numpy as np
from scripts.cuda_engine_functions import *
import time

def getNet(model_dir, threshold=0.5):
    return inference.detectNet(argv=["--model=" + model_dir + "/ssd-mobilenet.onnx", "--labels=" + model_dir + "/labels.txt", '--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes', '--overlay=none'], threshold = threshold)

def getCroppedLicensePlate(original_cuda_img, detection):
    crop_roi = (floor(detection.Left), floor(detection.Top), ceil(detection.Right), ceil(detection.Bottom))
    cuda_license_plate = utils.cudaAllocMapped(width=crop_roi[2] - crop_roi[0], height=crop_roi[3] - crop_roi[1], format=original_cuda_img.format)
    utils.cudaCrop(original_cuda_img, cuda_license_plate, crop_roi)
    license_plate = utils.cudaToNumpy(cuda_license_plate)
    cropped_license_plate = cv2.resize(license_plate, (96, 48))
    cropped_license_plate = np.transpose(cropped_license_plate, (2,0,1)).astype(np.float32)
    cropped_license_plate = np.expand_dims(cropped_license_plate, axis=0)
    cropped_license_plate /= 255.0
    cropped_license_plate = np.ascontiguousarray(cropped_license_plate)

    return cropped_license_plate

def outputsToLicenseNumber(outputs, labels):
    filtered_outputs = list(filter(lambda a: a != 35, outputs[0]))
    license_plate_chars = ""
    for ind in filtered_outputs:
        license_plate_chars += labels[ind]
    
    return license_plate_chars

def getOutputs(inputs, outputs, bindings, stream, context, input_shape, cropped_license_plate):
    
    inputs[0].host = cropped_license_plate
    input_shape = (1, 3, 48, 96)
    context.set_binding_shape(0, input_shape)
    outputs = do_inference(context, bindings=bindings, inputs=inputs, outputs=outputs, stream=stream)
    
    return outputs

def trackPlateAngle(w, detectionX, kp, ki, kd, pErrorX, sum_error, startT):
    centerX = w/2
    errorX = detectionX - centerX
    nowT = time.time()
    deltaT = nowT - startT
    startT = nowT
    sum_error += errorX * deltaT
    yawSpeed = kp*errorX+kd*(errorX-pErrorX)+ki*sum_error
    yawSpeed = np.clip(yawSpeed, -400, 400)
    pErrorX = errorX

    return yawSpeed, pErrorX, sum_error, startT

def trackPlateHeightAngle(hover, kp, ki, kd, center, lastCenter, minThrottle, maxThrottle, errorI):
    myI = errorI + ki * center
    myI = np.clip(myI, minThrottle - hover, maxThrottle - hover)
    inputD = center - lastCenter
    yawPID = kp * center + errorI - kd * inputD
    throttle = np.clip(hover + yawPID, minThrottle, maxThrottle)
    return throttle, myI

def smooth(throttle, pastTime, interval, up, minThrottle, maxThrottle):
    if time.time() - pastTime >= interval:
        pastTime = time.time()
        speed = np.clip(throttle + up, minThrottle, maxThrottle)
        return speed, pastTime
    else:
        return throttle, pastTime
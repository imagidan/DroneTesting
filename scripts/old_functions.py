import jetson.inference as inference
import jetson.utils as utils
from math import ceil, floor
import cv2
import numpy as np
from cuda_engine_functions import *
import time

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
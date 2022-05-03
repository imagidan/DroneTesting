import jetson.inference as inference
import jetson.utils as utils
import cv2
import numpy as np
from math import ceil, floor

class Detector:

    def __init__(self, net_dir, objectWidth, threshold=0.5, imgW=1280, imgH=720, FOV=75, FL=954):
        self.net = inference.detectNet(argv=["--model=" + net_dir + "/ssd-mobilenet.onnx", "--labels=" + net_dir + "/labels.txt", '--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes', '--overlay=none'], threshold = threshold)
        self.imgW = imgW
        self.imgH = imgH
        self.FOV = FOV
        self.distConst=FL*objectWidth

    def detect(self, img):
        cudaImg = utils.cudaFromNumpy(img)
        detections = self.net.Detect(cudaImg)
        #TODO threshold map
        detectionsImg = utils.cudaToNumpy(cudaImg)
        return detections, detectionsImg
    
    def cropDetection(self, img, detection):
        return img[floor(detection.Top):floor(detection.Top)+ceil(detection.Height), floor(detection.Left):floor(detection.Left)+ceil(detection.Width)]
    
    def resizeImg(self, img, width=96, height=48):
        return cv2.resize(img, (width, height))
    
    def getHorizontalAngle(self, detection):
        return (detection.Center[0] - self.imgW/2)/(self.imgW/2)*(self.FOV/2)
    
    def getVerticalAngle(self, detection):
        return (detection.Center[1] - self.imgH/2)/(self.imgH/2)*(self.FOV*(self.imgH/self.imgW)/2)

    def getDistance(self, detection):
        return self.distConst / detection.Width
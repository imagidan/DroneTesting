import jetson.inference as inference
import jetson.utils as utils

class Detector:

    def __init__(self, net_dir, threshold=0.5, imgW=1280, imgH=720, FOV=75):
        self.net = inference.detectNet(argv=["--model=" + net_dir + "/ssd-mobilenet.onnx", "--labels=" + net_dir + "/labels.txt", '--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes', '--overlay=none'], threshold = threshold)
        self.imgW = imgW
        self.imgH = imgH
        self.FOV = FOV

    def detect(self, img):
        cudaImg = utils.cudaFromNumpy(img)
        detections = self.net.Detect(cudaImg)
        #TODO threshold map
        detectionsImg = utils.cudaToNumpy(cudaImg)
        return detections, detectionsImg
    
    def getHorizontalAngle(self, detection):
        return (detection.Center[0] - self.imgW/2)/(self.imgW/2)*(self.FOV/2)
    
    def getVerticalAngle(self, detection):
        return (detection.Center[1] - self.imgH/2)/(self.imgH/2)*(self.FOV*(self.imgH/self.imgW)/2)

    def getDistance(self, detection):
        return self.objectWidth * self.focalLength / detection.Width
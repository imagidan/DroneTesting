import serial
import time
import subprocess
from serial import Serial

class HC_12(Serial):

    def __init__(self):
        self.serial_port = self.selectPort

    def checkBoardType(self):
        out = subprocess.Popen(['cat', '/sys/module/tegra_fuse/parameters/tegra_chip_id'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, _ = out.communicate()
        chip_id = int(stdout.decode("utf-8"))

        if chip_id == 25:
            return "Xavier"
        elif chip_id == 33:
            return "Nano"
        else:
            return "Unknown"

    def selectPort(self):
        jetsonType = self.checkBoardType()
        
        if jetsonType == "Xavier":
            return "/dev/ttyTHS0"
        elif jetsonType == "Nano":
            return "/dev/ttyTHS1"
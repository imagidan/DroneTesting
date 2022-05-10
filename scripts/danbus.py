import threading
import time
from serialConnection import SerialConnection

class DanBus:

    def __init__(self):
        self.serialConn = SerialConnection()
        self.reset()

    def start(self):
        threading.Thread(target=self.run, args=()).start()
        return self

    def reset(self):
        self.kpa_z = ""
        self.kps_z = ""
        self.kia_z = ""
        self.kis_z = ""
        self.kda_z = ""
        self.kds_z = ""
        self.t = ""
        self.z = ""
        self.z_mode = ""
        self.c = ""
        self.g = ""
        self.s = ""

    def setKpaZ(self, num):
        self.kpa_z = "q," + str(num) + ","
        
    def setKpsZ(self, num):
        self.kps_z = "p," + str(num) + ","

    def setKiaZ(self, num):
        self.kia_z = "j," + str(num) + ","
        
    def setKisZ(self, num):
        self.kis_z = "i," + str(num) + ","

    def setKdaZ(self, num):
        self.kda_z = "b," + str(num) + ","
        
    def setKdsZ(self, num):
        self.kds_z = "d," + str(num) + ","

    def setT(self, num):
        self.t = "t," + str(num) + ","
    
    def setZ(self, num):
        self.z = "z," + str(num) + ","

    def setZMode(self, num):
        self.z_mode = "m," + str(num) + ","

    def setConfig(self):
        self.c = "c,"

    def setGo(self):
        self.g = "g,"

    def setStop(self):
        self.s = "s,"

    def send(self):
        self.msg = self.kpa_z + self.kps_z + self.kia_z + self.kis_z + self.kda_z + self.kds_z + self.z + self.z_mode + self.c + self.g + self.s
        self.serialConn.sendMsg(self.msg)
        self.reset()

    def run(self):
        while 1:
            self.send()
            time.sleep(0.04)
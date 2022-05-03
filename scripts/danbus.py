import threading
from scripts.serial import *

class DanBus:

    def __init__(self):
        self.serial_port = getSerial()
        self.once = True
        self.reset()

    def start(self):
        threading.Thread(target=self.run, args=()).start()
        return self

    def reset(self):
        self.w = ""
        self.c = ""
        self.g = ""
        self.s = ""
        self.m = ""
        self.p = ""
        self.q = ""
        self.i = ""
        self.j = ""
        self.d = ""
        self.b = ""
        self.t = ""
        self.y = ""
        self.pi = ""
        self.r = ""
        self.z = ""

    def setStabilize(self, num):
        self.w = "w," + str(num) + ","

    def config(self):
        self.c = "h,"

    def go(self):
        self.g = "g,"

    def stop(self):
        self.s = "s,"

    def setP(self, num):
        self.p = "p,{:2f}".format(num) + ","

    def setQ(self, num):
        self.q = "q,{:2f}".format(num) + ","

    def setI(self, num):
        self.i = "i,{:3f}".format(num) + ","

    def setJ(self, num):
        self.j = "j,{:3f}".format(num) + ","

    def setD(self, num):
        self.d = "d,{:2f}".format(num) + ","

    def setB(self, num):
        self.b = "b,{:2f}".format(num) + ","
    
    def throttle(self, num):
        self.t = "t,{:1f}".format(num) + ","
    
    def yaw(self, num):
        self.y = "y,{:1f}".format(num) + ","
    
    def pitch(self, num):
        self.pi = "f,{:1f}".format(num) + ","
    
    def roll(self, num):
        self.r = "r,{:1f}".format(num) + ","
    
    def setYawBias(self, num):
        self.z = "z,{:3f}".format(num) + ","

    def send(self):
        self.msg = self.w + self.c + self.g + self.s + self.m + self.p + self.q + self.i + self.j + self.d + self.b + self.t + self.y + self.pi + self.r
        sendMsg(self.serial_port, self.msg)
        self.reset()

    def run(self):
        while 1:
            #if getMsg(self.serial_port) == "a":
            self.send()
            time.sleep(0.04)
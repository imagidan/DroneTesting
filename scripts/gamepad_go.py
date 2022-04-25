from inputs import get_gamepad
from danbus import DanBus
import threading
import numpy as np

"""
    ev_types:   Sync, Absolute
    codes:      ABS_Z = Right Joystick Left/Right (0-255)
                ABS_RZ = Right Joystick Up/Down (0-255)
                ABS_X = Left Joystick Left/Right (0-255)
                ABS_Y =  Left Joystick Up/Down (0-255)
                ABS_HAT0X = + pad Left/Right (-1,0,1)
                ABS_HAT0Y = + pad Up/Down (-1,0,1)
                BTN_TRIGGER = Button 1 (0,1)
                BTN_THUMB = Button 2 (0,1)
                BTN_THUMB2 = Button 3 (0,1)
                BTN_TOP = Button 4 (0,1)
                BTN_TOP2 = Button 5 (0,1)
                BTN_PINKIE = Button 6 (0,1)
                BTN_BASE = Button 7 (0,1)
                BTN_BASE2 = Button 8 (0,1)
                BTN_BASE3 = Button 9 (0,1)
                BTN_BASE4 = Button  10 (0,1)
                BTN_BASE5 = Button Left Joystick
                BTN_BASE6 = Button Right Joystick
"""

class Gamepad_Relay(threading.Thread):

    def __init__(self, danbus):
        self.danbus = danbus
        self.danbus.start()
        self.stabilize_yaw = False
        self.stabilize_pr = False
        self.altMode = False
        self.isRunning = False
        self.minJoystick = 0
        self.midJoystick = 128
        self.maxJoystick = 255
        self.minThrottle = 1000
        self.maxThrottle = 1600
        self.hover = 1000
        self.t_inc = 0.04
        self.dps_yaw = 150
        self.mode = 1
        self.yaw_bias = 1
        self.yaw_bias_min = 0.85
        self.yaw_bias_max = 2
        self.yaw_bias_inc = 0.00001
        self.q = 0
        self.p = 0
        self.tp = 0
        self.p_min = 0
        self.p_max = 10
        self.p_inc = 0.0001
        self.j = 0
        self.i = 0
        self.ti = 0
        self.i_min = 0
        self.i_max = 1
        self.i_inc = 0.00001
        self.b = 0
        self.d = 0
        self.td = 0
        self.d_min = 0
        self.d_max = 3
        self.d_inc = 0.0001
        self.throttle = 1000
        self.yaw = 0
        self.throttleDiff = self.maxThrottle - self.minThrottle

    def start(self):
        threading.Thread(target=self.run, args=()).start()
        return self

    def run(self):
        while 1:
            events = get_gamepad()
            for event in events:
                if event.code == "BTN_BASE" and event.state == 1 and self.isRunning == False:
                    self.danbus.config()
                    print("c")
                elif event.code == "BTN_BASE3" and event.state == 1 and self.isRunning == True:
                    self.danbus.setStabilize(1)
                    self.stabilize_yaw = True
                    #self.throttle = 1000
                    print("stabilize mode")
                elif event.code == "BTN_BASE4" and event.state == 1 and self.isRunning == True:
                    self.danbus.setStabilize(0)
                    self.stabilize_yaw = False
                    #self.throttle = 1000
                    print("acro mode")
                elif event.code == "BTN_TOP2" and event.state == 1 and self.isRunning == False:
                    self.danbus.go()
                    self.isRunning = True
                    print("g")
                elif event.code == "BTN_PINKIE" and event.state == 1 and self.isRunning == True:
                    self.isRunning = False
                    print("s")
                elif event.code == "ABS_RZ" and self.isRunning == True:
                    if self.stabilize_yaw == False and self.altMode == False:
                        if self.mode == 1:
                            self.q -= (event.state - self.midJoystick) * self.p_inc
                            self.q = np.clip(self.q, self.p_min, self.p_max)
                            self.danbus.setQ(self.q)
                            print("rate p " + str(self.q))
                        elif self.mode == 2:
                            self.j -= (event.state - self.midJoystick) * self.i_inc
                            self.j = np.clip(self.j, self.i_min, self.i_max)
                            self.danbus.setJ(self.j)
                            print("rate i " + str(self.j))
                        elif self.mode == 3:
                            self.b -= (event.state - self.midJoystick) * self.d_inc
                            self.b = np.clip(self.b, self.d_min, self.d_max)
                            self.danbus.setB(self.b)
                            print("rate d " + str(self.b))
                    elif self.stabilize_yaw == True and self.altMode == False:
                        if self.mode == 1:
                            self.p -= (event.state - self.midJoystick) * self.p_inc
                            self.p = np.clip(self.p, self.p_min, self.p_max)
                            self.danbus.setP(self.p)
                            print("stab p " + str(self.p))
                        elif self.mode == 2:
                            self.i -= (event.state - self.midJoystick) * self.i_inc
                            self.i = np.clip(self.i, self.i_min, self.i_max)
                            self.danbus.setI(self.i)
                            print("stab i " + str(self.i))
                        elif self.mode == 3:
                            self.d -= (event.state - self.midJoystick) * self.d_inc
                            self.d = np.clip(self.d, self.d_min, self.d_max)
                            self.danbus.setD(self.d)
                            print("stab d " + str(self.d))
                    elif self.altMode == True:
                        if self.mode == 1:
                            self.tp -= (event.state - self.midJoystick) * self.p_inc
                            self.tp = np.clip(self.tp, self.p_min, self.p_max)
                            print("altitude p " + str(self.tp))
                        elif self.mode == 2:
                            self.ti -= (event.state - self.midJoystick) * self.i_inc
                            self.ti = np.clip(self.ti, self.i_min, self.i_max)
                            print("altitude i " + str(self.ti))
                        elif self.mode == 3:
                            self.td -= (event.state - self.midJoystick) * self.d_inc
                            self.td = np.clip(self.td, self.d_min, self.d_max)
                            print("altitude d " + str(self.td))
                        elif self.mode == 4:
                            self.hover -= (event.state - self.midJoystick) * self.t_inc
                            self.hover = np.clip(self.hover, self.minThrottle, self.maxThrottle)
                            print("hover throttle " + str(self.hover))
                        
                elif event.code == "ABS_X" and self.isRunning == True and self.stabilize_yaw == False:
                    self.yaw = self.map_num(event.state, self.minJoystick, self.maxJoystick, -self.dps_yaw, self.dps_yaw)
                    self.danbus.yaw(self.yaw)
                    print("yaw " + str(self.yaw))
                elif event.code == "ABS_Y" and self.isRunning == True and self.altMode == False:
                    if event.state < self.midJoystick:
                        self.throttle = self.map_num(event.state, self.minJoystick, self.midJoystick, self.minThrottle, self.maxThrottle)
                        self.throttle = self.maxThrottle - (self.throttle - self.minThrottle)
                        self.danbus.throttle(self.throttle)
                        print("throttle " + str(self.throttle))
                elif event.code == "BTN_TRIGGER" and event.state == 1:
                    self.mode = 1
                    print("p mode")
                elif event.code == "BTN_THUMB" and event.state == 1:
                    self.mode = 2
                    print("i mode")
                elif event.code == "BTN_THUMB2" and event.state == 1:
                    self.mode = 3
                    print("d mode")
                elif event.code == "BTN_TOP" and event.state == 1:
                    self.mode = 4
                    self.altMode = not self.altMode
                    print("altitude mode" + str(self.altMode))

    def map_num(self, num, fromLow, fromHigh, toLow, toHigh):
        return (num - fromLow) * (toHigh - toLow) / (fromHigh - fromLow) + toLow
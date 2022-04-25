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
        self.isRunning = False
        self.minJoystick = 0
        self.midJoystick = 128
        self.maxJoystick = 255
        self.minThrottle = 1000
        self.maxThrottle = 1500
        self.dps = 30
        self.dps_yaw = 30
        self.yaw_mode = False
        self.mode = 1
        self.p = 0
        self.q = 0
        self.p_min = 0
        self.p_max = 3
        self.p_inc = 0.0001
        self.i = 0
        self.j = 0
        self.i_min = 0
        self.i_max = 1
        self.i_inc = 0.00001
        self.d = 0
        self.b = 0
        self.d_min = 0
        self.d_max = 3
        self.d_inc = 0.0001
        self.throttle = 1000
        self.yaw = 0
        self.pitch = 0
        self.roll = 0
        self.throttleDiff = self.maxThrottle - self.minThrottle

    def start(self):
        threading.Thread(target=self.run, args=()).start()
        return self

    def run(self):
        while 1:
            events = get_gamepad()
            for event in events:
                if self.isRunning == False:
                    if event.state == 1:
                        if event.code == "BTN_TRIGGER" and self.mode != 1:
                            self.mode = 1 
                            print("mode run")
                        elif event.code == "BTN_THUMB" and self.mode != 2:
                            self.mode = 2
                            print("mode p")
                        elif event.code == "BTN_THUMB2" and self.mode != 3:
                            self.mode = 3
                            print("mode i")
                        elif event.code == "BTN_TOP" and self.mode != 4:
                            self.mode = 4
                            print("mode d")
                        elif event.code == "BTN_BASE" and self.mode == 1:
                            self.danbus.config()
                            print("c")
                        elif event.code == "BTN_TOP2" and self.mode == 1:
                            self.danbus.go()
                            self.isRunning = True
                            print("g")
                        elif event.code == "BTN_BASE2" and self.mode != 1:
                            self.yaw_mode = not self.yaw_mode
                            print("yaw mode " + str(self.yaw_mode))
                        elif event.code == "ABS_RZ" and self.mode == 2 and self.yaw_mode == False:
                            self.p -= (1 - self.midJoystick) * self.p_inc
                            self.p = np.clip(self.p, self.p_min, self.p_max)
                            self.danbus.setP(self.p)
                            print("p " + str(self.p))
                        elif event.code == "ABS_RZ" and self.mode == 3 and self.yaw_mode == False:
                            self.i -= (1 - self.midJoystick) * self.i_inc
                            self.i = np.clip(self.i, self.i_min, self.i_max)
                            self.danbus.setI(self.i)
                            print("i " + str(self.i))
                        elif event.code == "ABS_RZ" and self.mode == 4 and self.yaw_mode == False:
                            self.d -= (1 - self.midJoystick) * self.d_inc
                            self.d = np.clip(self.d, self.d_min, self.d_max)
                            self.danbus.setD(self.d)
                            print("d " + str(self.d))
                        elif event.code == "ABS_RZ" and self.mode == 2 and self.yaw_mode == True:
                            self.q -= (1 - self.midJoystick) * self.p_inc
                            self.q = np.clip(self.q, self.p_min, self.p_max)
                            self.danbus.setQ(self.q)
                            print("yaw p " + str(self.q))
                        elif event.code == "ABS_RZ" and self.mode == 3 and self.yaw_mode == True:
                            self.j -= (1 - self.midJoystick) * self.i_inc
                            self.j = np.clip(self.j, self.i_min, self.i_max)
                            self.danbus.setJ(self.j)
                            print("yaw i " + str(self.j))
                        elif event.code == "ABS_RZ" and self.mode == 4 and self.yaw_mode == True:
                            self.b -= (1 - self.midJoystick) * self.d_inc
                            self.b = np.clip(self.b, self.d_min, self.d_max)
                            self.danbus.setB(self.b)
                            print("yaw d " + str(self.b))
                    else:
                        if event.code == "ABS_RZ" and self.mode == 2 and self.yaw_mode == False:
                            self.p -= (event.state - self.midJoystick) * self.p_inc
                            self.p = np.clip(self.p, self.p_min, self.p_max)
                            self.danbus.setP(self.p)
                            print("p " + str(self.p))
                        elif event.code == "ABS_RZ" and self.mode == 3 and self.yaw_mode == False:
                            self.i -= (event.state - self.midJoystick) * self.i_inc
                            self.i = np.clip(self.i, self.i_min, self.i_max)
                            self.danbus.setI(self.i)
                            print("i " + str(self.i))
                        elif event.code == "ABS_RZ" and self.mode == 4 and self.yaw_mode == False:
                            self.d -= (event.state - self.midJoystick) * self.d_inc
                            self.d = np.clip(self.d, self.d_min, self.d_max)
                            self.danbus.setD(self.d)
                            print("d " + str(self.d))
                        elif event.code == "ABS_RZ" and self.mode == 2 and self.yaw_mode == True:
                            self.q -= (event.state - self.midJoystick) * self.p_inc
                            self.q = np.clip(self.q, self.p_min, self.p_max)
                            self.danbus.setQ(self.q)
                            print("yaw p " + str(self.q))
                        elif event.code == "ABS_RZ" and self.mode == 3 and self.yaw_mode == True:
                            self.j -= (event.state - self.midJoystick) * self.i_inc
                            self.j = np.clip(self.j, self.i_min, self.i_max)
                            self.danbus.setJ(self.j)
                            print("yaw i " + str(self.j))
                        elif event.code == "ABS_RZ" and self.mode == 4 and self.yaw_mode == True:
                            self.b -= (event.state - self.midJoystick) * self.d_inc
                            self.b = np.clip(self.b, self.d_min, self.d_max)
                            self.danbus.setB(self.b)
                            print("yaw d " + str(self.b))
                else:
                    if event.code == "BTN_PINKIE" and event.state == 1:
                        self.isRunning = False
                        print("s")
                    elif event.code == "ABS_X":
                        self.yaw = self.map_num(event.state, self.minJoystick, self.maxJoystick, -self.dps_yaw, self.dps_yaw)
                        self.danbus.yaw(self.yaw)
                        print("yaw " + str(self.yaw))
                    elif event.code == "ABS_Y":
                        self.throttle = self.map_num(np.clip(event.state, self.minJoystick, self.midJoystick), 256, self.midJoystick, self.throttleDiff, self.minThrottle)
                        self.danbus.throttle(self.throttle)
                        print("throttle " + str(self.throttle))
                    elif event.code == "ABS_Z":
                        self.roll = self.map_num(event.state, self.minJoystick, self.maxJoystick, -self.dps, self.dps)
                        self.danbus.roll(self.roll)
                        print("roll " + str(self.roll))
                    elif event.code == "ABS_RZ":
                        self.pitch = self.map_num(event.state, self.maxJoystick, self.minJoystick, -self.dps, self.dps)
                        self.danbus.pitch(self.pitch)
                        print("pitch " + str(self.pitch))

    def map_num(self, num, fromLow, fromHigh, toLow, toHigh):
        return (num - fromLow) * (toHigh - toLow) / (fromHigh - fromLow) + toLow

if __name__ == "__main__":
    danbus = DanBus()
    relay = Gamepad_Relay(danbus)
    relay.start()
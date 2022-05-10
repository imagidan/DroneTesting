from inputs import get_gamepad
import threading
import numpy as np

class Gamepad:

    def __init__(self, danbus, constants_path):
        self.state = 0
        self.danbus = danbus
        self.danbus.start()
        self.constants = []
        self.p_max = 10
        self.p_inc = 0.0001
        self.i_max = 1
        self.i_inc = 0.00001
        self.d_max = 3
        self.d_inc = 0.0001
        self.minThrottle = 1000
        self.maxThrottle = 1600
        self.mode = 1
        self.joystickStateThrottle = 128
        self.joystickStatePitch = 128
        self.joystickStateRoll = 128
        self.joystickStateYaw = 128
        self.xyMode = 0
        self.zMode = 0
        self.tMode = 0
        self.t_inc = 0.01
        self.go = False
        self.minJoystick = 0
        self.maxJoystick = 255
        self.midJoystick = 128
        self.maxDeg = 45
        self.maxDPS = 150
        self.add = 0
        self.constants_path = constants_path

    def start(self):
        print("Load?")
        threading.Thread(target=self.run, args=()).start()
        return self

    def run(self):
        while 1:
            self.events = get_gamepad()
            self.stateMachine()
            if self.go == True:
                if self.mode != 0 and self.tMode == 0:
                    self.ThrottleSense()
                elif self.mode == 0 and self.xyMode != 2:
                    if self.xyMode == 0:
                        self.PitchSense(0, 0)
                    else:
                        self.PitchSense(0, 1)

                if self.mode != 0 and self.zMode == 0:
                    self.YawSense()
                elif self.mode == 0 and self.xyMode != 2:
                    if self.xyMode == 0:
                        self.RollSense(0, 0)
                    else:
                        self.RollSense(0, 1)

                if self.mode == 3:
                    if self.xyMode == 0:
                        self.PitchSense(1, 0)
                        self.RollSense(1, 0)
                    elif self.xyMode == 1:
                        self.PitchSense(1, 1)
                        self.RollSense(1, 1)
                
    def stateMachine(self):
        if self.state == 0:
            self.Load()
        elif self.state == 1:
            self.Config()
        elif self.state == 2:
            self.Go()
        elif self.state == 3:
            self.ConfigMode()
        elif self.state == 4:
            self.Mode()
        elif self.state == 5:
            self.Test()
        elif self.state == 6:
            self.ConstantXY()
        elif self.state == 7:
            self.ConstantZ()
        elif self.state == 8:
            self.ConstantT()    
        elif self.state == 9:
            self.Adjust()

    def Load(self):
        for event in self.events:
            if event.state == 1:
                if event.code == "BTN_TOP2":
                    self.LoadConstants()
                    print("Constants Loaded")
                    print("Config?")
                    self.state = 1
                elif event.code == "BTN_PINKIE":
                    print("Constants not loaded")
                    self.constants = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1000]
                    print("Config?")
                    self.state = 1

    def LoadConstants(self):
        constants_txt = open(self.constants_path, "r")
        lines = constants_txt.readlines()
        for line in lines:
            self.constants.append(float(line))
        constants_txt.close()

    def Config(self):
        for event in self.events:
            if event.state == 1:
                if event.code == "BTN_TOP2":
                    self.danbus.setConfig()
                    print("Go?")
                    self.state = 2
                elif event.code == "BTN_BASE":
                    print("Load?")
                    self.state = 0

    def Go(self):
        for event in self.events:
            if event.state == 1:
                if event.code == "BTN_TOP2":
                    self.go = True
                    self.danbus.setGo()
                    print("Config Mode?")
                    self.state = 3
                elif event.code == "BTN_BASE":
                    print("Config?")
                    self.state = 1

    def ConfigMode(self):
        for event in self.events:
            if event.state == 1:
                if event.code == "BTN_TRIGGER":
                    self.mode = 0
                    print("XY Mode Selected")
                    print("PID Mode?")
                    self.state = 4
                elif event.code == "BTN_THUMB":
                    self.mode = 1
                    print("Yaw Mode Selected")
                    print("PID Mode?")
                    self.state = 4
                elif event.code == "BTN_THUMB2":
                    self.mode = 2
                    print("Throttle Mode Selected")
                    print("PID Mode?")
                    self.state = 4
                elif event.code == "BTN_TOP":
                    self.mode = 3
                    print("Test Mode Selected")
                    self.state = 5
                elif event.code == "BTN_BASE4":
                    print("Saving Constants")
                    self.SaveConstants()
                elif event.code == "BTN_BASE" or event.code == "BTN_BASE2":
                    print("Go?")
                    self.danbus.setStop()
                    self.go = False
                    self.state = 2
    
    def Mode(self):
        for event in self.events:
            if event.state == 1:
                if event.code == "BTN_TRIGGER":
                    if self.mode == 0:
                        self.state = 6
                        self.xyMode = 0
                        self.pitch = 0
                        self.roll = 0
                        print("XY Mode Acro")
                        print("Constant XY?")
                    elif self.mode == 1:
                        self.state = 7
                        self.zMode = 0
                        self.yaw = 0
                        self.danbus.setZ(self.yaw)
                        self.danbus.setZMode(0)
                        print("Yaw Mode Acro")
                        print("Constant Yaw?")
                    elif self.mode == 2:
                        self.state = 8
                        self.tMode = 0
                        self.throttle = self.minThrottle
                        self.danbus.setThrottle(self.throttle)
                        print("Throttle Mode Acro")
                        print("Constant Throttle?")
                elif event.code == "BTN_THUMB":
                    if self.mode == 0:
                        self.state = 6
                        self.xyMode = 1
                        self.pitch = 0
                        self.roll = 0
                        print("XY Mode Stabilize")
                        print("Constant XY?")
                    elif self.mode == 1:
                        self.state = 7
                        self.zMode = 1
                        self.yaw = 0
                        self.danbus.setZ(self.yaw)
                        self.danbus.setZMode(1)
                        print("Yaw Mode Stabilize")
                        print("Constant Yaw?")
                    elif self.mode == 2:
                        self.state = 8
                        self.tMode = 1
                        self.throttle = self.minThrottle
                        self.danbus.setT(self.throttle)
                        print("Throttle Mode Stabilize")
                        print("Constant Throttle?")
                elif event.code == "BTN_THUMB2":
                    if self.mode == 0:
                        self.state = 6
                        self.xyMode = 2
                        self.pitch = 0
                        self.roll = 0
                        print("XY Mode Off")
                        print("Constant XY?")
                    elif self.mode == 1:
                        self.state = 7
                        self.zMode = 2
                        self.yaw = 0
                        self.danbus.setZ(self.yaw)
                        print("Yaw Mode Off")
                        print("Constant Yaw?")
                    elif self.mode == 2:
                        self.state = 8
                        self.tMode = 2
                        self.throttle = self.minThrottle
                        self.danbus.setT(self.throttle)
                        print("Throttle Mode Off")
                        print("Constant Throttle?")
                elif event.code == "BTN_BASE":
                    self.state = 3
                    print("Config Mode?")
                elif event.code == "BTN_BASE4":
                    print("Saving Constants")
                    self.SaveConstants()
                elif event.code == "BTN_BASE2":
                    print("Go?")
                    self.danbus.setStop()
                    self.go = False
                    self.state = 2
    
    def Test(self):
        for event in self.events:
            if event.code == "BTN_BASE":
                print("Config Mode?")
                self.state = 3
            elif event.code == "BTN_BASE4":
                print("Saving Constants")
                self.SaveConstants()
            elif event.code == "BTN_BASE2":
                print("Go?")
                self.danbus.setStop()
                self.go = False
                self.state = 2

    def ConstantXY(self):
        for event in self.events:
            if event.state == 1:
                if event.code == "BTN_TRIGGER":
                    self.state = 9
                    print("Adjust Constant kpa xy")
                    #self.const_index = 0
                elif event.code == "BTN_THUMB":
                    self.state = 9
                    print("Adjust Constant kia xy")
                    #self.const_index = 5
                elif event.code == "BTN_THUMB2":
                    self.state = 9
                    print("Adjust Constant kda xy")
                    #self.const_index = 10
                elif event.code == "BTN_TOP":
                    self.state = 9
                    print("Adjust Constant kps xy")
                    #self.const_index = 1
                elif event.code == "BTN_TOP2":
                    self.state = 9
                    print("Adjust Constant kis xy")
                    #self.const_index = 6
                elif event.code == "BTN_PINKIE":
                    self.state = 9
                    print("Adjust Constant kds xy")
                    #self.const_index = 11
                elif event.code == "BTN_BASE":
                    print("Mode?")
                    self.state = 4
                elif event.code == "BTN_BASE4":
                    print("Saving Constants")
                    self.SaveConstants()
                elif event.code == "BTN_BASE2":
                    print("Go?")
                    self.danbus.setStop()
                    self.go = False
                    self.state = 2
                
    def ConstantZ(self):
        for event in self.events:
            if event.state == 1:
                if event.code == "BTN_TRIGGER":
                    self.state = 9
                    print("Adjust Constant kpa yaw")
                    self.const_index = 0
                elif event.code == "BTN_THUMB":
                    self.state = 9
                    print("Adjust Constant kia yaw")
                    self.const_index = 3
                elif event.code == "BTN_THUMB2":
                    self.state = 9
                    print("Adjust Constant kda yaw")
                    self.const_index = 6
                elif event.code == "BTN_TOP":
                    self.state = 9
                    print("Adjust Constant kps yaw")
                    self.const_index = 1
                elif event.code == "BTN_TOP2":
                    self.state = 9
                    print("Adjust Constant kis yaw")
                    self.const_index = 4
                elif event.code == "BTN_PINKIE":
                    self.state = 9
                    print("Adjust Constant kds yaw")
                    self.const_index = 7
                elif event.code == "BTN_BASE":
                    print("Mode?")
                    self.state = 4
                elif event.code == "BTN_BASE4":
                    print("Saving Constants")
                    self.SaveConstants()
                elif event.code == "BTN_BASE2":
                    print("Go?")
                    self.danbus.setStop()
                    self.go = False
                    self.state = 2
    
    def ConstantT(self):
        for event in self.events:
            if event.state == 1:
                if event.code == "BTN_TRIGGER":
                    self.state = 9
                    print("Adjust Constant kp throttle")
                    self.const_index = 2
                elif event.code == "BTN_THUMB":
                    self.state = 9
                    print("Adjust Constant ki throttle")
                    self.const_index = 5
                elif event.code == "BTN_THUMB2":
                    self.state = 9
                    print("Adjust Constant kd throttle")
                    self.const_index = 8
                elif event.code == "BTN_TOP":
                    self.state = 9
                    print("Adjust Constant hover throttle")
                    self.const_index = 9
                elif event.code == "BTN_BASE":
                    print("Mode?")
                    self.state = 4
                elif event.code == "BTN_BASE4":
                    print("Saving Constants")
                    self.SaveConstants()
                elif event.code == "BTN_BASE2":
                    print("Go?")
                    self.danbus.setStop()
                    self.go = False
                    self.state = 2

    def constantDanBusMux(self, value):
        if self.const_index == 0:
            self.danbus.setKpaZ(value)
        elif self.const_index == 1:
            self.danbus.setKpsZ(value)
        elif self.const_index == 2:
            self.danbus.setKpsT(value)
        elif self.const_index == 3:
            self.danbus.setKiaZ(value)
        elif self.const_index == 4:
            self.danbus.setKisZ(value)
        elif self.const_index == 5:
            self.danbus.setKisT(value)
        elif self.const_index == 6:
            self.danbus.setKdaZ(value)
        elif self.const_index == 7:
            self.danbus.setKdsZ(value)
        elif self.const_index == 8:
            self.danbus.setKdsT(value)
        elif self.const_index == 9:
            self.danbus.setHoverT(value)

    def Adjust(self):
        for event in self.events:
            if event.code == "ABS_RZ":
                self.add = self.midJoystick - event.state
                if abs(self.add) < 2 and self.add != 0:
                    self.add = 0
            elif event.code == "BTN_BASE":
                if self.mode == 0:
                    print("Constant XY?")
                    self.state = 6
                elif self.mode == 1:
                    print("Constant Yaw?")
                    self.state = 7
                elif self.mode == 2:
                    print("Constant Throttle?")
                    self.state = 8
            elif event.code == "BTN_BASE4":
                    print("Saving Constants")
                    self.SaveConstants()
            elif event.code == "BTN_BASE2":
                self.go = False
                self.danbus.setStop()
                print("Go?")
                self.state = 2
        if self.const_index < 5:
            self.constants[self.const_index] += self.add * self.p_inc
            self.constants[self.const_index] = np.clip(self.constants[self.const_index], 0, self.p_max)
        elif self.const_index >= 5 and self.const_index < 10:
            self.constants[self.const_index] += self.add * self.i_inc
            self.constants[self.const_index] = np.clip(self.constants[self.const_index], 0, self.i_max)
        elif self.const_index >= 10 and self.const_index < 15:
            self.constants[self.const_index] += self.add * self.d_inc
            self.constants[self.const_index] = np.clip(self.constants[self.const_index], 0, self.d_max)
        elif self.const_index == 15:
            self.constants[self.const_index] += self.add * self.t_inc
            self.constants[self.const_index] = np.clip(self.constants[self.const_index], self.minThrottle, self.maxThrottle)
        print("Constant Value: " + str(self.constants[self.const_index]))

    def ThrottleSense(self):
        for event in self.events:
            if event.code == "ABS_Y":
                self.joystickStateThrottle = event.state
        if self.joystickStateThrottle < self.midJoystick:
            self.throttle = self.map_num(self.joystickStateThrottle, self.minJoystick, self.midJoystick, self.minThrottle, self.maxThrottle)
            self.throttle = self.maxThrottle - (self.throttle - self.minThrottle)
            if abs(self.throttle) < 1040 and self.throttle != 1000:
                self.throttle = 1000
            self.danbus.setThrottle(self.throttle)
            #print("Throttle: " + str(self.throttle))

    def YawSense(self):
        for event in self.events:
            if event.code == "ABS_X":
                self.joystickStateYaw = event.state

        self.yaw = self.map_num(self.joystickStateYaw, self.minJoystick, self.maxJoystick, -self.maxDPS, self.maxDPS)
        if abs(self.yaw) < 3 and self.yaw != 0:
            self.yaw = 0
        self.danbus.setYaw(self.yaw)
        #print("Yaw: " + str(self.yaw))

    def PitchSense(self, joystickPosition, mode):
        for event in self.events:
            if joystickPosition == 0:
                if event.code == "ABS_Y":
                    self.joystickStatePitch = event.state
            else:
                if event.code == "ABS_RZ":
                    self.joystickStatePitch = event.state
        if mode == 0:
            self.pitch = self.map_num(self.joystickStatePitch, self.minJoystick, self.maxJoystick, -self.maxDeg, self.maxDeg)
            self.pitch = self.maxDeg - (self.pitch + self.maxDeg)

            if abs(self.pitch) < 2 and self.pitch != 0:
                self.pitch = 0
        else:
            self.pitch = self.map_num(self.joystickStatePitch, self.minJoystick, self.maxJoystick, -self.maxDPS, self.maxDPS)
            self.pitch = self.maxDPS - (self.pitch + self.maxDPS)

            if abs(self.pitch) < 6 and self.pitch != 0:
                self.pitch = 0

        #print("Pitch: " + str(self.pitch))

    def RollSense(self, joystickPosition, mode):
        for event in self.events:
            if joystickPosition == 0:
                if event.code == "ABS_X":
                    self.joystickStateRoll = event.state
            else:
                if event.code == "ABS_Z":
                    self.joystickStateRoll = event.state
        if mode == 0:
            self.roll = self.map_num(self.joystickStateRoll, self.minJoystick, self.maxJoystick, -self.maxDeg, self.maxDeg)
            if abs(self.roll) < 2 and self.roll != 0:
                self.roll = 0
        else:
            self.roll = self.map_num(self.joystickStateRoll, self.minJoystick, self.maxJoystick, -self.maxDPS, self.maxDPS)
            if abs(self.roll) < 6 and self.roll != 0:
                self.roll = 0

        #print("Roll: " + str(self.roll))

    def map_num(self, num, fromLow, fromHigh, toLow, toHigh):
        return (num - fromLow) * (toHigh - toLow) / (fromHigh - fromLow) + toLow

    def SaveConstants(self):
        constants_txt = open(self.constants_path, "w")
        write_str = ""
        for constant in self.constants:
            write_str += str(constant) + "\n"
        constants_txt.write(write_str)
        constants_txt.close()
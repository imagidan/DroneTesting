import serial
import time
import glob

class Serial:

    def __init__(self):
        self.serial_port = self.getSerial()

    def selectPort(self):
        ports = glob.glob('/dev/ttyACM[0-9]*')
        return ports[0]

    def getSerial(self):
        serial_port = serial.Serial(
            port=self.selectPort(),
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )
        
        return serial_port

    def sendMsg(self, msg):
        self.serial_port.write(msg.encode())

    def getMsg(self):
        if self.serial_port.inWaiting() > 0:
            return self.serial_port.readline().decode().replace("\n", "").replace("\r", "")
        else:
            return ""
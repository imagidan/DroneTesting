import scripts.serialConnection as serialConnection
import time
import glob

class SerialConnection:
    
    def __init__(self, baud=115200):
        self.serial_port = self.getSerial()
        self.baud = baud

    def selectPort(self):
        ports = glob.glob('/dev/ttyACM[0-9]*')
        return ports[0]

    def getSerial(self):
        serial_port = serialConnection.Serial(
            port=self.selectPort(),
            baudrate=self.baud,
            bytesize=serialConnection.EIGHTBITS,
            parity=serialConnection.PARITY_NONE,
            stopbits=serialConnection.STOPBITS_ONE,
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
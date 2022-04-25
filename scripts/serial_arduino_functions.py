import serial
import time
import glob

def selectPort():
    ports = glob.glob('/dev/ttyACM[0-9]*')
    return ports[0]

def getSerial():
    serial_port = serial.Serial(
        port=selectPort(),
        baudrate=115200,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )

    time.sleep(1)

    return serial_port

def sendMsg(serial_port, msg):
    serial_port.write(msg.encode())

def getMsg(serial_port):
    if serial_port.inWaiting() > 0:
        return serial_port.readline().decode().replace("\n", "").replace("\r", "")
    else:
        return ""
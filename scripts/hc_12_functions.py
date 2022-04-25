import serial
import time
import subprocess

def checkBoardType():
    out = subprocess.Popen(['cat', '/sys/module/tegra_fuse/parameters/tegra_chip_id'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, _ = out.communicate()
    chip_id = int(stdout.decode("utf-8"))

    if chip_id == 25:
        return "Xavier"
    elif chip_id == 33:
        return "Nano"
    else:
        return "Unknown"

def selectPort():
    jetsonType = checkBoardType()
    
    if jetsonType == "Xavier":
        return "/dev/ttyTHS0"
    elif jetsonType == "Nano":
        return "/dev/ttyTHS1"

def setDefault(serial_port):
    serial_port.write("AT+DEFAULT\n".encode())

def getSerial():
    serial_port = serial.Serial(
        port=selectPort(),
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )
    
    time.sleep(1)

    print(serial_port)

    return serial_port

def sendMsg(serial_port, msg):
    serial_port.write(msg.encode())

def getMsg(serial_port):
    if serial_port.inWaiting() > 0:
        return serial_port.readline().decode().replace("\r\n", "\n")
    else:
        return ""
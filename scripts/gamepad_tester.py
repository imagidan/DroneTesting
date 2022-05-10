from gamepad import Gamepad
from danbus import DanBus

danbus = DanBus()
gamepad = Gamepad(danbus, "saved_constants.txt")
gamepad.start()

a = 0

while 1:
    a += 1
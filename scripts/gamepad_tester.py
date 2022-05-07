from gamepad import Gamepad

gamepad = Gamepad("saved_constants.txt")
gamepad.start()

a = 0

while 1:
    a += 1
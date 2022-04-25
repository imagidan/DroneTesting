from __future__ import print_function
import time

import inputs

def main(gamepad=None):
    if not gamepad:
        gamepad = inputs.devices.gamepads[0]

    gamepad.set_vibration(1, 0, 1000)

    time.sleep(2)

    gamepad.set_vibration(0, 1, 1000)
    time.sleep(2)

    gamepad.set_vibration(1, 1, 2000)
    time.sleep(2)

if __name__ == "__main__":
    main()
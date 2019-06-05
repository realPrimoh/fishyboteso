import pynput
from pynput.keyboard import Key, Listener
import time

mouse = pynput.mouse.Controller()

sensitivity = 20#10

keyboard = pynput.keyboard.Controller()

def on_press(key):
    if key == Key.up:
        mouse.move(0, -sensitivity)
    elif key == Key.down:
        mouse.move(0, sensitivity)
    elif key == Key.left:
        mouse.move(-sensitivity, 0)
    elif key == Key.right:
        mouse.move(sensitivity, 0)


def changeMoveValue(x):
    global sensitivity
    sensitivity = float(x)


def start():
    # Collect events until released

    with Listener(on_press=on_press) as lis:
        x = float(input("x?"))

        time.sleep(3)

        for i in range(360):
            keyboard.press(Key.left)

        y = float(input("y?"))

        # r = float(input("complete rotations?"))

        newSen = 360 / (360 + (y-x)) * sensitivity

        print(newSen)

        #lis.join()

if __name__ == "__main__":
    sensitivity = 8
    start()

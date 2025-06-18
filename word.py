import time
import threading
import keyboard
import pyautogui
from sys import exit

do_enter = False
stop_script = False
pixel_x, pixel_y = 0, 0

def press_enter_twice():
    global stop_script
    time.sleep(1)
    keyboard.press_and_release('enter')
    time.sleep(0.3)
    keyboard.press_and_release('enter')
    time.sleep(1.2)

    r, g, b = pyautogui.screenshot().getpixel((pixel_x, pixel_y))
    if r >= 245 and g >= 245 and b >= 245:
        keyboard.press_and_release('y')
        time.sleep(0.3)
        keyboard.press_and_release('down')
        time.sleep(0.3)
        keyboard.press_and_release('enter')
        time.sleep(0.3)
        keyboard.press_and_release('enter')
        time.sleep(5)
        stop_script = True
        print("Stopping script.")
    else:
        keyboard.press_and_release('esc')
        time.sleep(0.3)
        press_enter_twice()

def background_loop():
    global do_enter, stop_script
    while not stop_script:
        if do_enter:
            press_enter_twice()
            do_enter = False
        time.sleep(0.5)

def on_space_press(e):
    global do_enter
    do_enter = True

def on_q_press(e):
    global stop_script
    stop_script = True
    print("Stopping script.")

def on_p_press(e):
    global pixel_x, pixel_y
    pixel_x, pixel_y = pyautogui.position()
    keyboard.on_press_key('space', on_space_press)
    print("Press SPACE to trigger, Q to quit.")

thread = threading.Thread(target=background_loop, daemon=True)
thread.start()

keyboard.on_press_key('p', on_p_press)
keyboard.on_press_key('q', on_q_press)
print("Steps:\n1. Lock your fps at a stable value (e.g. 82fps)\n2. Turn off fullscreen for better visibility\n3. Open auction and find any car that is currently listed\n4. Move your cursor to a clear white part of the listing and then press p")
# print("Move your cursor onto the topmost listing's center and then press p")
# print("After that go back to the auction page")
# print("Tips:\n1. Turn off fulscreen\n2. Lock your fps so it's stable")
try:
    while not stop_script:
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
import time
import threading
import keyboard
import pyautogui

do_enter = False
stop_script = False
pixel_x, pixel_y = 0, 0
infinite = False

def press_enter_twice():
    global stop_script
    while True:
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
            if infinite:
                keyboard.press_and_release('enter')
                time.sleep(1)
                keyboard.press_and_release('enter')
                time.sleep(10)
                keyboard.press_and_release('enter')
                time.sleep(1)
                keyboard.press_and_release('esc')
                time.sleep(1)
                keyboard.press_and_release('esc')
                print("\nCar collected.")
            else:
                keyboard.press_and_release('enter')
                time.sleep(1)
                keyboard.press_and_release('enter')
                time.sleep(10)
                keyboard.press_and_release('enter')
                time.sleep(1)
                keyboard.press_and_release('esc')
                time.sleep(1)
                keyboard.press_and_release('esc')
                keyboard.on_press_key('space', on_space_press)
                print("\nAuction finished. Press SPACE to trigger, I for inifinte sniping toggle, Q to quit.")
                break
        else:
            keyboard.press_and_release('esc')
            time.sleep(0.3)

def background_loop():
    global do_enter, stop_script
    while not stop_script:
        if do_enter:
            press_enter_twice()
            do_enter = False
        time.sleep(0.5)

def on_space_press(_):
    global do_enter
    keyboard.unhook_key('space')
    print("\nStarting script.")
    do_enter = True

def on_q_press(_):
    global stop_script
    stop_script = True
    print("\nStopping script.")

def on_p_press(_):
    global pixel_x, pixel_y
    pixel_x, pixel_y = pyautogui.position()
    print("5. Now go to the auction page")
    print(f"\nChecking the pixel ({pixel_x}, {pixel_y})")
    keyboard.on_press_key('space', on_space_press)
    keyboard.on_press_key('i', on_i_press)
    print("\nPress SPACE to trigger, I for infinite sniping toggle, Q to quit.")

def on_i_press(_):
    global infinite
    if infinite:
        infinite = False
        print("Infinite sniping Off", end="\r")
    else:
        infinite = True
        print("Infinite sniping On ", end="\r")

thread = threading.Thread(target=background_loop, daemon=True)
thread.start()

keyboard.on_press_key('p', on_p_press)
keyboard.on_press_key('q', on_q_press)
print("Steps:\n1. Lock your fps at a stable value (e.g. 83fps)\n2. Turn off fullscreen for better visibility\n3. Open auction and find any car that is currently listed\n4. Move your cursor to a clear white part of the listing and then press P")
try:
    while not stop_script:
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
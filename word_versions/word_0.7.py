from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QInputDialog
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
from pyautogui import screenshot
from time import sleep
from pynput import keyboard
from pynput.keyboard import Controller, Key
from threading import Thread
from random import uniform
import sys, win32gui

class KeyDispatcher(QObject):
    key_released = pyqtSignal(str)

class Sniper():
    def normal_snipe():
        global running
        Logic.calculate_pixel_coords()
        sleep(1)
        kboard.tap(Key.enter)
        sleep(0.3)
        kboard.tap(Key.enter)
        sleep(1.2)

        r, g, b = screenshot().getpixel((pixel_x, pixel_y))
        if r >= 230 and g >= 230 and b >= 230:
            kboard.tap("y")
            sleep(0.3)
            kboard.tap(Key.down)
            sleep(0.3)
            kboard.tap(Key.enter)
            sleep(0.3)
            kboard.tap(Key.enter)
            sleep(5)
            r, g, b = screenshot().getpixel((x, y))
            if r >= 230 and g >= 230 and b >= 230:
                kboard.tap(Key.enter)
                sleep(1)
                kboard.tap(Key.enter)
                sleep(10)
                kboard.tap(Key.enter)
                sleep(1)
                kboard.tap(Key.esc)
                sleep(1)
                kboard.tap(Key.esc)
                if infinite:
                    Logic.message("Car collected", True)
                else:
                    Logic.message("Auction finished", False)
                    Sniper.finish_snipe()
            else:
                kboard.tap(Key.enter)
                sleep(1)
                kboard.tap(Key.esc)
                sleep(1)
                kboard.tap(Key.esc)
                sleep(0.5)
        else:
            kboard.tap(Key.esc)
            sleep(0.5)
    def quick_snipe():
        global running
        Logic.calculate_pixel_coords()
        sleep(1)
        kboard.tap(Key.enter)
        sleep(0.3)
        kboard.tap(Key.enter)
        sleep(0.85)

        r, g, b = screenshot().getpixel((pixel_x, pixel_y))
        if r >= 230 and g >= 230 and b >= 230:
            kboard.tap("y")
            sleep(0.3)
            kboard.tap(Key.down)
            sleep(0.3)
            kboard.tap(Key.enter)
            sleep(0.3)
            kboard.tap(Key.enter)
            sleep(5)
            r, g, b = screenshot().getpixel((x, y))
            if r >= 230 and g >= 230 and b >= 230:
                kboard.tap(Key.enter)
                sleep(1)
                kboard.tap(Key.enter)
                sleep(10)
                kboard.tap(Key.enter)
                sleep(1)
                kboard.tap(Key.esc)
                sleep(1)
                kboard.tap(Key.esc)
                if infinite:
                    Logic.message("Car collected", True)
                else:
                    Logic.message("Auction finished", False)
                    Sniper.finish_snipe()
            else:
                kboard.tap(Key.enter)
                sleep(1)
                kboard.tap(Key.esc)
                sleep(1)
                kboard.tap(Key.esc)
        else:
            kboard.tap(Key.esc)
    def safe_snipe():
        global running
        Logic.calculate_pixel_coords()
        sleep(uniform(1, 1.5))
        kboard.tap(Key.enter)
        sleep(uniform(0.3, 0.8))
        kboard.tap(Key.enter)
        sleep(uniform(1, 1.4))

        r, g, b = screenshot().getpixel((pixel_x, pixel_y))
        if r >= 230 and g >= 230 and b >= 230:
            kboard.tap("y")
            sleep(uniform(0.3, 0.5))
            kboard.tap(Key.down)
            sleep(uniform(0.3, 0.5))
            kboard.tap(Key.enter)
            sleep(uniform(0.3, 0.5))
            kboard.tap(Key.enter)
            sleep(uniform(5, 5.9))
            r, g, b = screenshot().getpixel((x, y))
            if r >= 230 and g >= 230 and b >= 230:
                kboard.tap(Key.enter)
                sleep(uniform(0.5, 1.5))
                kboard.tap(Key.enter)
                sleep(uniform(9.5, 12.7))
                kboard.tap(Key.enter)
                sleep(uniform(0.5, 1.5))
                kboard.tap(Key.esc)
                sleep(uniform(0.5, 1.5))
                kboard.tap(Key.esc)
                if infinite:
                    Logic.message("Car collected", True)
                else:
                    Logic.message("Auction finished", False)
                    Sniper.finish_snipe()
            else:
                kboard.tap(Key.enter)
                sleep(uniform(0.5, 1.5))
                kboard.tap(Key.esc)
                sleep(uniform(0.5, 1.5))
                kboard.tap(Key.esc)
                sleep(uniform(0.5, 1.5))
        else:
            kboard.tap(Key.esc)
            sleep(uniform(0.5, 1.5))
    def custom_snipe():
        global running

        sleep(delay_config["initial_delay"])
        kboard.tap(Key.enter)

        sleep(delay_config["quick_click_delay"])
        kboard.tap(Key.enter)

        sleep(delay_config["auction_check_delay"])
        r, g, b = screenshot().getpixel((delay_config["auction_pixel_x"], delay_config["auction_pixel_y"]))

        if r >= 230 and g >= 230 and b >= 230:
            kboard.tap("y")
            sleep(delay_config["quick_click_delay"])
            kboard.tap(Key.down)
            sleep(delay_config["quick_click_delay"])
            kboard.tap(Key.enter)
            sleep(delay_config["quick_click_delay"])
            kboard.tap(Key.enter)

            sleep(delay_config["short_wait_delay"])
            r, g, b = screenshot().getpixel((delay_config["buyout_pixel_x"], delay_config["buyout_pixel_y"]))

            if r >= 230 and g >= 230 and b >= 230:
                kboard.tap(Key.enter)
                sleep(delay_config["safe_delay"])
                kboard.tap(Key.enter)
                sleep(delay_config["long_wait_delay"])
                kboard.tap(Key.enter)
                sleep(delay_config["safe_delay"])
                kboard.tap(Key.esc)
                sleep(delay_config["safe_delay"])
                kboard.tap(Key.esc)

                if infinite:
                    Logic.message("Car collected", True)
                else:
                    Logic.message("Auction finished", False)
                    Sniper.finish_snipe()
            else:
                kboard.tap(Key.enter)
                sleep(delay_config["safe_delay"])
                kboard.tap(Key.esc)
                sleep(delay_config["safe_delay"])
                kboard.tap(Key.esc)
                sleep(delay_config["end_delay"])
        else:
            kboard.tap(Key.esc)
            sleep(delay_config["end_delay"])
    def finish_snipe():
        global running
        running = False
        Logic.update_button_state()
        start_btn.setStyleSheet(button_style_unfocused)
        start_btn.setText("Start (S)")

class Logic():
    def safe():
        global snipe_type
        snipe_type = "safe"
        Logic.message("Safe sniping on", True)
        safe_btn.setStyleSheet(button_style_focused)
        normal_btn.setStyleSheet(button_style_unfocused)
        custom_btn.setStyleSheet(button_style_unfocused)
        quick_btn.setStyleSheet(button_style_unfocused)
    def normal():
        global snipe_type
        snipe_type = "normal"
        Logic.message("Normal sniping on", True)
        safe_btn.setStyleSheet(button_style_unfocused)
        normal_btn.setStyleSheet(button_style_focused)
        custom_btn.setStyleSheet(button_style_unfocused)
        quick_btn.setStyleSheet(button_style_unfocused)
    def quick():
        global snipe_type
        snipe_type = "quick"
        Logic.message("Quick sniping on", True)
        safe_btn.setStyleSheet(button_style_unfocused)
        normal_btn.setStyleSheet(button_style_unfocused)
        custom_btn.setStyleSheet(button_style_unfocused)
        quick_btn.setStyleSheet(button_style_focused)
    def custom():
        global snipe_type
        snipe_type = "custom"
        Logic.message("Input custom values", False)
        safe_btn.setStyleSheet(button_style_unfocused)
        normal_btn.setStyleSheet(button_style_unfocused)
        quick_btn.setStyleSheet(button_style_unfocused)
        custom_btn.setStyleSheet(button_style_focused)

        for i, key in enumerate(delay_config):
            label = key.replace("_", " ").title()
            is_pixel = "pixel" in key.lower()

            if is_pixel:
                prompt = f"Enter {label} (default value: {defaults[i]}):"
                decimals = 0
            else:
                prompt = f"Enter {label} in seconds (default value: {defaults[i]}):"
                decimals = 2

            value, ok = QInputDialog.getDouble(window, label, prompt, decimals=decimals)

            if ok and value >= 0:
                delay_config[key] = int(value) if is_pixel else value
            else:
                Logic.message("Invalid value set", True)
                snipe_type = "safe"
                Logic.update_button_state()
                return None
        Logic.message("Values set", True)
    def update_button_state():
        if running:
            for button in state_buttons:
                button.setStyleSheet(button_style_disabled)
                button.setEnabled(False)
        else:
            for button in state_buttons:
                button.setStyleSheet(button_style_unfocused)
                button.setEnabled(True)
            if infinite:
                inf_btn.setStyleSheet(button_style_focused)
            if snipe_type == "safe":
                safe_btn.setStyleSheet(button_style_focused)
            elif snipe_type == "normal":
                normal_btn.setStyleSheet(button_style_focused)
            elif snipe_type == "custom":
                custom_btn.setStyleSheet(button_style_focused)
            else:
                quick_btn.setStyleSheet(button_style_focused)
    def get_window_bbox(title):
        def enum_callback(hwnd, result):
            if win32gui.IsWindowVisible(hwnd) and title.lower() in win32gui.GetWindowText(hwnd).lower():
                result.append(hwnd)
        
        hwnds = []
        win32gui.EnumWindows(enum_callback, hwnds)
        if not hwnds:
            print(f"{title} not found")
            return None
        hwnd = hwnds[0]
        rect = win32gui.GetClientRect(hwnd)
        x, y = win32gui.ClientToScreen(hwnd, (0, 0))
        width = rect[2] - rect[0]
        height = rect[3] - rect[1]
        return {"x": x, "y": y, "width": width, "height": height}
    def calculate_pixel_coords():
        global x, y, pixel_x, pixel_y
        tries = 0
        bbox = Logic.get_window_bbox("Forza Horizon 5")
        while not bbox:
            if tries < 5:
                tries += 1
                sleep(2)
                bbox = Logic.get_window_bbox("Forza Horizon 5")
            else:
                print("Launch Forza and try again")
                sys.exit()

        rel1_x, rel1_y = 1095 / 1920, 480 / 1080
        rel2_x, rel2_y = 570 / 1920, 370 / 1080

        pixel_x = int(rel2_x * bbox['width']) + bbox['x']
        pixel_y = int(rel2_y * bbox['height']) + bbox['y']

        x = int(rel1_x * bbox['width']) + bbox['x']
        y = int(rel1_y * bbox['height']) + bbox['y']
    def mousePressEvent(event):
        if event.button() == Qt.LeftButton:
            drag_pos["pos"] = event.globalPos() - window.frameGeometry().topLeft()
    def mouseMoveEvent(event):
        if drag_pos["pos"]:
            window.move(event.globalPos() - drag_pos["pos"])
    def mouseReleaseEvent(_):
        drag_pos["pos"] = None
    def bind_key(char, func):
        keymap[char.lower()] = func
    def on_press(key):
        try:
            char = key.char.lower()
            if char in keymap and not key_states.get(char, False):
                key_states[char] = True
                dispatcher.key_released.emit(char)
        except AttributeError:
            pass
    def on_release(key):
        try:
            char = key.char.lower()
            key_states[char] = False
        except AttributeError:
            pass
    def start_key_listener():
        listener = keyboard.Listener(on_press=Logic.on_press, on_release=Logic.on_release)
        listener.start()
        listener.join()
    def handle_keybind(char):
        func = keymap.get(char.lower())
        if func:
            func()
    def message(text, timed):
        timer.stop()
        try:
            timer.timeout.disconnect()
        except TypeError:
            pass
        if timed:
            message_txt.setText(text)
            timer.timeout.connect(Logic.clear_msg)
            timer.start(3000)
        else:
            message_txt.setText(text)
    def clear_msg():
        Logic.message("", False)
    def infinite_snipe():
        global infinite
        if infinite:
            inf_btn.setStyleSheet(button_style_unfocused)
            inf_btn.setText("Infinite sniping")
            Logic.message("Infinite sniping off", True)
            infinite = False
        else:
            inf_btn.setStyleSheet(button_style_focused)
            inf_btn.setText("Infinite sniping")
            Logic.message("Infinite sniping on", True)
            infinite = True
    def is_focused():
        allowed_titles = [
            "Forza Horizon 5",
            "word",
            "python",
            f"word_{version}"
        ]

        hwnd = win32gui.GetForegroundWindow()
        if not hwnd:
            return False

        window_title = win32gui.GetWindowText(hwnd).lower()
        return any(title.lower() in window_title for title in allowed_titles)
    def start():
        global running
        if Logic.is_focused():
            if running:
                start_btn.setStyleSheet(button_style_unfocused)
                start_btn.setText("Start (S)")
                running = False
                Logic.update_button_state()
                Logic.message("", False)
            else:
                start_btn.setStyleSheet(button_style_focused)
                start_btn.setText("Stop (S)")
                running = True
                Logic.update_button_state()
                if infinite:
                    Logic.message("Looking for auctions...", True)
                else:
                    Logic.message("Looking for auctions...", False)
                Thread(target=Logic.background_loop, daemon=True).start()
    def quit():
        if Logic.is_focused():
            app.quit()
            sys.exit()
    def background_loop():
        while running:
            if snipe_type == "quick":
                Sniper.quick_snipe()
            elif snipe_type == "normal":
                Sniper.normal_snipe()
            elif snipe_type == "custom":
                Sniper.custom_snipe()
            else:
                Sniper.safe_snipe()

dispatcher = KeyDispatcher()
keymap = {}
key_states = {}
kboard = Controller()

#variables
version = "0.7"
debug = False
running = False
infinite = False
timer = QTimer()
timer.setSingleShot(True)
x, y, pixel_x, pixel_y = None, None, None, None
delay_config = {
    "initial_delay": 1,
    "quick_click_delay": 0.3,
    "auction_check_delay": 1.2,
    "short_wait_delay": 5,
    "long_wait_delay": 10,
    "safe_delay": 1,
    "end_delay": 0.5,
    "auction_pixel_x": pixel_x,
    "auction_pixel_y": pixel_y,
    "buyout_pixel_x": x,
    "buyout_pixel_y": y
}
snipe_type = "safe"
if debug:
    defaults = [1, 0.3, 1.2, 5, 10, 1, 0.5, 0, 0, 0, 0]
else:
    Logic.calculate_pixel_coords()
    defaults = [1, 0.3, 1.2, 5, 10, 1, 0.5, pixel_x, pixel_y, x, y]

#layouts and windows
app = QApplication([])
window = QWidget()
parent_layout = QVBoxLayout()
parent_layout.setContentsMargins(0, 0, 0, 0)
parent_layout.setSpacing(0)
main_layout = QVBoxLayout()
main_layout.setContentsMargins(0, 0, 0, 0)
button_layout = QHBoxLayout()
button_layout.setContentsMargins(8, 8, 8, 8)
button_layout.setSpacing(8)
topbar_layout = QHBoxLayout()
topbar_layout.setContentsMargins(6, 6, 6, 6)
topbar_layout.setSpacing(4)
midbtn_layout = QVBoxLayout()
midbtn_layout.setContentsMargins(0, 0, 0, 0)
midbtn_layout.setSpacing(8)
window.setFixedSize(400, 500)
window.setLayout(parent_layout)
window.setWindowFlags(Qt.FramelessWindowHint)
window.setAttribute(Qt.WA_TranslucentBackground)
window.setStyleSheet("border-radius: 4px")
parent_frame = QFrame()
parent_frame.setStyleSheet("background-color: #1a181d")
button_frame = QFrame()
topbar_frame = QFrame()
topbar_frame.setStyleSheet("background-color: #232029")
midbtn_frame = QFrame()

#styles
button_style_unfocused = """
QPushButton {
    border: none;
    background-color: #925cf2;
    color: white;
    padding: 8px;
    font-size: 14px;
    border-radius: 4px;
}
QPushButton:hover {
    background-color: #4d3676;
}
"""
button_style_focused = """
QPushButton {
    border: none;
    background-color: #4d3676;
    color: white;
    padding: 8px;
    font-size: 14px;
    border-radius: 4px;
}
QPushButton:hover {
    background-color: #63429a;
}
"""
button_style_disabled = """
QPushButton {
    border: none;
    background-color: #444444;
    color: white;
    padding: 8px;
    font-size: 14px;
    border-radius: 4px;
}
"""
title_text_style = """
    color: #ffffff;
    font-size: 12pt;
    margin: 0px;
    padding: 0px
"""
text_style = """
    color: #ffffff;
    font-size: 10pt;
    margin: 0px;
    padding: 0px
"""

#widgets
start_btn = QPushButton("Start (S)")
start_btn.setStyleSheet(button_style_unfocused)
quit_btn = QPushButton("Quit (Q)")
quit_btn.setStyleSheet(button_style_unfocused)
inf_btn = QPushButton("Infinite sniping")
inf_btn.setStyleSheet(button_style_unfocused)
safe_btn = QPushButton("Safe sniping")
safe_btn.setStyleSheet(button_style_focused)
normal_btn = QPushButton("Normal sniping")
normal_btn.setStyleSheet(button_style_unfocused)
custom_btn = QPushButton("Custom sniping")
custom_btn.setStyleSheet(button_style_unfocused)
quick_btn = QPushButton("Quick sniping")
quick_btn.setStyleSheet(button_style_unfocused)
state_buttons = [inf_btn, safe_btn, normal_btn, custom_btn, quick_btn]

main_txt = QLabel("FH5 Auction Bot")
main_txt.setStyleSheet(title_text_style)
debug_txt = QLabel("Debug on")
debug_txt.setStyleSheet(text_style)
debug_txt.setAlignment(Qt.AlignCenter)
message_txt = QLabel()
message_txt.setStyleSheet(text_style)
message_txt.setMaximumWidth(250)
message_txt.setWordWrap(True)
message_txt.setAlignment(Qt.AlignCenter)

#adding widgets
parent_layout.addWidget(parent_frame)
parent_frame.setLayout(main_layout)
main_layout.addWidget(topbar_frame, alignment=Qt.AlignTop)
topbar_frame.setLayout(topbar_layout)
topbar_layout.addWidget(main_txt, alignment=Qt.AlignCenter)
main_layout.addWidget(midbtn_frame, alignment=Qt.AlignCenter)
midbtn_frame.setLayout(midbtn_layout)
if debug:
    midbtn_layout.addWidget(debug_txt)
midbtn_layout.addWidget(inf_btn)
midbtn_layout.addWidget(safe_btn)
midbtn_layout.addWidget(normal_btn)
midbtn_layout.addWidget(custom_btn)
midbtn_layout.addWidget(quick_btn)
midbtn_layout.addWidget(message_txt)
main_layout.addWidget(button_frame, alignment=Qt.AlignBottom)
button_frame.setLayout(button_layout)
button_layout.addWidget(quit_btn)
button_layout.addWidget(start_btn)

#window moving
drag_pos = {"pos": None}
topbar_frame.setCursor(Qt.OpenHandCursor)
topbar_frame.mousePressEvent = Logic.mousePressEvent
topbar_frame.mouseMoveEvent = Logic.mouseMoveEvent
topbar_frame.mouseReleaseEvent = Logic.mouseReleaseEvent

dispatcher.key_released.connect(Logic.handle_keybind)
Thread(target=Logic.start_key_listener, daemon=True).start()

#binds
start_btn.clicked.connect(Logic.start)
quit_btn.clicked.connect(Logic.quit)
inf_btn.clicked.connect(Logic.infinite_snipe)
safe_btn.clicked.connect(Logic.safe)
normal_btn.clicked.connect(Logic.normal)
custom_btn.clicked.connect(Logic.custom)
quick_btn.clicked.connect(Logic.quick)
Logic.bind_key("s", Logic.start)
Logic.bind_key("q", Logic.quit)
window.show()
app.exec_()
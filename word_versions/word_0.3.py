from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QLabel
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
from pyautogui import position, screenshot
from json import load, dump
from os import path
from time import sleep
from pynput import keyboard
from pynput.keyboard import Controller, Key
from threading import Thread
import sys

class KeyDispatcher(QObject):
    key_released = pyqtSignal(str)

dispatcher = KeyDispatcher()
keymap = {}
key_states = {}
kboard = Controller()

#variables
running = False
checking_coords = False
timer = QTimer()
timer.setSingleShot(True)

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
inf_btn = QPushButton("Infinite sniping (I)")
inf_btn.setStyleSheet(button_style_unfocused)
coord_btn = QPushButton("Pick coordinates")
coord_btn.setStyleSheet(button_style_unfocused)

main_txt = QLabel("FH5 Auction Bot")
main_txt.setStyleSheet(title_text_style)
coord_txt = QLabel("Waiting for coords...")
coord_txt.setStyleSheet(text_style)
coord_txt.setMaximumWidth(250)
coord_txt.setWordWrap(True)
coord_txt.setAlignment(Qt.AlignCenter)
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
midbtn_layout.addWidget(inf_btn)
midbtn_layout.addWidget(coord_btn)
midbtn_layout.addWidget(coord_txt)
midbtn_layout.addWidget(message_txt)
main_layout.addWidget(button_frame, alignment=Qt.AlignBottom)
button_frame.setLayout(button_layout)
button_layout.addWidget(quit_btn)
button_layout.addWidget(start_btn)

#window moving
drag_pos = {"pos": None}

def mousePressEvent(event):
    if event.button() == Qt.LeftButton:
        drag_pos["pos"] = event.globalPos() - window.frameGeometry().topLeft()

def mouseMoveEvent(event):
    if drag_pos["pos"]:
        window.move(event.globalPos() - drag_pos["pos"])

def mouseReleaseEvent(_):
    drag_pos["pos"] = None

topbar_frame.setCursor(Qt.OpenHandCursor)
topbar_frame.mousePressEvent = mousePressEvent
topbar_frame.mouseMoveEvent = mouseMoveEvent
topbar_frame.mouseReleaseEvent = mouseReleaseEvent

#functions
def start():
    global running
    if running:
        start_btn.setStyleSheet(button_style_unfocused)
        start_btn.setText("Start (S)")
        inf_btn.setEnabled(True)
        if infinite:
            inf_btn.setStyleSheet(button_style_focused)
        else:
            inf_btn.setStyleSheet(button_style_unfocused)
        inf_btn.setText("Infinite sniping (I)")
        message("", False)
        running = False
    else:
        start_btn.setStyleSheet(button_style_focused)
        start_btn.setText("Stop (S)")
        inf_btn.setEnabled(False)
        inf_btn.setStyleSheet(button_style_disabled)
        inf_btn.setText("Infinite sniping (disabled)")
        if infinite:
            message("Looking for auctions...", True)
        else:
            message("Looking for auctions...", False)
        running = True
        Thread(target=background_loop, daemon=True).start()

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
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    listener.join()

def handle_keybind(char):
    func = keymap.get(char.lower())
    if func:
        func()

def quit():
    app.quit()
    sys.exit()

def infinite_snipe():
    global infinite
    if infinite:
        inf_btn.setStyleSheet(button_style_unfocused)
        inf_btn.setText("Infinite sniping (I)")
        settings["infinite"] = False
        infinite = False
    else:
        inf_btn.setStyleSheet(button_style_focused)
        inf_btn.setText("Infinite sniping (I)")
        settings["infinite"] = True
        infinite = True
    try:
        with open(settings_path, "w") as f:
            dump(settings, f, indent=4)
            if infinite:
                message("Infinite sniping on\nSetting saved", True)
            else:
                message("Infinite sniping off\nSetting saved", True)
    except Exception:
        if infinite:
            message("Infinite sniping on\nUnable to save setting", True)
        else:
            message("Infinite sniping off\nUnable to save setting", True)

def start_coords():
    global checking_coords
    message("Find position of an active listing and press P", False)
    coord_btn.setStyleSheet(button_style_focused)
    checking_coords = True

def find_coords():
    global pixel_x, pixel_y, checking_coords, settings
    if checking_coords:
        pixel_x, pixel_y = position()
        coord_txt.setText(f"Checking: {pixel_x}, {pixel_y}")
        settings["pixel_x"], settings["pixel_y"] = pixel_x, pixel_y
        coord_btn.setStyleSheet(button_style_unfocused)
        try:
            with open(settings_path, "w") as f:
                dump(settings, f, indent=4)
            message("Coords saved", True)
        except Exception:
            message("Unable to save coords", True)

        checking_coords = False

def message(text, timed):
    timer.stop()
    try:
        timer.timeout.disconnect()
    except TypeError:
        pass
    if timed:
        message_txt.setText(text)
        timer.timeout.connect(clear_msg)
        timer.start(3000)
    else:
        message_txt.setText(text)

def clear_msg():
    message("", False)

def get_app_dir():
    if getattr(sys, 'frozen', False):
        return path.dirname(sys.executable)
    else:
        return path.dirname(path.abspath(__file__))

def background_loop():
    while running:
        snipe()
    sleep(0.5)

def snipe():
    global running
    sleep(1)
    kboard.tap(Key.enter)
    sleep(0.3)
    kboard.tap(Key.enter)
    sleep(1.2)

    r, g, b = screenshot().getpixel((pixel_x, pixel_y))
    if r >= 245 and g >= 245 and b >= 245:
        kboard.tap("y")
        sleep(0.3)
        kboard.tap(Key.down)
        sleep(0.3)
        kboard.tap(Key.enter)
        sleep(0.3)
        kboard.tap(Key.enter)
        sleep(5)
        if infinite:
            kboard.tap(Key.enter)
            sleep(1)
            kboard.tap(Key.enter)
            sleep(10)
            kboard.tap(Key.enter)
            sleep(1)
            kboard.tap(Key.esc)
            sleep(1)
            kboard.tap(Key.esc)
            message("Car collected", True)
        else:
            kboard.tap(Key.enter)
            sleep(1)
            kboard.tap(Key.enter)
            sleep(10)
            kboard.tap(Key.enter)
            sleep(1)
            kboard.tap(Key.esc)
            sleep(1)
            kboard.tap(Key.esc)
            message("Auction finished", False)
            running = False
            start_btn.setStyleSheet(button_style_unfocused)
            inf_btn.setEnabled(True)
            if infinite:
                inf_btn.setStyleSheet(button_style_focused)
            else:
                inf_btn.setStyleSheet(button_style_unfocused)
            inf_btn.setText("Infinite sniping (I)")
    else:
        kboard.tap(Key.esc)
        sleep(0.3)

#settings load
settings_path = path.join(get_app_dir(), "settings.json")
try:
    with open(settings_path, "r") as f:
        settings = load(f)
        if all((settings["pixel_x"], settings["pixel_y"])):
            pixel_x, pixel_y = settings["pixel_x"], settings["pixel_y"]
            coord_txt.setText(f"Checking: {pixel_x}, {pixel_y}")
        else:
            pixel_x, pixel_y = None, None
        if settings["infinite"]:
            infinite = True
            inf_btn.setStyleSheet(button_style_focused)
        else:
            infinite = False
except FileNotFoundError:
    settings = {
        "pixel_x": None,
        "pixel_y": None,
        "infinite": False
    }
    pixel_x, pixel_y = None, None
    infinite = False
dispatcher.key_released.connect(handle_keybind)
Thread(target=start_key_listener, daemon=True).start()

#binds
start_btn.clicked.connect(start)
quit_btn.clicked.connect(quit)
inf_btn.clicked.connect(infinite_snipe)
coord_btn.clicked.connect(start_coords)
bind_key("s", start)
bind_key("q", quit)
bind_key("i", infinite_snipe)
bind_key("p", find_coords)
window.show()
app.exec_()
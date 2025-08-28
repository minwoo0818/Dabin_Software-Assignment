from pynput import mouse

def on_click(x, y, button, pressed):
    if pressed:
        print(f'마우스 클릭 좌표: ({x}, {y})')

with mouse.Listener(on_click=on_click) as listener:
    listener.join()
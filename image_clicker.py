import pyautogui
import time
import sys
import os

def find_and_click_image(image_path, confidence=0.8):
    """
    Find an image on the screen and click it if found.

    :param image_path: The file path of the image to search for.
    :param confidence: The confidence level for image matching (default is 0.8).
    """
    while True:
        try:
            # Search for the image on the screen
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)

            if location:
                # If found, get the center of the image
                center = pyautogui.center(location)

                # Move the mouse to the center of the image and click
                pyautogui.moveTo(center)
                pyautogui.click()
                print(f"Clicked on the image at {center}.")

        except pyautogui.ImageNotFoundException:
            print("Image not found. Retrying...")

        # Add a short delay to avoid excessive CPU usage
        time.sleep(1)

if getattr(sys, 'frozen', False):
    # If the script is run as a bundled executable (e.g., PyInstaller)
    image_path = os.path.join(sys._MEIPASS, "target.jpg")
else:
    # If the script is run as a regular Python script
    image_path = "target.jpg"

if __name__ == "__main__":
    # Start searching for the image and click when found
    find_and_click_image(image_path)

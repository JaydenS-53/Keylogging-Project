from pynput import keyboard
import time
import cv2


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
    # Deletes the variable so that webcam becomes unlocked (cleans up after itself)
    del webcam


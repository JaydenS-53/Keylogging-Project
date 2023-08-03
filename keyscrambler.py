from pynput import keyboard
from cryptography.fernet import Fernet

# Generate a random encryption key
enc_key = Fernet.generate_key()
# Create an instance of the Fernet cipher using the encryption key
cipher = Fernet(enc_key)


# function to encrypt the keystrokes using the fernet key
def encrypt_keystrokes(key):
    # Check if the key is a printable character
    if hasattr(key, 'char'):
        char = key.char
        # Convert the character to bytes
        plaintext = char.encode()
        # Encrypt the keystroke using the Fernet cipher
        encrypted_keystroke = cipher.encrypt(plaintext)
        # Print the encrypted keystroke
        print("Keystroke = " + encrypted_keystroke.decode(), end='\n', flush=True)


# when a key is pressed, run the encryption algorithm
def on_press(key):
    # Encrypt the keystroke
    encrypt_keystrokes(key)


# when the key is released stop the listener
def on_release(key):
    # Stop the listener when the Escape key is pressed
    if key == keyboard.Key.esc:
        return False


# Start the listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("Encrypting keystrokes.")
    listener.join()

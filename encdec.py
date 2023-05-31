import sys
from cryptography.fernet import Fernet
from pathlib import Path
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename

gui = Tk()

key_grabber = Path("./cryptkey.key")
playlist_file = Path("./playlist.json")

if key_grabber.is_file():
    with open('cryptkey.key', 'rb') as cryptkey:
        key = cryptkey.read()
    fernet = Fernet(key)
else:
    sys.exit()

print("Please select an output file to encrypt.")
gui.geometry("800x600")
gui.title("Spotify Valence and Arousal Tool - Encrypt/Decrypt Files")
input()
# output_file = Path(askopenfilename())
# print(output_file)
# sys.exit()
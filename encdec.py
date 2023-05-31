import sys
from cryptography.fernet import Fernet
from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import askopenfilename

key_grabber = Path("./cryptkey.key")
playlist_file = Path("./playlist.json")

if key_grabber.is_file():
    with open('cryptkey.key', 'rb') as cryptkey:
        key = cryptkey.read()
    fernet = Fernet(key)
else:
    sys.exit()

print("Please select an output file to encrypt.")
Tk().withdraw()
output_file = Path(askopenfilename())
print(output_file)
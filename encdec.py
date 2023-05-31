import sys
from cryptography.fernet import Fernet
from pathlib import Path
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename

gui = Tk()

key_grabber = Path("./cryptkey.key")
output_file = None
playlist_file = Path("./playlist.json")

def select_output():
    global output_file
    output_file = Path(askopenfilename())

if key_grabber.is_file():
    with open('cryptkey.key', 'rb') as cryptkey:
        key = cryptkey.read()
    fernet = Fernet(key)
else:
    key = Fernet.generate_key()
    with open('cryptkey.key', 'wb') as cryptkey:
        cryptkey.write(key)
    fernet = Fernet(key)

gui.geometry("600x300")
gui.title("Spotify Valence and Arousal Tool - Encrypt/Decrypt Files")

outer_box = ttk.Frame(gui, padding="3 3 12 12")
outer_box.grid(column=0, row=0, sticky=(N, W, E, S))
gui.columnconfigure(0, weight=1)
gui.rowconfigure(0, weight=1)

ttk.Label(outer_box, text="Select your playlist output file.").grid(column=1, row=1, sticky=W)
output_path_select = ttk.Button(outer_box, text="Choose a file.", command=select_output, width=7)
output_path_select.grid(column=1, row=2, sticky=(W, E))
input()
print(output_file)
# output_file = Path(askopenfilename())
# print(output_file)
# sys.exit()
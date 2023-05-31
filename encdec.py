import sys
from cryptography.fernet import Fernet
from pathlib import Path
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename

gui = Tk()

key_grabber = Path("./cryptkey.key")
output_file = None
playlist_file = None

def select_output():
    global output_file
    output_file = Path(askopenfilename())
def select_playlist():
    global playlist_file
    playlist_file = Path(askopenfilename())
def encrypt_output():
    if output_file.is_file():
        with open(output_file, "rb") as file:
            original = file.read()
        encrypt_data = fernet.encrypt(original)
        with open(output_file, "wb") as encrypted_file:
            encrypted_file.write(encrypt_data)
    else:
        # Throw a popup or something
        sys.exit()
def decrypt_output():
    if output_file.is_file():
        with open(output_file, "rb") as encrypted_file:
            encrypted = encrypted_file.read()
        decrypted = fernet.decrypt(encrypted)
        with open(output_file, "wb") as decrypted_output_data:
            decrypted_output_data.write(decrypted)
def encrypt_playlist():
    if playlist_file.is_file():
        with open(playlist_file, "rb") as file:
            original = file.read()
        encrypt_data = fernet.encrypt(original)
        with open(playlist_file, "wb") as encrypted_file:
            encrypted_file.write(encrypt_data)
    else:
        # Throw a popup or something
        sys.exit()
def decrypt_playlist():
    if playlist_file.is_file():
        with open(playlist_file, "rb") as encrypted_file:
            encrypted = encrypted_file.read()
        decrypted = fernet.decrypt(encrypted)
        with open(playlist_file, "wb") as decrypted_playlist_data:
            decrypted_playlist_data.write(decrypted)

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

# Output file encrypt/decrypt
ttk.Label(outer_box, text="Select your songs output file.").grid(column=1, row=1, sticky=W)
output_path_select = ttk.Button(outer_box, text="Choose a file.", command=select_output, width=7)
output_path_select.grid(column=1, row=2, sticky=(W, E))
encrypt_output_button = ttk.Button(outer_box, text="ENCRYPT", command=encrypt_output, width=7)
encrypt_output_button.grid(column=1, row=3, sticky=(W, E))
decrypt_output_button = ttk.Button(outer_box, text="DECRYPT", command=decrypt_output, width=7)
decrypt_output_button.grid(column=1, row=4, sticky=(W, E))

# Playlist file encrypt/decrypt
ttk.Label(outer_box, text="Select your playlist output file.").grid(column=2, row=1, sticky=W)
playlist_path_select = ttk.Button(outer_box, text="Choose a file.", command=select_playlist, width=7)
playlist_path_select.grid(column=2, row=2, sticky=(W, E))
encrypt_playlist_button = ttk.Button(outer_box, text="ENCRYPT", command=encrypt_playlist, width=7)
encrypt_playlist_button.grid(column=2, row=3, sticky=(W, E))
decrypt_playlist_button = ttk.Button(outer_box, text="DECRYPT", command=decrypt_playlist, width=7)
decrypt_playlist_button.grid(column=2, row=4, sticky=(W, E))

input()
print(output_file)
print(playlist_file)
# output_file = Path(askopenfilename())
# print(output_file)
# sys.exit()
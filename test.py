import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import os
from decouple import config
import pprint

os.environ["SPOTIPY_CLIENT_ID"] = config("ID")
os.environ["SPOTIPY_CLIENT_SECRET"] = config("SECRET")
os.environ["SPOTIPY_REDIRECT_URI"] = config("URI")

yes = ["Y", "y"]
no = ["N", "n"]

def gather_data():
    gather_q = ""
    while gather_q not in yes or no:
        gather_q = input("Gather user data? Y/N ")
        if gather_q in yes:
            username = input("Enter username: ")
            client_credentials_manager = SpotifyClientCredentials()
            sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
            user = sp.user(username)
            pprint.pprint(user)
            break
        elif gather_q in no:
            print("Proceeding.")
            break
        else:
            print("Command not recognised.")
gather_data()

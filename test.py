import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import os
from decouple import config
import pprint

os.environ["SPOTIPY_CLIENT_ID"] = config("ID")
os.environ["SPOTIPY_CLIENT_SECRET"] = config("SECRET")
os.environ["SPOTIPY_REDIRECT_URI"] = config("URI")

username = input("Enter username: ")

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
user = sp.user(username)
pprint.pprint(user)
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import os
from decouple import config
import pprint
import sys
os.environ["SPOTIPY_CLIENT_ID"] = config("ID")
os.environ["SPOTIPY_CLIENT_SECRET"] = config("SECRET")
os.environ["SPOTIPY_REDIRECT_URI"] = config("URI")

yes = ["Y", "y"]
no = ["N", "n"]

username = input("Enter username: ")
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, auth_manager=SpotifyOAuth())
user = sp.user(username)

def gather_data():
    gather_q = ""
    while gather_q not in yes or no:
        gather_q = input("Gather user data? Y/N ")
        print("---------------------")
        if gather_q in yes:
            pprint.pprint(user)
            break
        elif gather_q in no:
            print("Proceeding.")
            break
        else:
            print("Command not recognised.")
def retrieve_playlist():
    retrieve_list = ""
    while retrieve_list not in yes or no:
        retrieve_list = input("Gather playlist data? Y/N ")
        print("---------------------")
        if retrieve_list in yes:
            playlists = sp.user_playlists(username)
            for playlist in playlists['items']:
                print(playlist['name'])
            break
        elif retrieve_list in no:
            print("Exiting.")
            sys.exit()
        else:
            print("Command not recognised.")

gather_data()
print("---------------------")
retrieve_playlist()
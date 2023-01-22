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
scope = "user-top-read, user-read-currently-playing"
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, auth_manager=SpotifyOAuth(scope=scope))
user = sp.user(username)

playback = sp.current_user_playing_track()
pprint.pprint("Currently listening to: '" + playback["item"]["name"] + "' by " + playback["item"]["artists"][0]["name"] + ".")

def gather_data():
    gather_q = ""
    while gather_q not in yes or no:
        gather_q = input("Gather user data? Y/N ")
        print("---------------------")
        if gather_q in yes:
            pprint.pprint(user)
            print("---------------------")
            print("TOP ARTISTS FOR CURRENT USER")
            print("---------------------")
            top_artist_results = sp.current_user_top_artists(limit=10)
            for i, item in enumerate(top_artist_results["items"]):
                print(i, item["name"])
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
            print("Proceeding.")
            # sys.exit()
            break
        else:
            print("Command not recognised.")

gather_data()
print("---------------------")
retrieve_playlist()

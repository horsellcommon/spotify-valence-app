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

def current_valence_arousal():
    ### POSITIVE
    if current_song_features[0]["valence"] > 0.75 and current_song_features[0]["energy"] > 0.75:
        print(f"This song has very high valence and very high arousal.")
    elif current_song_features[0]["valence"] > 0.75 and current_song_features[0]["energy"] > 0.5:
        print(f"This song has very high valence and positive arousal.")
    elif current_song_features[0]["valence"] > 0.5 and current_song_features[0]["energy"] > 0.5:
        print("This song has both positive valence and arousal.")
    ### AVERAGE HERE OR BOTH POS/NEG VALENCE/AROUSAL
    elif current_song_features[0]["valence"] > 0.75 and current_song_features[0]["energy"] < 0.25:
        print("This song has very high valence but very negative arousal.")
    elif current_song_features[0]["valence"] > 0.75 and current_song_features[0]["energy"] < 0.5:
        print("This song has very high valence but negative arousal.")
    elif current_song_features[0]["valence"] > 0.5 and current_song_features[0]["energy"] > 0.5:
        print("This song has positive valence but negative arousal.")
    elif current_song_features[0]["valence"] < 0.25 and current_song_features[0]["energy"] > 0.75:
        print("This song has very high arousal but very low valence.")
    elif current_song_features[0]["valence"] < 0.5 and current_song_features[0]["energy"] > 0.75:
        print("This song has very high arousal but negative valence.")
    elif current_song_features[0]["valence"] < 0.5 and current_song_features[0]["energy"] > 0.5:
        print("This song has positive arousal but negative valence.")
    ### NEGATIVE
    elif current_song_features[0]["valence"] < 0.25 and current_song_features[0]["energy"] > 0.25:
        print(f"This song has very negative valence and very negative arousal.")
    elif current_song_features[0]["valence"] < 0.25 and current_song_features[0]["energy"] > 0.5:
        print(f"This song has very negative valence and negative arousal.")
    elif current_song_features[0]["valence"] < 0.5 and current_song_features[0]["energy"] > 0.5:
        print(f"This song has negative valence and arousal.")
    else:
        print("No valence/energy data available for some reason.")

#### Gather user info - display name & follower count
def gather_data():
    gather_q = ""
    while gather_q not in yes or no:
        gather_q = input("Gather user data? Y/N ")
        print("---------------------")
        if gather_q in yes:
            pprint.pprint("Display Name: " + user["display_name"])
            pprint.pprint("Followers: " + str(user["followers"]["total"]))
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

#### Gather Playlists
def retrieve_playlist():
    retrieve_list = ""
    while retrieve_list not in yes or no:
        retrieve_list = input("Gather playlist data? Y/N ")
        print("---------------------")
        if retrieve_list in yes:
            playlists = sp.user_playlists(username, limit=10) # Limit to 10 latest playlists
            listed = []
            for playlist in playlists['items']:
                listed.append(playlist)
            #pprint.pprint(listed) # Have all playlist metadata now, including URI
            # Now enumerate and allow for selection?
            for i, item in enumerate(playlists["items"]): # Number them all!!!!
                print(i, item["name"])
            
            # input, and if input correlates to this playlist number then display song name, artist and valence/energy/key results of each track
            selected_playlist = input("Input a playlist number for more details: ")
            if selected_playlist == "0":
                # pprint.pprint(listed[0])
                playlist_uri = sp.playlist(listed[0]["uri"])
                pprint.pprint(playlist_uri) # Well done

            else:
                print("FUCK")
            break
        elif retrieve_list in no:
            print("Proceeding.")
            # sys.exit()
            break
        else:
            print("Command not recognised.")

yes = ["Y", "y"]
no = ["N", "n"]

username = input("Enter username: ")
scope = "user-top-read, user-read-currently-playing"
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, auth_manager=SpotifyOAuth(scope=scope))
user = sp.user(username)

playback = sp.current_user_playing_track()
print("---------------------")
pprint.pprint("Currently listening to: '" + playback["item"]["name"] + "' by " + playback["item"]["artists"][0]["name"] + ".")
# Add valence of currently playing track.
# pprint.pprint(playback["item"]["uri"])
current_song_features = sp.audio_features(playback["item"]["uri"])
print("Song valence: " + str(current_song_features[0]["valence"]))
print("Song arousal: " + str(current_song_features[0]["energy"]))
current_valence_arousal()
print(">>> SONG KEY may influence effect of valence on mood. <<<")
print("Key: " + str(current_song_features[0]["key"]))
# Figure out Spotify's ridiculous way of presenting key. Is 1 C??? Is 4 Eb or E?
# Find out whether major/minor is available, valence can not be relied on for key.
# If all else fails then make best guess based on valence levels? Over 0.75 most probably maj and under 0.25 most probably min

print("---------------------")
gather_data()
print("---------------------")
retrieve_playlist()
print("---------------------")

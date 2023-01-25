import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import os
from decouple import config
import pprint
import json
from pathlib import Path
os.environ["SPOTIPY_CLIENT_ID"] = config("ID")
os.environ["SPOTIPY_CLIENT_SECRET"] = config("SECRET")
os.environ["SPOTIPY_REDIRECT_URI"] = config("URI")

scope = "user-top-read, user-read-currently-playing"
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, auth_manager=SpotifyOAuth(scope=scope))

yes = ["Y", "y"]
no = ["N", "n"]
json_exist = False
path = Path("./output.json")
if path.is_file() == True:
    json_exist = True

class Song:
    def __init__(self, title, artist, valence, arousal):
        self.title = title
        self.artist = artist
        self.valence = valence
        self.arousal = arousal   

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
    elif current_song_features[0]["valence"] > 0.5 and current_song_features[0]["energy"] < 0.5:
        print("This song has negative arousal but positive valence.")
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

            # No need for top artists for current user at the moment?

            # print("---------------------")
            # print("TOP ARTISTS FOR CURRENT USER")
            # print("---------------------")
            # top_artist_results = sp.current_user_top_artists(limit=10)
            # for i, item in enumerate(top_artist_results["items"]):
            #     print(i, item["name"])
            break
        elif gather_q in no:
            print("Proceeding.")
            break
        else:
            print("Command not recognised.")

#### Gather Playlists
def retrieve_playlist():
    global json_exist
    retrieve_list = ""
    while retrieve_list not in yes or no:
        retrieve_list = input("Gather playlist data? Y/N ")
        print("---------------------")
        if retrieve_list in yes:
            playlists = sp.user_playlists(username)
            listed = []
            for playlist in playlists['items']:
                listed.append(playlist)
            for i, item in enumerate(playlists["items"]):
                print(i, item["name"])
            print("---------------------")
            selected_playlist = int(input("Input a playlist number for more details: "))
            print("---------------------")
            if selected_playlist < len(listed) +1:
                playlist_uri = listed[selected_playlist]["uri"]
                more_details = sp.playlist_items(playlist_uri, fields=None, offset=0, market=None, additional_types=('track', 'episode'))

                # ENUMERATOR
                track_enumerator = sp.playlist_tracks(playlist_uri, fields=None, limit=40, offset=0, market=None, additional_types=('track', )) # Limited to 39 because selecting anything above 39 causes an error
                track_names = []
                for i in range(len(track_enumerator["items"])): # Loops through and appends to track_names
                    track_names.append(track_enumerator["items"][i]["track"]["name"])
                numbered_names = enumerate(track_names)
                pprint.pprint(list(numbered_names))

                # SELECTOR, WORKS
                print("---------------------")
                track_selector = int(input("Select a track for more details: "))
                if track_selector < len(playlist_uri) + 1:
                    # pprint.pprint(more_details["items"][track_selector]["track"])
                    print("--------------------")
                    print("You have chosen '" + more_details["items"][track_selector]["track"]["name"] + "' by " + more_details["items"][track_selector]["track"]["artists"][0]["name"] + ".")
                    get_features = sp.audio_features(more_details["items"][track_selector]["track"]["uri"])
                    print("Song valence: " + str(get_features[0]["valence"]))
                    print("Song arousal: " + str(get_features[0]["energy"]))
                    print("Key: " + str(get_features[0]["key"]))
                    print("--------------------")

                    ###### WORK ON THIS
                    save_q = input("Save song valence/arousal? Y/N ")
                    if save_q in yes and json_exist == True:
                        artist_list = [more_details["items"][track_selector]["track"]["name"], more_details["items"][track_selector]["track"]["artists"][0]["name"], get_features[0]["valence"], get_features[0]["energy"]]
                        make_it = Song(artist_list[0], artist_list[1], artist_list[2], artist_list[3])
                        dump_it = json.dumps(make_it.__dict__)
                        with open("output.json", "a") as json_file:
                            json.dump(dump_it, json_file)
                            json_file.write("\n")
                    elif save_q in yes:
                        artist_list = [more_details["items"][track_selector]["track"]["name"], more_details["items"][track_selector]["track"]["artists"][0]["name"], get_features[0]["valence"], get_features[0]["energy"]]
                        make_it = Song(artist_list[0], artist_list[1], artist_list[2], artist_list[3])
                        dump_it = json.dumps(make_it.__dict__)
                        print(dump_it)
                        with open("output.json", "w") as json_file:
                            json.dump(dump_it, json_file)
                            json_file.write("\n")
                        json_exist = True
                        retrieve_playlist()
                    else:
                        break
                else:
                    print("Incorrect track number selected.")

            else:
                print("Incorrect playlist number selected.")
            break
        elif retrieve_list in no:
            print("Proceeding.")
            break
        else:
            print("Command not recognised.")

listening_now = "" # Quick fix for if Spotify isn't running, will try to substitute with something that checks whether the user is listening rather than having manual input
while listening_now not in yes or no:
        listening_now = input("Are you listening to Spotify right now? Y/N ")
        if listening_now in yes:
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
            break
        elif listening_now in no:
            print("Proceeding.")
            break
        else:
            print("Command not recognised")

username = input("Enter username: ")
user = sp.user(username)

gather_data()
print("---------------------")
retrieve_playlist()
print("---------------------")

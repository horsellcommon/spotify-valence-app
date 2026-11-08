import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import os
import pprint
import json
from pathlib import Path
import sys
import linecache
from cryptography.fernet import Fernet
import requests

# Cool global variables and check to see if files already exist
yes = ["Y", "y"]
no = ["N", "n"]
current_song_exists = False

# Check for files
path = Path("./output.json")
path1 = Path("./playlist.json")
path2 = Path("./user.txt")
path3 = Path("./cryptkey.key")
        

if path3.is_file():
    with open('cryptkey.key', 'rb') as cryptkey:
        key = cryptkey.read()
    fernet = Fernet(key)
else:
    key = Fernet.generate_key()
    with open('cryptkey.key', 'wb') as cryptkey:
        cryptkey.write(key)
    fernet = Fernet(key)


class Song:
    def __init__(self, title, artist, valence, arousal, key):
        self.title = title
        self.artist = artist
        self.valence = valence
        self.arousal = arousal
        self.key = key

if path2.is_file():
    with open("user.txt", "rb") as encrypted_file:
        encrypted = encrypted_file.read()
    decrypted = fernet.decrypt(encrypted)
    with open("user.txt", "wb") as decrypted_user_data:
        decrypted_user_data.write(decrypted)
    
    os.environ["SPOTIPY_CLIENT_ID"] = linecache.getline(r"./user.txt", 1)
    os.environ["SPOTIPY_CLIENT_SECRET"] = linecache.getline(r"./user.txt", 2)
    os.environ["SPOTIPY_REDIRECT_URI"] = linecache.getline(r"./user.txt", 3)
    os.environ["NEW_API_KEY"] = linecache.getline(r"./user.txt", 4)

    with open("user.txt", "rb") as file:
        original = file.read()
    encrypt_user = fernet.encrypt(original)
    with open("user.txt", "wb") as encrypted_user_data:
        encrypted_user_data.write(encrypt_user)
else:
    os.environ["SPOTIPY_CLIENT_ID"] = input("Enter your Spotify Client ID: ")
    os.environ["SPOTIPY_CLIENT_SECRET"] = input("Enter your Spotify Secret ID: ")
    os.environ["SPOTIPY_REDIRECT_URI"] = input("Enter your Spotify Redirect URI: ")
    os.environ["NEW_API_KEY"] = input("Enter your new API key: ")
        
    with open("user.txt", "w") as user_data:
        user_data.write(os.environ["SPOTIPY_CLIENT_ID"] + "\n" + os.environ["SPOTIPY_CLIENT_SECRET"] + "\n" + os.environ["SPOTIPY_REDIRECT_URI"] + "\n" + os.environ["NEW_API_KEY"])
    with open("user.txt", "rb") as file:
        original = file.read()
    encrypt_user = fernet.encrypt(original)
    with open("user.txt", "wb") as encrypted_user_data:
        encrypted_user_data.write(encrypt_user)

# Spotipy stuff
scope = "user-top-read user-read-currently-playing"
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, auth_manager=SpotifyOAuth(scope=scope))
# New API testing
with path2.open("rb") as new_api:
    newapi = linecache.getline(r"./user.txt", 4).rstrip('\n') # fuck off linecache
# New requests testing - LOOK AT THIS SHIT https://freqblog.com/#docs
spnew = requests.get("https://api.freqblog.com/", headers={"X-Api-Key": newapi})
print(spnew.status_code)

#### Gather user info - display name & follower count
def gather_data():
    gather_q = ""
    while gather_q not in yes or no:
        gather_q = input("Gather user data? Y/N ")
        print("---------------------")
        if gather_q in yes:
            pprint.pprint("Display Name: " + user["display_name"])
            pprint.pprint("Followers: " + str(user["followers"]["total"]))
            break
        elif gather_q in no:
            print("Proceeding.")
            break
        else:
            print("Command not recognised.")

def get_audio_features(track):
    response = requests.get(
        "https://api.freqblog.com/lookup",
        headers={"X-Api-Key": newapi},
        params={"spotify_id": track["id"]},
        timeout=30
    )

    if response.status_code == 404:
        # Give it another go son
        response = requests.get(
            "https://api.freqblog.com/lookup",
            headers={"X-Api-Key": newapi},
            params={"track": track["name"],
                    "artist": track["artists"][0]["name"],
                    "wait": 20},
                    timeout=30
        )
    if response.status_code == 202:
        print("BE PATIENT.")
        return None
    if response.status_code == 404:
        print("Track unavailable.")
        return None
    response.raise_for_status()
    return response.json()

#### Gather Playlists
def retrieve_playlist():
    retrieve_list = ""
    while retrieve_list not in yes or no:
        retrieve_list = input("Gather playlist data? Y/N ")
        print("---------------------")
        if current_song_exists == True and retrieve_list in no and path.is_file() == False:
            with open("output.json", "w") as json_file:
                json_file.write("[" + "\n" + current_song_dumped + "\n" + "]")
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

                # ENUMERATOR + GATHER VALENCE/ENERGY OF ENTIRE PLAYLIST
                track_enumerator = sp.playlist_tracks(playlist_uri, fields=None, limit=40, offset=0, market=None, additional_types=('track', )) # Limited to 39 because selecting anything above 39 causes an error
                track_names = []
                track_uris = []                
                valences = []
                energy = []
                
                # FUCK IT. WE'RE DOING IT LIVE.
                playlist_exists = path1.is_file()
                playlist_objects = []

                for item in track_enumerator["items"]:
                    track = item.get("track")
                    if not track or not track.get("id"):
                        print("Skipping track due to missing ID.")
                        continue
                    features = get_audio_features(track)
                    if features is None:
                        print(f"Skipping track due to missing features.")
                        continue
                    if features.get("valence") is None or features.get("energy") is None:
                        print(f"Missing audio features for {track['name']}")
                        continue

                    track_names.append(track["name"])
                    track_uris.append(track["uri"])
                    valences.append(features["valence"])
                    energy.append(features["energy"])
                    

                    playlist_objects.append(
                        Song(
                            track["name"],
                            track["artists"][0]["name"],
                            features["valence"],
                            features["energy"],
                            features["key"]
                        ).__dict__
                    )
                if not playlist_exists:
                    with open("playlist.json", "w") as json_file:
                        json.dump(playlist_objects, json_file, indent=4)
                combination = [
                    track_names[i] + ". V: " + str(valences[i]) + ". A: " + str(energy[i]) + "."
                    for i in range(len(track_names))
                ]
                numbered_names = enumerate(combination)
                pprint.pprint(list(numbered_names))

                # SELECTOR, WORKS
                print("---------------------")
                track_selector = int(input("Select a track for more details: "))
                if track_selector < len(playlist_uri) + 1:
                    print("--------------------")
                    print("You have chosen '" + more_details["items"][track_selector]["track"]["name"] + "' by " + more_details["items"][track_selector]["track"]["artists"][0]["name"] + ".")
                    selected_track = more_details["items"][track_selector]["track"]
                    get_features = get_audio_features(selected_track)
                    if get_features is None:
                        print("Audio features unavailable.")
                        retrieve_playlist()
                        return
                    print("Song valence: " + str(get_features["valence"]))
                    print("Song arousal: " + str(get_features["energy"]))
                    print("Key: " + str(get_features.get("key", "Unavailable")))
                    print("--------------------")

                    ###### WORK ON THIS
                    save_q = input("Save song valence/arousal? Y/N ")
                    if save_q in yes and path.is_file():
                        final_input = input("Is this your final data entry? Y/N ")
                        if final_input in yes:
                            artist_list = [selected_track["name"], selected_track["artists"][0]["name"], get_features["valence"], get_features["energy"], get_features.get("key", "Unavailable")]
                            make_it = Song(artist_list[0], artist_list[1], artist_list[2], artist_list[3], artist_list[4])
                            dump_it = json.dumps(make_it.__dict__, indent=4, separators=(",", ": "))
                            print(dump_it)
                            if current_song_exists == True:
                                with open("output.json", "a") as json_file:
                                    json_file.write(dump_it + "," + "\n" + current_song_dumped + "\n" + "]")
                            else:
                                with open("output.json", "a") as json_file:
                                    json_file.write(dump_it + "\n" + "]")
                            # Final read and average of output file
                            open_file = open("output.json")
                            load_file = json.load(open_file)
                            valence_list = []
                            arousal_list = []
                            for valences in load_file:
                                valence_list.append(valences["valence"])
                            for energy in load_file:
                                arousal_list.append(energy["arousal"])
                            def Average(total):
                                return sum(total) / len(total)
                            call_average_valence = Average(valence_list)
                            call_average_energy = Average(arousal_list)
                            print("---------------------")
                            print("Averaging valence and energy/arousal of existing output file...")
                            print("Average Valence: ", call_average_valence)
                            print("Average energy/arousal: ", call_average_energy)
                            print("---------------------")
                            open_file.close()
                            sys.exit()
                        else:
                            artist_list = [selected_track["name"], selected_track["artists"][0]["name"], get_features["valence"], get_features["energy"], get_features.get("key", "Unavailable")]
                            make_it = Song(artist_list[0], artist_list[1], artist_list[2], artist_list[3], artist_list[4])
                            dump_it = json.dumps(make_it.__dict__, indent=4, separators=(",", ": "))
                            print(dump_it)
                            with open("output.json", "a") as json_file:
                                json_file.write(dump_it + "," + "\n")
                            retrieve_playlist()
                    elif save_q in yes:
                        artist_list = [selected_track["name"], selected_track["artists"][0]["name"], get_features["valence"], get_features["energy"], get_features.get("key", "Unavailable")]
                        make_it = Song(artist_list[0], artist_list[1], artist_list[2], artist_list[3], artist_list[4])
                        dump_it = json.dumps(make_it.__dict__, indent=4, separators=(",", ": "))
                        print(dump_it)
                        with open("output.json", "w") as json_file:
                            json_file.write("[" + "\n" + dump_it + "," + "\n")
                        retrieve_playlist()
                    else:
                        retrieve_playlist()
                else:
                    print("Incorrect track number selected.")
            else:
                print("Incorrect playlist number selected.")
        elif retrieve_list in no:
            sys.exit()
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
            response = requests.get(
                "https://api.freqblog.com/lookup",
                headers={"X-Api-Key": newapi},
                params={"track": playback["item"]["name"],
                        "artist": playback["item"]["artists"][0]["name"],
                        "wait": 20
                }
            )
            print(response.status_code)
            print(response.text)

            response.raise_for_status()  # Raise an exception if the request was unsuccessful
            current_song_features = response.json()
            print("Song valence: " + str(current_song_features["valence"]))
            print("Song arousal: " + str(current_song_features["energy"]))
            print(">>> SONG KEY may influence effect of valence on mood. <<<")
            print("Key: " + str(current_song_features.get("key", "Unavailable")))
            append_at_end = input("Add song to output file? Y/N ")
            if append_at_end in yes:
                current_song_object = Song(playback["item"]["name"], playback["item"]["artists"][0]["name"], current_song_features["valence"], current_song_features["energy"], current_song_features.get("key", "Unavailable"))
                current_song_dumped = json.dumps(current_song_object.__dict__, indent=4, separators=(",", ": "))
                print(current_song_dumped)
                current_song_exists = True
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

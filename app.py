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

# Better way to do this but cba changing it
yes = ["Y", "y"]
no = ["N", "n"]
current_song_exists = False
second_time_around = False
saved_song_records = []

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


def save_json_file(base_path, data):
    output_path = base_path
    file_number = 2
    while output_path.exists():
        output_path = base_path.with_name(
            f"{base_path.stem}_{file_number}{base_path.suffix}"
        )
        file_number += 1

    with output_path.open("w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Saved data to {output_path}.")
    return output_path


def save_song_record(song):
    global second_time_around

    record = song.__dict__
    save_json_file(path, [record])
    saved_song_records.append(record)
    second_time_around = True


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
with path2.open("rb") as new_api:
    newapi = linecache.getline(r"./user.txt", 4).rstrip('\n') # fuck off linecache

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

def raise_for_freqblog_unauthorized(response):
    if response.status_code == 401:
        error = response.json()
        error_code = error.get("error_code", "unknown")
        detail = error.get("detail", "The API key was rejected.")
        raise requests.HTTPError(
            f"Freqblog rejected the API key (401, {error_code}): {detail} "
            "Check that the saved API key is current and active.",
            response=response,
        )


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
    raise_for_freqblog_unauthorized(response)
    if response.status_code == 202:
        print("BE PATIENT.")
        return None
    if response.status_code == 404:
        print("Track unavailable.")
        return None
    response.raise_for_status()
    return response.json()

def get_audio_features_batch(tracks):
    features = []
    for start in range(0, len(tracks), 50):
        batch = tracks[start:start + 50]
        response = requests.post(
            "https://api.freqblog.com/bulk",
            headers={"X-Api-Key": newapi},
            json={
                "tracks": [
                    {
                        "track": track["name"],
                        "artist": track["artists"][0]["name"],
                    }
                    for track in batch
                ]
            },
            timeout=30,
        )
        raise_for_freqblog_unauthorized(response)
        response.raise_for_status()
        results = response.json()["results"]
        if len(results) != len(batch):
            raise ValueError(
                "Freqblog returned a different number of results than requested."
            )
        features.extend(
            result.get("result") if result.get("found") else None
            for result in results
        )
    return features

#### Gather Playlists
def retrieve_playlist():
    global second_time_around

    retrieve_list = ""
    while retrieve_list not in yes or no:
        retrieve_list = input("Gather playlist data? Y/N ")
        print("---------------------")
        if current_song_exists and retrieve_list in no:
            current_song_record = json.loads(current_song_dumped)
            save_json_file(path, [current_song_record])
            saved_song_records.append(current_song_record)
            second_time_around = True
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
            if 0 <= selected_playlist < len(listed):
                playlist_uri = listed[selected_playlist]["uri"]
                more_details = sp.playlist_items(
                    playlist_uri,
                    fields=None,
                    limit=100,
                    offset=0,
                    market=None,
                    additional_types=('track', 'episode'),
                )
                playlist_tracks = []
                while more_details:
                    playlist_tracks.extend(more_details["items"])
                    more_details = sp.next(more_details)
                tracks_to_lookup = []
                for item in playlist_tracks:
                    track = item.get("track")
                    if not track or not track.get("id"):
                        print("Skipping track due to missing ID.")
                    elif not track.get("artists"):
                        print(f"Skipping track with missing artist: {track['name']}")
                    else:
                        tracks_to_lookup.append(track)
                batch_features = get_audio_features_batch(tracks_to_lookup)
                analyzed_tracks = []
                
                # FUCK IT. WE'RE DOING IT LIVE.
                playlist_objects = []

                for track, features in zip(tracks_to_lookup, batch_features):
                    if features is None:
                        print(f"Skipping track due to missing features: {track['name']}")
                        continue
                    if features.get("valence") is None or features.get("energy") is None:
                        print(f"Missing audio features for {track['name']}")
                        continue

                    analyzed_tracks.append((track, features))

                    playlist_objects.append(
                        Song(
                            track["name"],
                            track["artists"][0]["name"],
                            features["valence"],
                            features["energy"],
                            features["key"]
                        ).__dict__
                    )
                save_json_file(path1, playlist_objects)
                combination = [
                    track["name"] + ". V: " + str(features["valence"])
                    + ". A: " + str(features["energy"]) + "."
                    for track, features in analyzed_tracks
                ]
                numbered_names = enumerate(combination)
                pprint.pprint(list(numbered_names))

                print("---------------------")
                track_selector = int(input("Select a track for more details: "))
                if 0 <= track_selector < len(analyzed_tracks):
                    print("--------------------")
                    selected_track, get_features = analyzed_tracks[track_selector]
                    print("You have chosen '" + selected_track["name"] + "' by " + selected_track["artists"][0]["name"] + ".")
                    print("Song valence: " + str(get_features["valence"]))
                    print("Song arousal: " + str(get_features["energy"]))
                    print("Key: " + str(get_features.get("key", "Unavailable")))
                    print("--------------------")

                    save_q = input("Save song valence/arousal? Y/N ")
                    if save_q in yes:
                        had_saved_song = second_time_around
                        make_it = Song(
                            selected_track["name"],
                            selected_track["artists"][0]["name"],
                            get_features["valence"],
                            get_features["energy"],
                            get_features.get("key", "Unavailable"),
                        )
                        print(json.dumps(make_it.__dict__, indent=4))
                        save_song_record(make_it)

                        if had_saved_song:
                            final_input = input("Is this your final data entry? Y/N ")
                            if final_input in yes:
                                valence_list = [
                                    record["valence"] for record in saved_song_records
                                ]
                                arousal_list = [
                                    record["arousal"] for record in saved_song_records
                                ]
                                print("---------------------")
                                print("Averaging saved song valence and energy/arousal...")
                                print("Average Valence: ", sum(valence_list) / len(valence_list))
                                print("Average energy/arousal: ", sum(arousal_list) / len(arousal_list))
                                print("---------------------")
                                sys.exit()
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

listening_now = ""
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

# Spotify Valence and Arousal Tool

A console-based program that gathers playlist metadata from the current user or a selected user.

# Usage and Requirements

You need what you needed last time, but with some extra steps! This app still uses Spotify's API for everything other than audio_features, so all of that still works!
- Head to the Spotify dev dashboard and create a new app, that'll give you your 'CLIENT_ID', 'CLIENT_SECRET', and your 'REDIRECT_URIs'.
- Set your 'REDIRECT URI' to 'http://127.0.0.1:PORT' (Any port will do so have fun with it)
- Once you've got that done, keep that page open because now we've got to do a big fucking detour over to 'https://freqblog.com/' because they've got the audio features we need! The whole point of the app isn't even available on Spotify anymore!
- Sign up for a free API key, you get like 1000 requests a month.
- After you've got that, you should be good to go. Keep all of that bullshit on hand because you're going to copy/paste it into this frankenapp momentarily.
- I'm not releasing an executable with this release just yet because I can't be bothered! So clone this repo and grab the dependencies then run 'app.py'. The standalone encryption thingimajig that comes with it ('encdec.py') didn't need an update so that still works as intended. There's a standalone repo for that which is a bit better than this bundled one somewhere on my profile if you're just looking for that.

## GDPR - Do we need it? A brief rundown of 'encdec.py'

Researchers *LOVE* GDPR. It's what they get up in the morning to think about and it's what gets them to bed at night. You may be thinking, how on Earth am I going to show that I'm towing the line of legality in regard to my participants' data? Well worry no more because that's what this little file helps with.

Once you've gathered playlist data, you can go overkill by running this file which can encrypt and decrypt whatever you grab from your participants' Spotify. [This](https://github.com/horsellcommon/Text-File-Encryption) is the standalone package if you're into that sort of thing.

When you run this, you'll be presented with the most beautiful GUI you've ever seen in your life, so just select the file and hit either encrypt or decrypt.

# What's the point of this?

Good question! I've been wondering that myself. The purpose of this is, or was, to aid in research focused around listener valence and arousal data. Data from this may benefit those studying or researching Psychology or Musicology.

The program gathers the valence of a song/songs (How happy or sad a song is) and the energy of a song. The user is able to gather playlist data of any Spotify account, as long as the user knows that account's Spotify username.
Once all data has been collected, a json file is created with all data collected for use (May or may not function as intended now compared to previously).

If you do end up using this code or program for whatever reason then please acknowledge where you got it from, you are more than welcome to use this in your own research.

# Troubleshooting & Known Issues

Honestly, it should work out of the box and if it isn't then you're doing it wrong. It's not me, it's you.
BUT, if you do come across any issues then send them through and I'll get to it.

- Some outputted JSON files may appear blank if the world-class API that this application is using fails to deliver. I may introduce another API in the future (I'm sorry) as a fallback if I can be bothered to get around to implementing it.

## Useful Links

* Download releases [here](https://github.com/horsellcommon/spotify-valence-app/releases)
* Link to the [Spotify developer dashboard](https://developer.spotify.com/dashboard)
* The third-party API you need! [FreqBlog's Music Metadata API](https://freqblog.com/)

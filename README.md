# spotify-valence-app

A VERY rough console-based program that gathers playlist metadata from the current user or a selected user.

To use this, you must have your own client id, secret and redirect URI. You can get these by creating your own app on the Spotify developer dashboard, a link is available at the bottom of this readme (You can find tutorials on how to properly use Spotify's development section online if you're struggling).<br>Once you have these, simply create your own .env and put the respective variables as:

ID=yourclientid<br>
SECRET=yourclientsecret<br>
URI=yourredirecturi


The purpose of this is to aid in research focused around listener valence and arousal data. Data from this may benefit those studying or researching Psychology or Musicology.

The program gathers the valence of a song/songs (How happy or sad a song is) and the energy of a song. The user is able to gather playlist data of any Spotify account, as long as the user knows that account's Spotify username.
Once all data has been collected, a json file is created with all data collected for use.

If you do end up using this code for whatever reason then please acknowledge where you got it from, you are more than welcome to use this in your own research.


Spotify developer dashboard: https://developer.spotify.com/dashboard

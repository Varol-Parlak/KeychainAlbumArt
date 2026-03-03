import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-read-currently-playing"
))

def get_current_song():
    track = sp.current_user_playing_track()
    
    if track is None or not track["is_playing"]:
        print("Nothing is playing")
        return
    
    title = track["item"]["name"]
    artist = track["item"]["artists"][0]["name"]
    art_url = track["item"]["album"]["images"][0]["url"]
    
    print(f"Now playing: {title} by {artist}")
    
    img_data = requests.get(art_url).content
    with open("cover.jpg", "wb") as f:
        f.write(img_data)
    print("Saved cover.jpg")

get_current_song()
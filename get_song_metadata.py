import asyncio
import requests
import re
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager

async def get_current_song():
    sessions = await GlobalSystemMediaTransportControlsSessionManager.request_async()
    current = sessions.get_current_session()
    if current:
        info = await current.try_get_media_properties_async()
        return info.title, info.artist
    return None, None

def get_high_res_art(title, artist):
    query = f"{title} {artist}".replace(" ", "+")
    url = f"https://itunes.apple.com/search?term={query}&media=music&limit=1"
    
    resp = requests.get(url).json()
    if resp["resultCount"] > 0:
        art_url = resp["results"][0]["artworkUrl100"]
        art_url_hd = art_url.replace("100x100bb", "600x600bb")
        
        img_data = requests.get(art_url_hd).content
        with open("cover.jpg", "wb") as f:
            f.write(img_data)
        print(f"{artist} - {title}")
    else:
        get_art_musicbrainz(title, artist)

def get_art_musicbrainz(title, artist):
    headers = {"User-Agent": "MusicArtFetcher/1.0 ( your@email.com )"}
    search_url = f"https://musicbrainz.org/ws/2/recording/?query=recording:{title}+artist:{artist}&fmt=json&limit=1"
    
    resp = requests.get(search_url, headers=headers).json()
    if resp.get("recordings"):
        release_id = resp["recordings"][0]["releases"][0]["id"]
        art_url = f"https://coverartarchive.org/release/{release_id}/front-500"
        
        img_resp = requests.get(art_url, headers=headers)
        if img_resp.status_code == 200:
            with open("cover.jpg", "wb") as f:
                f.write(img_resp.content)
        else:
            print("No cover art found")

async def main():
    title, artist = await get_current_song()
    if title:
        get_high_res_art(title, artist)
    else:
        print("Nothing is currently playing")

asyncio.run(main())
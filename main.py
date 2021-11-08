from bs4 import BeautifulSoup
import requests
import lxml
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

keep_ask_for_date = True
while keep_ask_for_date:

    time = input("What time you would like to travel to? Type the date in YYYY-MM-DD format: ")

    response = requests.get(f"https://www.billboard.com/charts/hot-100/{time}")
    web_page = response.text
    soup = BeautifulSoup(web_page, "lxml")

    artists = soup.find_all(class_="chart-element__information__artist text--truncate color--secondary")
    artists_list = [artist.get_text() for artist in artists]

    songs = soup.find_all(class_="chart-element__information__song text--truncate color--primary")
    songs_list = [song.get_text() for song in songs]

    if artists_list and songs_list:
        keep_ask_for_date = False
    else:
        print("Wrong input. make sure the date is in the past and the format is correct")

print("continue")

client_ID = os.environ["SPOTIPY_CLIENT_ID"]
client_secret = os.environ["SPOTIPY_CLIENT_SECRET"]
print(f"{client_ID}, {client_secret}")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://127.0.0.1:9090",
        client_id=client_ID,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt"
    ))

user_id = sp.current_user()["id"]
song_names = songs_list

song_uris = []
year = time.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{time} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
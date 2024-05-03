import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = "d49db720a99d4257b89fcc11beff3266"
client_secret = "f06be26d02004537b4151aa7d435f1e4"
user_id = "erccfq9chzntdqayamu7gpf29"


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri="http://example.com",
    scope="playlist-modify-public playlist-modify-private",
    cache_path="token.txt",
    username="Rhythm"
))

date = input(
    "Which year do you want to travel to? Type this date in format of YYYY-MM-DD :")
url = f"https://www.billboard.com/charts/hot-100/{date}/"
year = date.split("-")[0]

response = requests.get(url)
web_page = response.text
soup = BeautifulSoup(web_page, "html.parser")
song_names_spans = soup.select("div li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]
songs_uris = []


for song in song_names:
    result = sp.search(type="track", q=f"track:{song} year:{year}")

    try:
        uri = result["tracks"]["items"][0]["id"]
        songs_uris.append(uri)

    except:
        print(f"The song {song} doesn't exist")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100")
playlist_id = playlist["id"]
sp.user_playlist_add_tracks(
    user=user_id, playlist_id=playlist_id, tracks=songs_uris)

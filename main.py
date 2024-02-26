import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint


date = input("Which year do you want to travel to? Type the date in this format YYY-MM-DD: ")
BILLBOARD_URL = f"https://www.billboard.com/charts/hot-100/{date}"

#Spotify
SPOTIPY_CLIENT_ID = '866a86e99bb64a70ade75a198d49b05b'
SPOTIPY_CLIENT_SECRET = '9216cb81de334cb3b045d4c5001188c4'
SPOTIPY_REDIRECT_URI='http://example.com'

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=SPOTIPY_REDIRECT_URI,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username='Wiktoria Bronowska',
    )
)
user_id = sp.current_user()["id"]



def fetch_song_titles(url):
    response = requests.get(url)
    if response.status_code == 200:
        web_page = response.text
        soup = BeautifulSoup(web_page, "html.parser")
        articles = soup.find_all(name="li", class_="o-chart-results-list__item")
        songs_titles = []
        for article in articles:
            songs_titles.extend(article.find_all('h3', id='title-of-a-story'))
        songs_titles = [title.getText().replace('\t', '').replace('\n', '') for title in songs_titles]
        get_songs_uris(songs_titles, date)
        return
    else:
        print(f"Failed to fetch data from {url}")
        return []


def get_songs_uris(songs_titles, date):
    song_uris = []
    year = date.split("-")[0]
    for song in songs_titles:
        result = sp.search(q=f"track:{song} year:{year}", type="track")
        try:
            uri = result["tracks"]["items"][0]["uri"]
            song_uris.append(uri)
        except IndexError:
            print(f"{song} doesn't exist in Spotify. Skipped.")
    playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

    sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)


fetch_song_titles(BILLBOARD_URL)



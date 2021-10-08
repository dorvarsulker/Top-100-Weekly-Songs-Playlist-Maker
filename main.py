# Required libraries.
import requests
from bs4 import BeautifulSoup
from logo import logo
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Getting required inputs.
print(logo)
print("Welcome to the Spotify Playlist Maker!")
print("This program creates a playlist of 100 Top Weekly Songs of a specific date!")
print("To begin, please enter this link: https://developer.spotify.com/dashboard/")
print("After doing so, please login and create an app. (Name it however you'd like.")
client_id = input("Please enter your client id shown in your app page: ")
client_secret = input("Please enter your client secret as shown in your app page: ")
print("Click on edit settings on your page, and add a Redirect URI (can be pretty much anything)")
redirect_uri = input("Enter the Redirect URI here: ")

# Recieving Input from user regarding the desired date.
print("\nAlright than!, Now that we are done with the authorization mumbo-jumbo,")
date = input("Which date do you have in mind? Type the date in this format YYYY-MM-DD: ")
TOP_100_LINK = f"https://www.billboard.com/charts/hot-100/{date}"


# Making a request to pull Top 100 Songs list.
response = requests.get(url=TOP_100_LINK).text

# Reformatting into a more digestable data format
soup = BeautifulSoup(response, "html.parser")
artists = [i.getText() for i in soup.find_all(name="span", class_="chart-element__information__artist")]
songs = [i.getText() for i in soup.find_all(name="span", class_="chart-element__information__song")]

# Making an Auth request to Spotify.
scope = "playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))
# A list of Spotify Songs URIs.
year = date.split("-")[0]
song_uris = []
for song in songs:
    results = sp.search(q=f"track:{song} year:{year}")
    try:
        uri = results["tracks"]["items"][0]["uri"]
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped")

# Creating a new playlist
current_user = sp.current_user()['id']
playlist_id = sp.user_playlist_create(current_user,
                                      f"{date} Billboard 100",
                                      public=False,
                                      collaborative=False,
                                      description=f'Top 100 Songs for {date}')
# Adding songs to playlist
for i in range(len(song_uris)):
    sp.playlist_add_items(playlist_id, song_uris[i], position=i)
print("Code completed successfully.")
import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Firebase
firebase_service_account = json.loads(os.getenv("FIREBASE_SERVICE_ACCOUNT"))
cred = credentials.Certificate(firebase_service_account)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Spotify Credentials
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"

# Spotify Scope for Playlist Modification
SPOTIFY_SCOPE = "playlist-modify-public"

# Initialize Spotify Client
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SPOTIFY_SCOPE,
    )
)

# Get the Spotify User ID
user_id = sp.current_user()["id"]


# Fetch Song Links from Firebase
def fetch_song_links():
    song_links = db.collection("song_links").stream()
    return [(song_link.id, song_link.to_dict()["url"]) for song_link in song_links]


# Extract Track IDs from URLs
def extract_track_ids(song_links):
    track_ids = []
    for _, link in song_links:
        parts = link.split("/")
        if len(parts) > 0 and parts[-1]:
            track_id = parts[-1].split("?")[0]
            track_ids.append(track_id)
        else:
            print(f"Invalid Spotify URL: {link}")
    return track_ids


# Get Current Playlist Tracks
def get_playlist_tracks(playlist_id):
    results = sp.playlist_items(playlist_id)
    tracks = [item["track"]["id"] for item in results["items"]]
    return set(tracks)


# Add Songs to Specific Playlist
def add_songs_to_playlist(playlist_id, song_links):
    current_tracks = get_playlist_tracks(playlist_id)
    new_songs = [
        (doc_id, link)
        for doc_id, link in song_links
        if link.split("/")[-1].split("?")[0] not in current_tracks
    ]

    if not new_songs:
        print("No new songs to add.")
        return

    track_ids = extract_track_ids(new_songs)
    if track_ids:
        try:
            sp.user_playlist_add_tracks(user_id, playlist_id, track_ids)
            print("New tracks added to the playlist successfully.")
        except spotipy.exceptions.SpotifyException as e:
            print(f"An error occurred: {e}")
    else:
        print("No valid track IDs found.")


# Playlist ID from the given URL
target_playlist_id = "2vFjMb9dw5WbIrrr3RUwXY"

# Execute the Function
song_links = fetch_song_links()
add_songs_to_playlist(target_playlist_id, song_links)

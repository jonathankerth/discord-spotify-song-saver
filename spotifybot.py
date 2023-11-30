import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

try:
    # Initialize Firebase
    firebase_service_account = json.loads(os.getenv("FIREBASE_SERVICE_ACCOUNT"))
    cred = credentials.Certificate(firebase_service_account)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firebase initialized successfully.")
except Exception as e:
    print(f"Failed to initialize Firebase: {e}")
    exit(1)


playlist_url = (
    "https://open.spotify.com/playlist/2vFjMb9dw5WbIrrr3RUwXY?si=e757825a2a5a4074"
)
parts = playlist_url.split("/")
user_id = parts[4]

try:
    # Initialize Spotify Client using Client Credentials Flow
    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
        )
    )
    print("Spotify client initialized successfully.")
except Exception as e:
    print(f"Failed to initialize Spotify client: {e}")
    exit(1)


def fetch_song_links():
    try:
        song_links = db.collection("song_links").stream()
        return [(song_link.id, song_link.to_dict()["url"]) for song_link in song_links]
    except Exception as e:
        print(f"Error fetching song links from Firebase: {e}")
        return []


def extract_track_ids(song_links):
    track_ids = []
    for _, link in song_links:
        try:
            parts = link.split("/")
            if len(parts) > 0 and parts[-1]:
                track_id = parts[-1].split("?")[0]
                track_ids.append(track_id)
            else:
                print(f"Invalid Spotify URL: {link}")
        except Exception as e:
            print(f"Error processing link {link}: {e}")
    return track_ids


def get_playlist_tracks(playlist_id):
    try:
        results = sp.playlist_items(playlist_id)
        tracks = [item["track"]["id"] for item in results["items"]]
        return set(tracks)
    except Exception as e:
        print(f"Error fetching tracks from playlist {playlist_id}: {e}")
        return set()


def add_songs_to_playlist(user_id, target_playlist_id, song_links):
    try:
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
            sp.user_playlist_add_tracks(user_id, playlist_id, track_ids)
            print("New tracks added to the playlist successfully.")
        else:
            print("No valid track IDs found.")
    except Exception as e:
        print(f"An error occurred while adding songs to playlist: {e}")


# Playlist ID from the given URL
target_playlist_id = "2vFjMb9dw5WbIrrr3RUwXY"

# Execute the Function
try:
    song_links = fetch_song_links()
    print(f"Fetched {len(song_links)} song links from Firebase.")
    add_songs_to_playlist(target_playlist_id, song_links)
except Exception as e:
    print(f"An error occurred during execution: {e}")
try:
    song_links = fetch_song_links()
    print(f"Fetched {len(song_links)} song links from Firebase.")
    add_songs_to_playlist(
        user_id, target_playlist_id, song_links
    )  # Pass user_id as the first argument
except Exception as e:
    print(f"An error occurred during execution: {e}")

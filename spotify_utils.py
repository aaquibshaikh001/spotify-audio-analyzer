import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_playlist_tracks(playlist_id):
    tracks = []
    results = sp.playlist_items(playlist_id, additional_types=["track"])
    tracks.extend(results['items'])

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    return [track['track']['id'] for track in tracks if track['track']]

def get_audio_features(track_ids):
    audio_features = []
    for i in range(0, len(track_ids), 100):
        batch = track_ids[i:i + 100]
        try:
            features = sp.audio_features(batch)
            if features:
                audio_features.extend(features)
        except Exception as e:
            print(f"Error fetching audio features: {e}")
    return audio_features

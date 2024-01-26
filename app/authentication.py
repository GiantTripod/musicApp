import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

def get_spotify_client():
    SPOTIPY_CLIENT_ID = 'e139a0fc9290404996790866f596dd74'
    SPOTIPY_CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    SPOTIPY_REDIRECT_URI = 'https://gianttripod.pythonanywhere.com/'

    sp_oauth = SpotifyOAuth(
        SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope='user-library-read'
    )
    
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        print(f'Please visit this URL to authorize your application: {auth_url}')
        response = input('Paste the above link here: ')
        token_info = sp_oauth.get_access_token(response)

    # Create Spotify client
    sp = spotipy.Spotify(auth=token_info['access_token'])
    return sp
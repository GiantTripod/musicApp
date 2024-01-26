import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

def get_spotify_client():
    SPOTIPY_CLIENT_ID = 'e139a0fc9290404996790866f596dd74'
    SPOTIPY_CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    SPOTIPY_REDIRECT_URI = 'https://accounts.spotify.com/authorize?scope=user-library-read+user-read-private&response_type=code&redirect_uri=https%3A%2F%2Fgianttripod.pythonanywhere.com%3A8080%2Fcallback&client_id=e139a0fc9290404996790866f596dd74&flow_ctx=c51d5a52-878f-4cb9-9f5b-a7d0f2fc70a4%3A1706259578'

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
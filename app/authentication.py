import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_spotify_client():
    SPOTIPY_CLIENT_ID = 'e139a0fc9290404996790866f596dd74'
    SPOTIPY_CLIENT_SECRET = 'da931e8a3f19400580c8bf707ba6ce83'
    SPOTIPY_REDIRECT_URI = 'http://localhost:5000/callback'

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
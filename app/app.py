from flask import Flask, redirect, request, render_template
from spotipy.oauth2 import SpotifyOAuth


app = Flask(__name__)

SPOTIPY_CLIENT_ID = 'e139a0fc9290404996790866f596dd74'
SPOTIPY_CLIENT_SECRET = 'da931e8a3f19400580c8bf707ba6ce83'
SPOTIPY_REDIRECT_URI = 'http://localhost:5000/callback'

sp_oauth = SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope='user-library-read')


@app.route('/')
def home():
       auth_url = sp_oauth.get_authorize_url()
       return redirect(auth_url)

@app.route('/callback')
def callback():
    token_info = sp_oauth.get_access_token(request.args['code'])
    # Now you can use token_info to make Spotify API requests
    # For example: sp = spotipy.Spotify(auth=token_info['access_token'])
    return render_template('home.html')

@app.route('/about')
def about():
        return render_template('about.html')


@app.route('/discovery')
def discovery():
        return render_template('discovery.html')

@app.route('/login')
def login():
        return render_template('login.html')

@app.route('/signup')
def signup():
        return render_template('signup.html')




if __name__ == "__main__":
        app.run(debug=True)
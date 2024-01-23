from flask import Flask, redirect, render_template, session, url_for, request
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)



app.secret_key = os.getenv("FLASK_SECRET_KEY")


SPOTIPY_CLIENT_ID = 'e139a0fc9290404996790866f596dd74'
SPOTIPY_CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = 'http://localhost:5000/callback'

sp_oauth = SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope='user-library-read')

@app.route('/')
def home():
    # Check if the user is authenticated
    if 'token_info' not in session or sp_oauth.is_token_expired(session['token_info']):
        # If not authenticated, redirect to Spotify authorization
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    # If authenticated, render the homepage
    return render_template('home.html')

# Your callback route
@app.route('/callback')
def callback():
    # Handle Spotify callback and get access token
    token_info = sp_oauth.get_access_token(request.args['code'])
    
    # Store token_info in the session for later use
    session['token_info'] = token_info
    
    # Redirect to the homepage
    return redirect(url_for('home'))

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
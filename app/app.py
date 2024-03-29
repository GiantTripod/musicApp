from flask import Flask, redirect, render_template, session, url_for, request, flash
from spotipy.oauth2 import SpotifyOAuth
import os
import secrets
import spotipy
from spotipy import SpotifyException
from dotenv import load_dotenv
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

load_dotenv()

app = Flask(__name__)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

app.secret_key = os.getenv("FLASK_SECRET_KEY", secrets.token_hex(16))

SPOTIPY_CLIENT_ID = 'e139a0fc9290404996790866f596dd74'
SPOTIPY_CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = 'https://gianttripod.pythonanywhere.com/callback'
SCOPES = 'user-read-email user-read-private user-library-read'

sp_oauth = SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPES)


@login_manager.user_loader
def load_user(user_id):
    print('Load user: Start')
    if user_id:
        token_info = session.get('token_info', None)
        print(f"Token Info in load_user: {token_info}")

        if token_info and sp_oauth.is_token_expired(token_info):
            try:
                token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
                session['token_info'] = token_info
            except SpotifyException as e:
                print(f"Error refreshing access token: {e}")

        sp = spotipy.Spotify(auth=session['token_info']['access_token'])
        user_data = sp.me()
        print(f"User Data in load_user: {user_data}")

        if user_data and 'id' in user_data:
            user = User(user_data['id'], user_data.get('display_name', 'Unknown'))
            print(f"User object created: {user.id}, {user.name}")
            return user
        else:
            print('User_data or user ID not present')
    else:
        print('User ID not present')

    print('Load user: End')
    return None

class User(UserMixin):
    def __init__(self, id, name):
        self.id = id
        self.name = name

@app.before_request
def before_request():
    print('Before request: Start')
    if current_user.is_authenticated:
        print('User is authenticated')
        print(f"User ID: {current_user.id}, User Name: {current_user.name}")
    else:
        print('User is not authenticated')
    print('Before request: End')


@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    return render_template('home.html')

@app.route('/callback')
def callback():
    try:
        print('Callback: hello world')
        token_info = sp_oauth.get_access_token(request.args['code'])
        print(f"Token Info: {token_info}")
        
        # Store token_info in the session
        session['token_info'] = token_info

        # Print user data
        sp = spotipy.Spotify(auth=token_info['access_token'])
        user_data = sp.me()
        print(f"User Data: {user_data}")

        user_id = user_data.get('id')
        print(f"User ID: {user_id}")

        if user_id:
            user = load_user(user_id)
            if user:
                login_user(user)
                print(f"User logged in: {current_user.id}, {current_user.name}")
            else:
                flash("Failed to log in. Please try again.")

        return redirect(url_for('profile'))

    except Exception as e:
        print(f"Error in callback route: {e}")
        flash("Failed to authenticate. Please try again.")
        return redirect(url_for('profile'))

@app.route('/profile')
@login_required
def profile():
    sp = spotipy.Spotify(auth=session['token_info']['access_token'])
    print(sp)
    return render_template('profile.html', user=sp.current_user())

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('token_info', None)  # Clear Spotify OAuth token information
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/discovery')
def discovery():
    return render_template('discovery.html')

@app.route('/login')
def login():
    if 'token_info' not in session or sp_oauth.is_token_expired(session['token_info']):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('profile'))

if __name__ == "__main__":
    app.run(debug=True)
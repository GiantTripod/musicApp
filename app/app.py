from flask import Flask, redirect, render_template, session, url_for, request, flash
from spotipy.oauth2 import SpotifyOAuth
import os
import spotipy
from spotipy import SpotifyException
from dotenv import load_dotenv
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

load_dotenv()

app = Flask(__name__)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

app.secret_key = os.getenv("FLASK_SECRET_KEY")

SPOTIPY_CLIENT_ID = 'e139a0fc9290404996790866f596dd74'
SPOTIPY_CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = 'http://gianttripod.pythonanywhere.com/callback'

sp_oauth = SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope='user-library-read user-read-private')

@login_manager.user_loader
def load_user(user_id):
    if user_id:
        token_info = session.get('token_info', None)
        if token_info and sp_oauth.is_token_expired(token_info):
            try:
                token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
                session['token_info'] = token_info
            except SpotifyException as e:
                print(f"Error refreshing access token: {e}")

        sp = spotipy.Spotify(auth=session['token_info']['access_token'])
        user_data = sp.me()
        if user_data and 'id' in user_data:
            return User(user_data['id'], user_data.get('display_name', 'Unknown'))

    return None

class User(UserMixin):
    def __init__(self, id, name):
        self.id = id
        self.name = name

@app.before_request
def before_request():
    if current_user.is_authenticated:
        print('User is authenticated')
        print(f"User ID: {current_user.id}, User Name: {current_user.name}")
        # You can use current_user.id and current_user.name in your application


@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    return render_template('home.html')

@app.route('/callback')
def callback():
    print('Callback: hello world')
    token_info = sp_oauth.get_access_token(request.args['code'])
    print(f"Token Info: {token_info}")
    session['token_info'] = token_info
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
    return redirect(url_for('home'))

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
    return render_template('profile.html')

if __name__ == "__main__":
    app.run(debug=True)
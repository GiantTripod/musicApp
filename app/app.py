from flask import Flask
from flask import render_template
from app.authentication import get_spotify_client


app = Flask(__name__)


@app.route('/')
def home():
        # Get the Spotify client
        sp = get_spotify_client()

    # Example: Get the user's saved tracks
        saved_tracks = sp.current_user_saved_tracks(limit=10)

    # Extract relevant information for display
        tracks_info = [
        {
            'name': track['track']['name'],
            'artists': ', '.join(artist['name'] for artist in track['track']['artists']),
            'url': track['track']['external_urls']['spotify']
        }
        for track in saved_tracks['items']
        ]

        return render_template('home.html', saved_tracks=tracks_info)

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
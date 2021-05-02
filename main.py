import spotipy
import json
import flask
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='513f41055fe74def8c2a9236458d8dcb',
                                               client_secret='5c37d1a354a743ed97dcb8b797b86cb0',
                                               redirect_uri='http://example.com/',
                                               scope='user-read-playback-state'))

app = flask.Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')
def get_song():
    results = sp.current_user_playing_track()

    url = results['item']['album']['images'][1]['url']
    name = results['item']['name']
    artist = results['item']['album']['artists'][0]['name']
    title = name + ' - ' + artist

    jsondata = json.dumps({'title': title, 'image': url})

    return(jsondata)


if __name__ == "__main__":
    app.run(port=3000)

import spotipy
import json
import flask
from spotipy.oauth2 import SpotifyOAuth
from flask_restful import Resource, Api
from flask_cors import CORS

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='513f41055fe74def8c2a9236458d8dcb',
                                               client_secret='5c37d1a354a743ed97dcb8b797b86cb0',
                                               redirect_uri='http://example.com/',
                                               scope='user-read-playback-state'))
app = flask.Flask(__name__)
api = Api(app)
CORS(app)

class Song(Resource):
  def __init__(self):
    super().__init__()

  def get(self):
      try:
        results = sp.current_user_playing_track()

        url = results['item']['album']['images'][1]['url']
        name = results['item']['name']
        artist = results['item']['album']['artists'][0]['name']
        title = name + ' - ' + artist

        jsondata = json.dumps({'title': title, 'image': url})
        resp = flask.Response(response=jsondata,
                  status=200,
                  mimetype="application/json")
        self.latest = resp
        return (resp)
      except:
        return flask.Response(response=json.dumps({"title" : "Nothing rn, sorry!", "image" : "https://cdn.shopify.com/s/files/1/3013/1908/products/LCD-1_PS3_2000x.jpg?v=1584599044"}),
                  status=200,
                  mimetype="application/json")

api.add_resource(Song, '/')

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
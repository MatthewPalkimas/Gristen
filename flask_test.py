import flask
from gristen import Gristen, SongNotFound
import flask_socketio

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = flask_socketio.SocketIO(app)

default_song = "Sound & Color"

gs = None


@app.route('/audio<song>', methods=["GET", "POST"])
def audio(song):
    if flask.request.method == "GET":
        try:
            global gs
            if gs is None:
                gs = Gristen(song)
            return flask.Response(gs.generate_wav_data())
        except SongNotFound:
            raise SongNotFound


@app.route('/', methods=["GET", "POST"])
def sessions():
    global gs
    errors = ""
    if flask.request.method == "POST":
        try:
            song = flask.request.form['song_name']
        except:
            song = gs.song_name
            return flask.render_template('test.html', song=song, song_name=gs.song_name, song_artist=gs.song_artist)
        gs = Gristen(song)
        return flask.render_template('test.html', song=song, song_name=gs.song_name, song_artist=gs.song_artist, errors=errors)
    else:
        return flask.render_template('test.html', song=default_song)


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)


@socketio.on('song change')
def handle_song_request(json, methods=['GET', 'POST']):
    print(json)
    global gs
    song = json
    gs = Gristen(song)
    song_name = gs.song_name
    song_artist = gs.song_artist
    print('received song request: ' + str(json))
    socketio.emit('')


if __name__ == '__main__':
    socketio.run(app, debug=True, port=6458)
# app.run(debug=True, port=6464)

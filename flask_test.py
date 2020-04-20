import flask
from gristen import Gristen, SongNotFound

app = flask.Flask(__name__)

default_song = "Sound & Color"


@app.route('/audio<song>', methods=["GET", "POST"])
def audio(song):
    if flask.request.method == "GET":
        try:
            gs = Gristen(song)
            return flask.Response(gs.generate_wav_data())
        except SongNotFound:
            raise SongNotFound


@app.route('/', methods=["GET", "POST"])
def index():
    errors = ""
    if flask.request.method == "POST":
        song = flask.request.form['song_name']
        try:
            gs = Gristen(song)
            song_name = gs.song_name
            song_artist = gs.song_artist
            return '''
                <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <meta http-equiv="X-UA-Compatible" content="ie=edge">
                        <title>Gristen</title>
                    </head>
                    <body>
                        <p>Currently listening to</p>
                        <p>{song_name} by {song_artist}</p>
                        <audio controls autoplay loop>
                            <source src="/audio{song}" type="audio/x-wav;codec=pcm">
                            Your browser does not support the audio element.
                        </audio>
                        <p>To change the current song enter below:</p>
                        <form method="post" action=".">
                            <p><input name="song_name" /></p>
                            <p><input type="submit" value="Gristen" /></p>
                        </form>
                    </body>
                </html>
                '''.format(song=song, song_name=song_name, song_artist=song_artist)
        except SongNotFound:
            errors = "<p>{!r} is not available.</p>\n".format(flask.request.form["song_name"])
    return '''
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">
            <title>Gristen</title>
        </head>
        <body>
            <p>Hello! Enter the song name you want to listen to :)</p>
            {errors}
            <form method="post" action=".">
                <p><input name="song_name" /></p>
                <p><input type="submit" value="Gristen" /></p>
            </form>
            <p>If you want a sample song then click play below!</p>
            <audio controls>
                <source src="/audio{song}" type="audio/x-wav;codec=pcm">
                Your browser does not support the audio element.
            </audio>
        </body>
    </html>
    '''.format(song=default_song, errors=errors)


app.run(debug=True, port=6464)

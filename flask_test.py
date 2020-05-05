import flask
from gristen import Gristen, SongNotFound
import flask_socketio
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from flask_sqlalchemy import SQLAlchemy
import datetime

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
socketio = flask_socketio.SocketIO(app)

default_song = "Sound & Color"
gs = None

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)


@app.route('/create_<name>')
def index(name):
    user = User(name=name)
    db.session.add(user)
    db.session.commit()
    return '<h1>Added new User!</h1>'


@app.route('/get_<name>')
def get_user_id(name):
    user = User.query.filter_by(name=name).first()
    return f'The user id is { user.id }'


class LoginForm(FlaskForm):
    username = StringField('username')


@app.route('/audio_<song>', methods=["GET", "POST"])
def audio_(song):
    if flask.request.method == "GET":
        try:
            global gs
            if gs is None:
                gs = Gristen(song)
            return flask.Response(gs.generate_wav_data(), mimetype="audio/x-wav")
        except SongNotFound:
            raise SongNotFound


@app.route('/group', methods=['POST'])
def group():
    group = flask.request.form['group_name']
    return flask.redirect(flask.url_for('group_', id=group))


@app.route('/group_<id>', methods=["GET", "POST"])
def group_(id):
    global gs
    errors = ""
    if flask.request.method == "POST":
        try:
            song = flask.request.form['song_name']
            print(song)
        except:
            print("couldn't get song name?")
            song = gs.song_name
            return flask.render_template('test.html', song=song, song_name=gs.song_name, song_artist=gs.song_artist, group_name=id)
        gs = Gristen(song)
        return flask.render_template('test.html', song=song, song_name=gs.song_name, song_artist=gs.song_artist, errors=errors, group_name=id)
    else:
        return flask.render_template('test.html', song=default_song, group_name=id, song_name=gs.song_name, song_artist=gs.song_artist)


@app.route('/home', methods=["GET", "POST"])
def home():
    name = flask.request.form['name']
    if User.query.filter_by(name=name).first() is not None:
        return flask.render_template('index.html', song=default_song, name=name, greeting="Welcome back ")
    else:
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
        print("added a new user")
        return flask.render_template('index.html', song=default_song, name=name, greeting="Welcome ")


@app.route('/', methods=['GET', 'POST'])
def form():
    form = LoginForm()
    if form.validate_on_submit():
        return flask.redirect(flask.url_for('home'))
    return flask.render_template('form.html', form=form)


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


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True, port=6464)
# app.run(debug=True, port=6464)

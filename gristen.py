import pyaudio as pya
import wave
import time
import os
import glob
import sys
import string
import youtube_dl
import youtube_search
import subprocess

CHUNK = 1024
youtube_options = {
    'format': 'bestaudio/best',
    'extractaudio': True,  # only keep the audio
    'audioformat': "mp3",  # wav or mp3 hopefully
    'outtmpl': 'music/%(id)s.mp3',  # name the file the ID of the video
    'noplaylist': True,  # only download single song, not playlist
}


class SongNotFound(Exception):
    pass


class Gristen:
    def __init__(self, song_requested=None):
        self.music_path = os.path.join(os.getcwd(), 'music')
        self.wf = None
        self.wav_path = None
        self.utube_title = None
        self.stream = None
        self.p = None
        if song_requested is not None or song_requested != '':
            try:
                self.lil_path = self.find_song(song_requested)
                self.wav_file = os.path.join(self.music_path, self.lil_path)
                print("found song %s" % self.wav_file)
            except SongNotFound:
                raise SongNotFound
        else:
            raise SongNotFound
        self.wf = wave.open(self.wav_file, 'rb')
        self.get_song_info(song_requested)
        # self.generate_wav_data()

    def find_song(self, song_requested):
        song_db = glob.glob(os.path.join(self.music_path, '*'))
        for song in song_db:
            song_name = song.split('\\')[-1]
            if song_name.lower().__contains__(song_requested.lower()):
                return song.split('\\')[-1]
        try:
            print("attempting to download song %s" % song_requested)
            song_url = youtube_search.YoutubeSearch(song_requested + ' lyrics', max_results=3).to_dict()[0]['link']
            url = 'https://www.youtube.com' + song_url
            with youtube_dl.YoutubeDL(youtube_options) as ydl:
                r = ydl.extract_info(url, download=True)
                self.utube_title = r['title'].replace('\"', '')
                self.utube_title = self.utube_title.replace('/', '')
                song_mp3 = os.path.join(self.music_path, r['id'] + '.mp3')
                time.sleep(5)
                self.wav_path = os.path.join(self.music_path, self.utube_title + '.wav')
                subprocess.call(['ffmpeg',
                                 '-n',
                                 '-i',
                                 song_mp3,
                                 self.wav_path])
                os.remove(song_mp3)
                return self.wav_path
        except Exception as e:
            print(e)
            raise SongNotFound

    def get_song_info(self, song_requested):
        song_length = self.wf.getnframes()
        self.song_duration = int(song_length / self.wf.getframerate())
        self.minutes = self.song_duration / 60
        self.seconds = self.song_duration % 60
        try:
            song_info = self.wav_file.split('\\')[-1].split('.')[0].split(' - ')
            self.song_name = song_info[1]
            self.song_artist = song_info[0]
        except:
            if self.utube_title is not None:
                self.song_name = self.utube_title
            else:
                self.song_name = self.wav_file.split('\\')[-1].split('.')[0]
            self.song_artist = ""

    def callback(self, in_data, frame_count, time_info, status):
        wav_bytes = self.wf.readframes(frame_count)
        return wav_bytes, pya.paContinue

    def generate_wav_data(self):
        self.p = pya.PyAudio()
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                        channels=self.wf.getnchannels(),
                        rate=self.wf.getframerate(),
                        output=True)

        print("Current Song:\n--- %s by %s" % (self.song_name, self.song_artist))
        with open(self.wav_file, "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
        # self.stream = p.open(format=p.get_format_from_width(self.wf.getsampwidth()),
        #                 channels=self.wf.getnchannels(),
        #                 rate=self.wf.getframerate(),
        #                 output=True,
        #                 stream_callback=self.callback)
        #
        # self.stream.start_stream()
        # for second_count in range(self.song_duration):
        #     total_of_song = round(second_count / self.song_duration * 60)
        #     timestamp = ('▮' * total_of_song) + ('▯' * (60 - total_of_song))
        #     sys.stdout.write("\r")
        #     sys.stdout.write("--- %02d:%02d %s %02d:%02d" %
        #                      (second_count / 60, second_count % 60, timestamp, self.minutes, self.seconds))
        #     sys.stdout.flush()
        #     time.sleep(1)
        #
        # while self.stream.is_active():
        #     time.sleep(0.1)

        print("\nstopping stream")
        self.stream.stop_stream()
        self.stream.close()

        self.p.terminate()


if __name__ == '__main__':
    while True:
        song_request = input("Hello! Enter the song name you want to listen to :)\n~ ")
        try:
            Gristen(song_request)
        except SongNotFound:
            print("Could not find song %s..." % song_request)
'''
ILL TYPE HERE
pretty much it is playing through the stream.write!!!
so if we can somehow make the clients receieve the data and then pass that to the string using numpy
read into numpy as dtype 16 int bit songs so that numpy can be created like this
'''
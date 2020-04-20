import pyaudio as pya
import wave
import time
import os
import glob
import sys

CHUNK = 1024


class SongNotFound(Exception):
    pass


class Gristen:
    def __init__(self, song_requested=None):
        self.music_path = os.path.join(os.getcwd(), 'music')
        self.wf = None
        if song_requested is not None:
            try:
                self.lil_path = self.find_song(song_requested)
                self.wav_file = os.path.join(self.music_path, self.lil_path)
            except SongNotFound:
                raise SongNotFound
        self.wf = wave.open(os.path.join('music', self.wav_file), 'rb')
        self.get_song_info()
        self.generate_wav_data()

    def find_song(self, song_requested):
        song_db = glob.glob(os.path.join(self.music_path, '*'))
        for song in song_db:
            song_name = song.split('\\')[-1].split(' - ')[0]
            if song_requested == song_name:
                return song.split('\\')[-1]
        raise SongNotFound

    def get_song_info(self):
        song_length = self.wf.getnframes()
        self.song_duration = int(song_length / self.wf.getframerate())
        self.minutes = self.song_duration / 60
        self.seconds = self.song_duration % 60
        song_info = self.wav_file.split('\\')[-1].split('.')[0].split(' - ')
        self.song_name = song_info[0]
        self.song_artist = song_info[1]

    def callback(self, in_data, frame_count, time_info, status):
        wav_bytes = self.wf.readframes(frame_count)
        return wav_bytes, pya.paContinue

    def generate_wav_data(self):
        p = pya.PyAudio()
        self.stream = p.open(format=p.get_format_from_width(self.wf.getsampwidth()),
                        channels=self.wf.getnchannels(),
                        rate=self.wf.getframerate(),
                        output=True)
        # self.stream = p.open(format=p.get_format_from_width(self.wf.getsampwidth()),
        #                 channels=self.wf.getnchannels(),
        #                 rate=self.wf.getframerate(),
        #                 output=True,
        #                 stream_callback=self.callback)

        print("Current Song:\n--- %s by %s" % (self.song_name, self.song_artist))
        with open(self.wav_file, "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)

        self.stream.stop_stream()
        self.stream.close()

        p.terminate()


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
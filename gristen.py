import pyaudio as py
import wave
import time
import os
import glob
import sys
import numpy as np

CHUNK = 1024


class Gristen:
    def __init__(self, song_requested=None):
        self.music_path = os.path.join(os.getcwd(), 'music')
        self.wf = None
        if song_requested is not None:
            wav_file = self.find_song(song_requested)
            if wav_file is not None:
                self.wav_file = os.path.join(self.music_path, wav_file)
            else:
                self.wav_file = os.path.join(self.music_path, 'Timeless Clouds - Henrik Olsson.WAV')
        self.generate_wav_data()

    def find_song(self, song_requested):
        song_db = glob.glob(os.path.join(self.music_path, '*'))
        for song in song_db:
            song_name = song.split('\\')[-1].split(' - ')[0]
            if song_requested == song_name:
                return song.split('\\')[-1]
        print("Did not find song '%s' sorry!" % song_requested)
        return None

    def callback(self, in_data, frame_count, time_info, status):
        wav_bytes = self.wf.readframes(frame_count)
        return wav_bytes, py.paContinue

    def generate_wav_data(self):
        self.wf = wave.open(os.path.join('music', self.wav_file), 'rb')
        song_length = self.wf.getnframes()
        song_duration = int(song_length / self.wf.getframerate())
        minutes = song_duration / 60
        seconds = song_duration % 60
        song_info = self.wav_file.split('\\')[-1].split('.')[0].split(' - ')
        song_name = song_info[0]
        song_artist = song_info[1]

        p = py.PyAudio()
        stream = p.open(format=p.get_format_from_width(self.wf.getsampwidth()),
                        channels=self.wf.getnchannels(),
                        rate=self.wf.getframerate(),
                        output=True,
                        stream_callback=self.callback)

        print("Current Song:\n--- %s by %s" % (song_name, song_artist))

        stream.start_stream()
        for second_count in range(song_duration):
            total_of_song = round(second_count / song_duration * 60)
            timestamp = ('▮' * total_of_song) + ('▯' * (60 - total_of_song))
            sys.stdout.write("\r")
            sys.stdout.write("--- %02d:%02d %s %02d:%02d" %
                             (second_count / 60, second_count % 60, timestamp, minutes, seconds))
            sys.stdout.flush()
            time.sleep(1)

        while stream.is_active():
            time.sleep(0.1)

        print("\nstopping stream")
        stream.stop_stream()
        stream.close()

        p.terminate()


if __name__ == '__main__':
    song_request = input("Hello! Enter the song name you want to listen to :)\n~ ")
    music = Gristen(song_request)
'''
ILL TYPE HERE
pretty much it is playing through the stream.write!!!
so if we can somehow make the clients receieve the data and then pass that to the string using numpy
read into numpy as dtype 16 int bit songs so that numpy can be created like this
'''
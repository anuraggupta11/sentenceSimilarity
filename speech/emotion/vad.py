import utils as utils
import os
import webrtcvad
import jsonpickle

"""Represents a "frame" of audio data."""


class Frame(object):
    def __init__(self, bytes, timestamp, duration):
        self.bytes = bytes
        self.timestamp = timestamp
        self.duration = duration


"""Represents a snippet of the audio file post performing vad."""


class Snippet(object):
    def __init__(self, path, from_time, to_time):
        self.path = path
        self.from_time = from_time
        self.to_time = to_time
    def add_emotion(self, emotion, score):
        self.emotion = emotion
        self.score = score

def vad(file_path):
    print('Processing ' + file_path + ' for voice activity detection...')
    file_name = os.path.basename(file_path).replace('.wav', '')
    chunk_folder_path = os.path.dirname(file_path) + '/' + file_name + '/'
    os.makedirs(chunk_folder_path, exist_ok=True)
    print('Storing chunks of vad in ' + chunk_folder_path)
    snippets = []
    aggressiveness = 2
    min_chunk_length = 2.5
    max_chunk_length = 3.0
    accumulated_frames = []
    chunk_count = 0
    vad = webrtcvad.Vad(aggressiveness)
    audio, sample_rate, audio_length = utils.read_wave(file_path)
    # this particular implementation (webrtcvad) works best at these frequency
    assert sample_rate in (8000, 16000)
    frame_duration_ms = 30
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
    offset = 0
    timestamp = 0.0
    chunk_from = 0.0
    chunk_to = 0.0
    duration = (float(n) / sample_rate) / 2.0
    while offset + n < len(audio):
        frame = Frame(audio[offset:offset + n], timestamp, duration)
        is_speech = vad.is_speech(frame.bytes, sample_rate)
        if(is_speech):
            accumulated_frames.append(audio[offset:offset + n])
            if(chunk_from == chunk_to):
                chunk_from = offset/len(audio)*audio_length
            chunk_to = (offset+n)/len(audio)*audio_length
            if(len(accumulated_frames) > 0):
                if(chunk_to - chunk_from > max_chunk_length):
                    chunk_file_path = chunk_folder_path + \
                        file_name + "_{:03}".format(chunk_count)+'.wav'
                    utils.write_wave(
                        chunk_file_path, accumulated_frames, sample_rate)
                    snippets.append(
                        Snippet(chunk_file_path, chunk_from, chunk_to))
                    print('Creating chunk from: ' + str(chunk_from) +
                          ' to: ' + str(chunk_to) + ': ' + chunk_file_path)
                    chunk_count = chunk_count + 1
                    accumulated_frames = []
                    chunk_from = chunk_to
        else:
            if(len(accumulated_frames) > 0):
                if(chunk_to - chunk_from > min_chunk_length):
                    chunk_file_path = chunk_folder_path + \
                        file_name + "_{:03}".format(chunk_count)+'.wav'
                    utils.write_wave(
                        chunk_file_path, accumulated_frames, sample_rate)
                    snippets.append(
                        Snippet(chunk_file_path, chunk_from, chunk_to))
                    print('Creating chunk from: ' + str(chunk_from) +
                          ' to: ' + str(chunk_to) + ': ' + chunk_file_path)
                    chunk_count = chunk_count + 1
                accumulated_frames = []
                chunk_from = chunk_to
        timestamp += duration
        offset += n
    return snippets


if __name__ == '__main__':
    print(jsonpickle.encode(vad('/home/absin/git/sentenceSimilarity/speech/audio/17897067_1.wav')))
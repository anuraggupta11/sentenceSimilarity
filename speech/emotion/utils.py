from scipy.io import wavfile
import wave
import os
import contextlib
import requests

"""Writes a .wav file.
Takes the path, and frames and writes the frame data to the path file.
"""


def write_wave(path, frames, sample_rate):
    wav_file = wave.open(path, "w")
    nchannels = 1
    sampwidth = 2
    nframes = len(frames)
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((nchannels, sampwidth, sample_rate,
                        nframes, comptype, compname))
    wav_file.writeframes(b''.join(frames))
    wav_file.close()
    #print('Created chunk file at: '+path)


"""Reads a .wav file.
Takes the path, and returns (PCM audio data, sample rate).
"""


def read_wave(path):
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        num_channels = wf.getnchannels()
        assert num_channels == 1
        sample_width = wf.getsampwidth()
        assert sample_width == 2
        sample_rate = wf.getframerate()
        assert sample_rate in (8000, 16000, 32000)
        frames = wf.getnframes()
        pcm_data = wf.readframes(frames)
        duration = frames / sample_rate
        return pcm_data, sample_rate, duration


"""Turns a dual channel file into 2 mono channeled files
Returns the absolute path of the audio files 
"""


def split_stereo(path):
    fs, data = wavfile.read(path)            # reading the file
    file_name = path.split('/')[-1]
    folder = os.path.dirname(path) + '/'
    channel_1 = folder + file_name.replace('.wav', '') + '_1.wav'
    channel_2 = folder + file_name.replace('.wav', '') + '_2.wav'
    # saving first column which corresponds to channel 1
    wavfile.write(channel_1, fs, data[:, 0])
    # saving second column which corresponds to channel 2
    wavfile.write(channel_2, fs, data[:, 1])
    print('Successfully split ' + path + ' into ' +
          channel_1 + ' and ' + channel_2)
    return [channel_1, channel_2]


def download_file(url, folder):
    local_filename = url.split('/')[-1]
    print('Downloading file ' + local_filename + ' ...')   
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(folder + local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush()
    return local_filename

if __name__ == '__main__':
    print(split_stereo('/home/absin/git/sentenceSimilarity/speech/audio/17897067.wav'))

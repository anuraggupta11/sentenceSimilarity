import os
import wave
import contextlib
import webrtcvad

class Frame(object):
    """Represents a "frame" of audio data."""
    def __init__(self, bytes, timestamp, duration):
        self.bytes = bytes
        self.timestamp = timestamp
        self.duration = duration

"""Writes a .wav file.
Takes the path, and frames and writes the frame data to the path file.
"""
def write_wave(path, frames, sample_rate):
    wav_file=wave.open(path,"w")
    nchannels = 1
    sampwidth = 2
    nframes = len(frames)
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))
    wav_file.writeframes(b''.join(frames))
    wav_file.close()
    print('Created chunk file at: '+path)
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

def performVad(filePath, chunkFolderPath):
    chunkFilePaths = []
    print('Processing '+ filePath+' for voice activity detection...')
    if os.path.isdir(chunkFolderPath) is False:
        print('Creating chunk folder at: '+chunkFolderPath)
        os.makedirs(chunkFolderPath)
    aggressiveness = 2
    min_chunk_length = 4.0
    max_chunk_length = 5.0
    directory = os.fsencode(chunkFolderPath)
    fileName = os.path.basename(filePath).replace('.wav','')
    vad = webrtcvad.Vad(aggressiveness)
    chunkCount = 0
    accumulatedFrames = []
    audio, sample_rate, audio_length = read_wave(filePath)
    assert sample_rate == 8000, "Only 8000Hz input WAV files are supported for now!"
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
            accumulatedFrames.append(audio[offset:offset + n])
            if(chunk_from == chunk_to):
                chunk_from = offset/len(audio)*audio_length
            chunk_to = (offset+n)/len(audio)*audio_length
            #if(len(accumulatedFrames)>0):
            #    if(chunk_to - chunk_from>max_chunk_length):
            #        chunkFileName = chunkFolderPath+fileName+"{:03}".format(chunkCount)+'.wav'
            #        write_wave(chunkFileName,accumulatedFrames,sample_rate)
            #        chunkFilePaths.append(chunkFileName)
            #        print('Creating chunk from: '+ str(chunk_from)  +'to: '+ str(chunk_to) +': '+ chunkFileName)
            #        chunkCount = chunkCount + 1
            #    accumulatedFrames = []
            #    chunk_from = chunk_to
        else:
            if(len(accumulatedFrames)>0):
                if(chunk_to - chunk_from>min_chunk_length):
                    chunkFileName = chunkFolderPath+fileName+"{:03}".format(chunkCount)+'.wav'
                    write_wave(chunkFileName,accumulatedFrames,sample_rate)
                    chunkFilePaths.append(chunkFileName)
                    print('Creating chunk from: '+ str(chunk_from)  +'to: '+ str(chunk_to) +': '+ chunkFileName)
                    chunkCount = chunkCount + 1
                accumulatedFrames = []
                chunk_from = chunk_to
            timestamp += duration
            offset += n
    return chunkFilePaths

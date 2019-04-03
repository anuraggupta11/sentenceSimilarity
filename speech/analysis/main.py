import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from utils import vad
from utils import misc
from utils import objects
import contextlib
import shutil
import wave
from transcription import google_transcribe
import pdb
import jsonpickle
from emotion import emotion_api
import requests

def transcribe_emotion(task_id, language, model, loaded_model, do_emotion = True):
    r = requests.get("http://db.talentify.in:5050/product?method=SIGNAL&taskId="+task_id)
    data = json.loads(r.content)
    phrases=[]
    for item in data:
    phrases.append(item['value'])
    task_folder = '/home/absin/git/sentenceSimilarity/speech/audio/tasks/'
    task_file_path = misc.download_file(
        'https://storage.googleapis.com/istar-static/'+task_id+'.wav', task_folder)
    channel_files = [task_file_path]
    # split multichannel to 2 files
    with contextlib.closing(wave.open(task_file_path, 'rb')) as wf:
        num_channels = wf.getnchannels()
        if num_channels == 2:
            channel_files = misc.split_stereo(task_file_path)
    snippets = []
    for channel_file in channel_files:
        snippets.extend(vad.perform_vad(
            channel_file, task_folder + 'chunks/', min_chunk_length=1, max_chunk_length=50))

    conversation_blocks = []

    for snippet in snippets:
        print('Transcribing: ' + snippet.path)
        speaker = 'Customer'
        if task_id + '_1' in snippet.path:
            speaker = 'Agent'
        for response in google_transcribe.transcribe_streaming(snippet.path, language, model, phrases):
            for result in response.results:
                alternatives = result.alternatives
                for alternative in alternatives:
                    conversation_block = objects.ConversationBlock(snippet.from_time, snippet.to_time, speaker, alternative.transcript, alternative.confidence)
                    for word_info in alternative.words:
                        word = word_info.word
                        start_time = word_info.start_time
                        end_time = word_info.end_time
                        word = objects.ConversationBlock(snippet.from_time + word_info.start_time.seconds + word_info.start_time.nanos * 1e-9,
                            snippet.from_time + word_info.end_time.seconds + word_info.end_time.nanos * 1e-9, speaker, word, alternative.confidence)
                        conversation_block.add_word(word)
                conversation_blocks.append(conversation_block)
        #break
    conversation_blocks.sort(key=lambda x: x.from_time, reverse=False)

    if do_emotion:
        # Now the emotional bit
        #loaded_model = emotion_api.getModel()
        #loaded_model._make_predict_function()
        snips = emotion_api.emotion(channel_files, loaded_model, task_folder, task_id)
        # empty chunks foilder
        shutil.rmtree(task_folder + task_id, ignore_errors=True)
        for emotion_snip in snips:
            emotion_snippet_located = False
            for conv in conversation_blocks:
                if conv.from_time <= emotion_snip.from_time and conv.to_time >= emotion_snip.to_time:
                    conv.add_signals(emotion_snip.signals)
                    emotion_snippet_located = True
            if emotion_snippet_located is False:
                print("Emotion snippet from " + str(emotion_snip.from_time) + " to: "
    						+ str(emotion_snip.to_time) + " not found")
    print(jsonpickle.encode(conversation_blocks))
    return conversation_blocks

def emotion(task_id, loaded_model):
    task_folder = '/home/absin/git/sentenceSimilarity/speech/audio/tasks/'
    task_file_path = misc.download_file(
        'https://storage.googleapis.com/istar-static/'+task_id+'.wav', task_folder)
    channel_files = [task_file_path]
    # split multichannel to 2 files
    with contextlib.closing(wave.open(task_file_path, 'rb')) as wf:
        num_channels = wf.getnchannels()
        if num_channels == 2:
            channel_files = misc.split_stereo(task_file_path)
    snips = emotion_api.emotion(channel_files, loaded_model, task_folder, task_id)
    print(snips)
    # empty chunks foilder
    shutil.rmtree(task_folder + task_id, ignore_errors=True)
    return snips

if __name__ == '__main__':
    task_id = '17906567'
    language = 'en-US'
    model = True
    transcribe_emotion(task_id, language, model)

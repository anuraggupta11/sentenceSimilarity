import time
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import io
from speech.utils import objects
import jsonpickle

def transcribe_streaming(stream_file, language="en-IN", model=False, phrases=["talentify"]):
    """Streams transcription of the given audio file."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    # [START speech_python_migration_streaming_request]
    with io.open(stream_file, 'rb') as audio_file:
        content = audio_file.read()

    # In practice, stream should be a generator yielding chunks of audio data.
    stream = [content]
    requests = (types.StreamingRecognizeRequest(audio_content=chunk)
                for chunk in stream)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code=language,
        use_enhanced=True,
        model='video',
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True,
        speech_contexts=[speech.types.SpeechContext(phrases=phrases)])
    if not model:
        config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code=language,
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True,
        speech_contexts=[speech.types.SpeechContext(phrases=phrases)])
    streaming_config = types.StreamingRecognitionConfig(config=config)
    conv_blocks = []
    responses = client.streaming_recognize(streaming_config, requests)
    for response in responses:
        for result in response.results:
            alternatives = result.alternatives
            for alternative in alternatives:
                conversation_block = objects.ConversationBlock(0, 0, 'speaker', alternative.transcript, alternative.confidence)
                for word_info in alternative.words:
                    word = word_info.word
                    start_time = word_info.start_time
                    end_time = word_info.end_time
                    word = objects.ConversationBlock(0 + word_info.start_time.seconds + word_info.start_time.nanos * 1e-9,
                        0 + word_info.end_time.seconds + word_info.end_time.nanos * 1e-9, 'speaker', word, alternative.confidence)
                    conversation_block.add_word(word)
            conv_blocks.append(conversation_block)
    return conv_blocks
def threaded():
    futures = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures.append(executor.submit(transcribe_streaming, '/home/absin/git/sentenceSimilarity/speech/audio/tasks/chunks/17916689_1_000.wav'))
        futures.append(executor.submit(transcribe_streaming, '/home/absin/git/sentenceSimilarity/speech/audio/tasks/chunks/17916689_1_001.wav'))
        futures.append(executor.submit(transcribe_streaming, '/home/absin/git/sentenceSimilarity/speech/audio/tasks/chunks/17916689_1_002.wav'))
        futures.append(executor.submit(transcribe_streaming, '/home/absin/git/sentenceSimilarity/speech/audio/tasks/chunks/17906563_1_000.wav'))
        futures.append(executor.submit(transcribe_streaming, '/home/absin/git/sentenceSimilarity/speech/audio/tasks/chunks/17906563_1_001.wav'))
        futures.append(executor.submit(transcribe_streaming, '/home/absin/git/sentenceSimilarity/speech/audio/tasks/chunks/17906563_1_002.wav'))
    print('Futures started')
    for future in futures:
        try:
            z = future.result(timeout=10)
            print(jsonpickle.encode(z))
        except Exception as exc:
            print(exc)
    print('Futures finished')
def unthreaded():
    transcribe_streaming('/home/absin/git/sentenceSimilarity/speech/audio/tasks/chunks/17916689_1_000.wav')
    transcribe_streaming('/home/absin/git/sentenceSimilarity/speech/audio/tasks/chunks/17916689_1_001.wav')
    transcribe_streaming('/home/absin/git/sentenceSimilarity/speech/audio/tasks/chunks/17916689_1_002.wav')
    transcribe_streaming('/home/absin/git/sentenceSimilarity/speech/audio/tasks/chunks/17906563_1_000.wav')
    transcribe_streaming('/home/absin/git/sentenceSimilarity/speech/audio/tasks/chunks/17906563_1_001.wav')
    transcribe_streaming('/home/absin/git/sentenceSimilarity/speech/audio/tasks/chunks/17906563_1_002.wav')
if __name__ == '__main__':
    start = time.time()
    #threaded()
    unthreaded()
    print('Time taken: '+str(time.time() - start))

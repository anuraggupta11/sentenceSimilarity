import io

# [START speech_transcribe_streaming]
def transcribe_streaming(stream_file, language, model, phrases):
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
        # Enhanced models are only available to projects that
        # opt in for audio data collection.
        use_enhanced=True,
        # A model must be specified to use enhanced model.
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

    # streaming_recognize returns a generator.
    # [START speech_python_migration_streaming_response]
    responses = client.streaming_recognize(streaming_config, requests)
    # [END speech_python_migration_streaming_request]
    return responses
    #for response in responses:
        # Once the transcription has settled, the first result will contain the
        # is_final result. The other results will be for subsequent portions of
        # the audio.
    #    for result in response.results:
            #print('Finished: {}'.format(result.is_final))
            #print('Stability: {}'.format(result.stability))
   #         alternatives = result.alternatives
            # The alternatives are ordered from most likely to least.
    #        for alternative in alternatives:
                #print('Confidence: {}'.format(alternative.confidence))
                #print(u'Transcript: {}'.format(alternative.transcript))
    #            for word_info in alternative.words:
    #                word = word_info.word
     #               start_time = word_info.start_time
      #              end_time = word_info.end_time
                    #print('Word: {}, start_time: {}, end_time: {}'.format(word,start_time.seconds + start_time.nanos * 1e-9,end_time.seconds + end_time.nanos * 1e-9))
    #return responses
    # [END speech_python_migration_streaming_response]
# [END speech_transcribe_streaming]

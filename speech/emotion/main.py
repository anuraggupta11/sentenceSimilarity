import argparse
import vad as vad
import utils as utils
import librosa
import numpy as np
import pandas as pd
import os
from keras.models import model_from_json
import jsonpickle
import shutil
from flask import Flask
from flask import request
import time
import tensorflow as tf

def getModel():
    json_file = open('models/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("models/Emotion_Voice_Detection_Model.h5")
    print("Loaded model and weights from disk")
    return loaded_model


def getEmotionPredictionChunk(f, loaded_model):
    labels = ['female_angry', 'female_calm', 'female_fearful', 'female_happy',
              'female_sad', 'male_angry', 'male_calm', 'male_fearful', 'male_happy', 'male_sad']
    X, sample_rate = librosa.load(
        f, res_type='kaiser_fast', duration=2.5, sr=22050*2, offset=0)
    sample_rate = np.array(sample_rate)
    mfccs = np.mean(librosa.feature.mfcc(
        y=X, sr=sample_rate, n_mfcc=13), axis=0)
    featurelive = mfccs
    livedf2 = featurelive
    livedf2 = pd.DataFrame(data=livedf2)
    livedf2 = livedf2.stack().to_frame().T
    twodim = np.expand_dims(livedf2, axis=2)
    livepreds = loaded_model.predict(twodim,
                                     batch_size=32,
                                     verbose=1)
    livepreds1 = livepreds.argmax(axis=1)
    return labels[livepreds1[0]], str(livepreds[0][livepreds1[0]])


def emotion(task_id):
    tf.keras.backend.clear_session()
    folder = '/home/absin/git/sentenceSimilarity/speech/audio/tasks/'+task_id+'/'
    if os.path.exists(folder) and os.path.isdir(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)
    # Download the task audio
    dual_channel_file = utils.download_file(
        'https://storage.googleapis.com/istar-static/' + str(task_id) + '.wav', folder)
    files = utils.split_stereo(folder + dual_channel_file)
    agent_snippets = vad.vad(files[0])
    cust_snippets = vad.vad(files[1])
    for snippet in agent_snippets:
        predicted, score = getEmotionPredictionChunk(
            snippet.path, loaded_model)
        snippet.add_emotion(predicted, score)
        if float(score) > 0.6:
            print('Agent: For time: ' + str(snippet.from_time) + ' to time: ' +
                  str(snippet.to_time) + ' Predicted label - > ' + predicted + ' with score -> ' + score + ' on file: ' + snippet.path)
    for snippet in cust_snippets:
        predicted, score = getEmotionPredictionChunk(
            snippet.path, loaded_model)
        snippet.add_emotion(predicted, score)
        if float(score) > 0.6:
            print('Customer: For time: ' + str(snippet.from_time) + ' to time: ' +
                  str(snippet.to_time) + ' Predicted label - > ' + predicted + ' with score -> ' + score + ' on file: ' + snippet.path)
    snips = agent_snippets + cust_snippets
    snips.sort(key=lambda x: x.from_time, reverse=False)
    shutil.rmtree(folder)
    return jsonpickle.encode(snips)


app = Flask(__name__)
loaded_model = getModel()
loaded_model._make_predict_function()


@app.route("/", methods=['GET', 'POST'])
def hello():
    start = time.time()
    task_id = request.args['task_id']
    snips = emotion(task_id)
    print('Emotion recognition of task(' + task_id +
          ') done after: '+str(time.time()-start))
    return snips


if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description='Get task Id')
    #parser.add_argument("task_id", type=int, help="the task id")
    #args = parser.parse_args()
    #task_id = args.task_id
    app.run(debug=True, threaded=False, host='0.0.0.0', port='5010')

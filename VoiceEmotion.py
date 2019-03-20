from keras.models import model_from_json
import os
import pandas as pd
import librosa
import glob
import numpy as np
import utils as utils
chunkFolderPath='/home/absin/git/sematicSimilarity/audio/chunks/'
filePath='/home/absin/git/sematicSimilarity/audio/17895363_right.wav'
doPerformVad = True
json_file = open('models/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("models/Emotion_Voice_Detection_Model.h5")
print("Loaded model from disk")
if doPerformVad:
    chunks = utils.performVad(filePath, chunkFolderPath)
else:
    chunks = [filePath]

for chunk in chunks:
    X, sample_rate = librosa.load(chunk, res_type='kaiser_fast',duration=2.5,sr=22050*2,offset=0.5)
    sample_rate = np.array(sample_rate)
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=13),axis=0)
    featurelive = mfccs
    livedf2 = featurelive
    livedf2= pd.DataFrame(data=livedf2)
    livedf2 = livedf2.stack().to_frame().T
    twodim= np.expand_dims(livedf2, axis=2)
    livepreds = loaded_model.predict(twodim,
                             batch_size=32,
                             verbose=1)
    livepreds1=livepreds.argmax(axis=1)
    liveabc = livepreds1.astype(int).flatten()
    predictionHolder = ["female_angry","female_calm","female_fearful","female_happy","female_sad","male_angry","male_calm","male_fearful","male_happy","male_sad"]
    if livepreds[0,liveabc[0]] > 0.8:
        print(chunk+'-->'+predictionHolder[liveabc[0]]+' with confidence: '+str(livepreds[0,liveabc[0]]))
    else:
        #print('')
        os.remove(chunk)

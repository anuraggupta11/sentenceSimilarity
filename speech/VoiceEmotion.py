from keras.models import model_from_json
import os
import pandas as pd
import librosa
import glob
import numpy as np
import utils as utils

json_file = open('models/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("models/Emotion_Voice_Detection_Model.h5")
print("Loaded model from disk")

def performVoiceEmotionOneFile(filePath, chunkFolderPath, doPerformVad):
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
            #print(chunk+'-->'+predictionHolder[liveabc[0]]+' with confidence: '+str(livepreds[0,liveabc[0]]))
            return predictionHolder[liveabc[0]], str(livepreds[0,liveabc[0]])
        else:
            os.remove(chunk)
            return predictionHolder[liveabc[0]], str(livepreds[0,liveabc[0]])

def getEmotionTypeFromFileName(item):
    expected = ''
    #if item[6:-16]=='01' and int(item[18:-4])%2==0:
    #    expected = 'female_neutral'
    #elif item[6:-16]=='01' and int(item[18:-4])%2==1:
    #    expected = 'male_neutral'
    if item[6:-16]=='02' and int(item[18:-4])%2==0:
        expected = 'female_calm'
    elif item[6:-16]=='02' and int(item[18:-4])%2==1:
        expected = 'male_calm'
    elif item[6:-16]=='03' and int(item[18:-4])%2==0:
        expected = 'female_happy'
    elif item[6:-16]=='03' and int(item[18:-4])%2==1:
        expected = 'male_happy'
    elif item[6:-16]=='04' and int(item[18:-4])%2==0:
        expected = 'female_sad'
    elif item[6:-16]=='04' and int(item[18:-4])%2==1:
        expected = 'male_sad'
    elif item[6:-16]=='05' and int(item[18:-4])%2==0:
        expected = 'female_angry'
    elif item[6:-16]=='05' and int(item[18:-4])%2==1:
        expected = 'male_angry'
    elif item[6:-16]=='06' and int(item[18:-4])%2==0:
        expected = 'female_fearful'
    elif item[6:-16]=='06' and int(item[18:-4])%2==1:
        expected = 'male_fearful'
    #elif item[6:-16]=='07' and int(item[18:-4])%2==0:
    #    expected = 'female_disgust'
    #elif item[6:-16]=='07' and int(item[18:-4])%2==1:
    #    expected = 'male_disgust'
    #elif item[6:-16]=='08' and int(item[18:-4])%2==0:
    #    expected = 'female_surprised'
    #elif item[6:-16]=='08' and int(item[18:-4])%2==1:
    #    expected = 'male_surprised'
    return expected

if __name__ == "__main__":
    folderPath = '/home/absin/git/sematicSimilarity/RawData'
    chunkFolderPath='/home/absin/git/sematicSimilarity/audio/chunks/'
    #filePath='/home/absin/git/sematicSimilarity/audio/17895363_right.wav'
    #doPerformVad = True
    totalCount = 0
    successCount = 0
    folderPath='/home/absin/git/sematicSimilarity/RawData/'
    doPerformVad = False
    for f in os.listdir(folderPath):
        try:
            actual, score = performVoiceEmotionOneFile(folderPath+f, chunkFolderPath, doPerformVad)
            expected = getEmotionTypeFromFileName(f)
            print(f+' was computer for emotion --> '+actual+' against reality --> '+expected+' with confidence: '+str(score))
            if len(expected)>0:
                totalCount += 1
                if actual == expected:
                    successCount += 1
        except:
            print("An exception occurred with "+f)
    print("Final result: "+str(successCount)+" out of "+str(totalCount))

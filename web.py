from flask import Flask
from flask import request
from flask import jsonify
from text import sentence_similarity as sentence_similarity_api
from speech.analysis import main as analysis_api
from speech.emotion import emotion_api
import jsonpickle
import redis

app = Flask(__name__)
loaded_model = ""
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
#loaded_model = emotion_api.getModel()
#loaded_model._make_predict_function()

@app.route("/sentence_similarity", methods=['GET', 'POST'])
def sentence_similarity():
    sentence1 = request.form['sentence1']
    sentence2 = request.form['sentence2']
    return jsonify(sentence1=sentence1, sentence2=sentence2, similarityScore=str(sentence_similarity_api.ss(sentence1, sentence2)))

@app.route("/transcibe", methods=['GET', 'POST'])
def transcibe():
    task_id = request.args['task_id']
    language = request.args['language']
    model = (request.args['model'] == 'True')
    print('Started: '+task_id)
    conversation_blocks = analysis_api.transcribe_emotion(task_id, language, model, loaded_model, pool, False)
    print('Finished: '+task_id)
    return jsonpickle.encode(conversation_blocks)

@app.route("/transcibe_emotion", methods=['GET', 'POST'])
def transcibe_emotion():
    task_id = request.args['task_id']
    language = request.args['language']
    model = (request.args['model'] == 'True')
    conversation_blocks = analysis_api.transcribe_emotion(task_id, language, model, loaded_model, pool)
    return jsonpickle.encode(conversation_blocks)

@app.route("/emotion", methods=['GET', 'POST'])
def emotion():
    task_id = request.args['task_id']
    emotion_blocks = analysis_api.emotion(task_id, loaded_model)
    return jsonpickle.encode(emotion_blocks)

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port='5010')

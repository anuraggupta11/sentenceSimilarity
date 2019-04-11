from flask import Flask
from flask import request
from flask import jsonify
from flask import send_from_directory
from text import sentence_similarity as sentence_similarity_api
from speech.analysis import main as analysis_api
from speech.emotion import emotion_api
import jsonpickle
import redis
from speech.transcription.transfer_learning import chunk_data_api as chunk_api
app = Flask(__name__)
loaded_model = None
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

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
    engine = request.args['engine']
    if engine is None:
        engine = 'google'
    print('Started: '+task_id)
    conversation_blocks = analysis_api.transcribe_emotion(engine, task_id, language, model, loaded_model, pool, False)
    print('Finished: '+task_id)
    return jsonpickle.encode(conversation_blocks)

@app.route("/transcibe_emotion", methods=['GET', 'POST'])
def transcibe_emotion():
    task_id = request.args['task_id']
    language = request.args['language']
    model = (request.args['model'] == 'True')
    engine = request.args['engine']
    if engine is None:
        engine = 'google'
    conversation_blocks = analysis_api.transcribe_emotion(engine, task_id, language, model, loaded_model, pool)
    return jsonpickle.encode(conversation_blocks)

@app.route("/emotion", methods=['GET', 'POST'])
def emotion():
    task_id = request.args['task_id']
    global loaded_model
    if loaded_model is None:
        loaded_model = emotion_api.getModel()
        loaded_model._make_predict_function()
    emotion_blocks = analysis_api.emotion(task_id, loaded_model)
    return jsonpickle.encode(emotion_blocks)

@app.route("/chunks", methods=['GET', 'POST'])
def chunks():
    page = request.args['page']
    chunks = chunk_api.fetch_chunks(page)
    return jsonpickle.encode(chunks)

@app.route("/verify_chunk", methods=['GET', 'POST'])
def verify_chunk():
    chunk_id = request.args['chunk_id']
    is_verified = request.args['is_verified'].lower().startswith('t')
    chunks = chunk_api.mark_chunk_as_verified(chunk_id, is_verified)
    return jsonpickle.encode(chunks)

@app.route("/update_chunk_transcription", methods=['GET', 'POST'])
def update_chunk_transcription():
    chunk_id = request.args['chunk_id']
    transcript = request.args['transcript']
    print("New: "+transcript)
    chunks = chunk_api.update_chunk_transcription(chunk_id, transcript)
    return jsonpickle.encode(chunks)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/audio/<path:path>')
def send_static_audio(path):
    return send_from_directory('speech/transcription/transfer_learning/chunks', path)

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port='5010')

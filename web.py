from flask import Flask
from flask import request
from flask import jsonify
from text import sentence_similarity as sentence_similarity_api
from speech.analysis import main as analysis_api
import jsonpickle

app = Flask(__name__)


@app.route("/sentence_similarity", methods=['GET', 'POST'])
def sentence_similarity():
    sentence1 = request.form['sentence1']
    sentence2 = request.form['sentence2']
    return jsonify(sentence1=sentence1, sentence2=sentence2, similarityScore=str(sentence_similarity_api.ss(sentence1, sentence2)))

@app.route("/transcibe_emotion", methods=['GET', 'POST'])
def transcibe_emotion():
    task_id = request.args['task_id']
    language = request.args['language']
    model = (request.args['model'] == 'True')
    conversation_blocks = analysis_api.transcribe_emotion(task_id, language, model)
    return jsonpickle.encode(conversation_blocks)

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port='5010')
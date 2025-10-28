from flask import Flask, jsonify, request
from flask_cors import CORS
import os, json

app = Flask(__name__)  
CORS(app)
DATA_FOLDER = os.path.join(os.path.dirname(__file__), 'data')

def load_data(filename):
    filepath = os.path.join(DATA_FOLDER, filename)
    with open(filepath, 'r', encoding="utf-8") as f:
        return json.load(f)

@app.route("/note_reading/<difficulty>")
def note_reading(difficulty):
    questions = load_data('note_reading.json')
    difficulty_order = [ 'bronze', 'silver', 'gold', 'maestro' ]
    try:
        index = difficulty_order.index(difficulty)
    except ValueError:
        return jsonify({"error": "Invalid difficulty"}), 400
    included_difficulties = difficulty_order[:index + 1]
    selected_questions = [ q for q in questions if q['difficulty'] in included_difficulties ]
    return jsonify(selected_questions)

@app.route("/chord_analysis/<difficulty>")
def chord_analysis(difficulty):
    questions = load_data('chord_analysis.json')
    difficulty_order = [ 'bronze', 'silver', 'gold', 'maestro' ]
    try:
        index = difficulty_order.index(difficulty)
    except ValueError:
        return jsonify({"error": "Invalid difficulty"}), 400
    included_difficulties = difficulty_order[:index + 1]
    selected_questions = [ q for q in questions if q['difficulty'] in included_difficulties ]
    return jsonify(selected_questions)

@app.route("/scales/<difficulty>")
def scales(difficulty):
    questions = load_data('scales.json')
    difficulty_order = [ 'bronze', 'silver', 'gold', 'maestro' ]
    try:
        index = difficulty_order.index(difficulty)
    except ValueError:
        return jsonify({"error": "Invalid difficulty"}), 400
    included_difficulties = difficulty_order[:index + 1]
    selected_questions = [ q for q in questions if q['difficulty'] in included_difficulties ]
    return jsonify(selected_questions)

if __name__ == '__main__':
    app.run(debug=True)
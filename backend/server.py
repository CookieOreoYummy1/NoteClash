from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os, json

app = Flask(__name__)  
CORS(app)
DATA_FOLDER = os.path.join(os.path.dirname(__file__), 'data')

# Incase leaderboard file doesn't exist, creates it
leaderboard_file = os.path.join(DATA_FOLDER, 'leaderboard.json')
if not os.path.exists(leaderboard_file):
    with open(leaderboard_file, 'w', encoding="utf-8") as f:
        json.dump([], f)

def load_data(filename):
    filepath = os.path.join(DATA_FOLDER, filename)
    with open(filepath, 'r', encoding="utf-8") as f:
        return json.load(f)


# Define routes for different question types
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

#POST route to submit scores
@app.route("/submit_score", methods=['POST'])
def submit():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    user = data.get('user')
    famous_musicians = ['Chopin', 'Liszt', 'Mozart', 'Beethoven', 'Bach', 
                       'Debussy', 'Tchaikovsky', 'Rachmaninoff', 'Vivaldi', 
                       'Brahms', 'Handel', 'Haydn', "Schubert", "Schumann", 
                       "Mendelssohn", "Grieg", "Dvorak", "Paganini", "Sibelius",
                       "Saint-Saens"]
    
    if user in famous_musicians:
        return jsonify({"error": "You can't use a famous musician's name!"}), 400

    accuracy = data.get('accuracy')
    time_taken = data.get('time_taken')

    if user is None or accuracy is None or time_taken is None:
        return jsonify({"error": "Missing fields in data"}), 400

    #***reminder to save score to database later if possible***

    if time_taken < 0 or accuracy < 0 or accuracy > 100:
        return jsonify({"error": "Invalid values"}), 400
    
    rr = accuracy * 1000 / (time_taken + 1) 


    leaderboard_file = os.path.join(DATA_FOLDER, 'leaderboard.json')
    try:
        with open(leaderboard_file, 'r', encoding="utf-8") as f:
            leaderboard = json.load(f)
    except FileNotFoundError:
            leaderboard = []
    
    user_entry = None
    for entry in leaderboard:
        if entry['user'] == user:
            user_entry = entry
            break

    if user_entry:
        user_entry['sessions'] += 1
        user_entry['total_accuracy'] += accuracy
        user_entry['accuracy'] = user_entry['total_accuracy'] / user_entry['sessions']
        user_entry['total_time'] += time_taken
        user_entry['time_taken'] = user_entry['total_time'] / user_entry['sessions']
        user_entry['total_rr'] += rr

        #Divisions based on total RR
        if user_entry['total_rr'] >= 800:
            user_entry['difficulty'] = 'maestro'
        elif user_entry['total_rr'] >= 600:
            user_entry['difficulty'] = 'gold'
        elif user_entry['total_rr'] >= 400:
            user_entry['difficulty'] = 'silver'
        else:
            user_entry['difficulty'] = 'bronze'
        
    else:
        leaderboard.append({
            "user": user,
            "sessions": 1,
            "total_accuracy": accuracy,
            "accuracy": accuracy,
            "total_time": time_taken,
            "time_taken": time_taken,
            "total_rr": rr,
            'difficulty': 'bronze'
        })

    with open(leaderboard_file, 'w', encoding="utf-8") as f:
        json.dump(leaderboard, f, indent=4)

    return jsonify({"message": "Score submitted"})

#GET route for leaderboard
@app.route("/leaderboard")
def leaderboard():
    leaderboard_file = os.path.join(DATA_FOLDER, 'leaderboard.json')
    try:
        with open(leaderboard_file, 'r', encoding="utf-8") as f:
            leaderboard = json.load(f)
    except FileNotFoundError:
        leaderboard = []

# Sorts by RR descending
    leaderboard.sort(key=lambda x: x.get('total_rr', 0), reverse=True)
    leaderboard = leaderboard[:10]
        
    return jsonify(leaderboard)
    

if __name__ == '__main__':
    app.run(debug=True)
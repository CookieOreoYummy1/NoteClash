import json

chord_types = {
    "bronze": ["Major"],
    "silver": ["Minor"],
    "gold": ["Augmented", "Diminished"],
    "maestro": ["Dominant7", "Minor7", "Major7", "Dim7", "HalfDim7"]
}


timers = {
    "bronze": 50,
    "silver": 40,
    "gold": 35,
    "maestro": 30
}

division_clefs = {
    "bronze": ["treble"],
    "silver": ["treble", "bass"],
    "gold": ["treble", "bass", "alto"],
    "maestro": ["treble", "bass", "alto", "tenor"]
}


notes = ["Ab", "A", "Bb", "B", "C",  "Db", "D", "Eb", "E", "F", "F#", "Gb", "G",]
accidental_map = {
    "Ab": "Aflat",
    "Bb": "Bflat",
    "Db": "Dflat",
    "Eb": "Eflat",
    "F#": "Fsharp",
    "Gb": "Gflat",
}

questions = []

#Loops over everything and makes JSON entries, sorry for ultra nested loop :p
for difficulty, clefs in division_clefs.items():
    for clef in clefs:
        for chord in chord_types[difficulty]:
            for base_note in notes:
                if base_note in accidental_map:
                    safe_note = accidental_map[base_note]
                else:
                    safe_note = base_note
                image_file = f"images/chords/{clef}note_{safe_note}_{chord}.svg"
                questions.append({
                    "question": "Identify the note shown",
                     "image": image_file,
                     "answer": f"{base_note} {chord}",
                     "clef": clef,
                     "difficulty": difficulty,
                     "timers": timers
                    })

with open("chord_analysis.json", "w") as f:
    json.dump(questions, f, indent=4)

print("JSON with accidentals generated successfully!")

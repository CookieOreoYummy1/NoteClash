import json

clef_notes = {
    "treble": ["A4","A5", "B4", "B5", "C4" "C5", "D5", "E5", "F4", "F5", "G4", "G5"],
    "bass": ["A2","A3", "B2", "B3", "C3", "C4", "D3", "D4", "E2", "E3", "E4", "F2", "F3", "F4", "G2", "G3"],
    "alto": ["A3", "B3", "C4", "D4", "E4", "F4", "G4"],
    "tenor": ["A3", "B3", "C4", "D4", "E4", "F4", "G4"]
}

timers = {
    "bronze": 13,
    "silver": 10,
    "gold": 7,
    "maestro": 6
}

division_clefs = {
    "bronze": ["treble"],
    "silver": ["treble", "bass"],
    "gold": ["treble", "bass", "alto"],
    "maestro": ["treble", "bass", "alto", "tenor"]
}


accidentals = ["", "#", "b"]
accidental_map = {"": "", "#": "sharp", "b": "flat"}

questions = []

#Loops over everything and makes JSON entries, sorry for ultra nested loop :p
for difficulty, clefs in division_clefs.items():
    for clef in clefs:
        for base_note in clef_notes[clef]:
            for accidental in accidentals if difficulty != "bronze" else [""]:
                note_name = base_note[0] + accidental
                filename_accidental = accidental_map[accidental]
                image_file = f"images/notes/{clef}note_{base_note[0].lower()}{filename_accidental}.svg"
                questions.append({
                    "question": "Identify the note shown",
                    "image": image_file,
                    "answer": note_name,
                    "clef": clef,
                    "difficulty": difficulty,
                    "timers": timers
                })

with open("note_reading.json", "w") as f:
    json.dump(questions, f, indent=4)

print("JSON with accidentals generated successfully!")

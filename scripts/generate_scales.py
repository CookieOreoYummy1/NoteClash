import json

scale_types = {
    "bronze": ["Major_scale"],
    "silver": ["Natural_minor"],
    "gold": ["Melodic_minor", "Harmonic_minor"],
    "maestro": ["Mixolydian", "Lydian", "Dorian", "Phrygian", "Locrian"]
}


timers = {
    "bronze": 35,
    "silver": 30,
    "gold": 25,
    "maestro": 15
}

division_clefs = {
    "bronze": ["treble"],
    "silver": ["treble", "bass"],
    "gold": ["treble", "bass"],
    "maestro": ["treble", "bass"]
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
        for scale in scale_types[difficulty]:
            for base_note in notes:
                if base_note in accidental_map:
                    safe_note = accidental_map[base_note]
                else:
                    safe_note = base_note
                image_file = f"images/scales/{clef}note_{safe_note}_{scale}.png"
                questions.append({
                    "question": "Identify the note shown",
                     "image": image_file,
                     "answer": f"{base_note} {scale}",
                     "clef": clef,
                     "difficulty": difficulty,
                     "timers": timers
                    })

with open("scales.json", "w") as f:
    json.dump(questions, f, indent=4)

print("JSON with accidentals generated successfully!")
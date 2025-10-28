from music21 import environment, note, stream, clef, meter, key, scale, chord, interval
import os

us = environment.UserSettings()
us['lilypondPath'] = r'C:\Users\Victor Van\Documents\lilypond-2.24.4-mingw-x86_64\lilypond-2.24.4\bin\lilypond.exe'  

folders = [
    "images/notes",
    "images/chords",
    "images/scales"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

#Notes & Chord Analysis use same clefs
note_clefs = {
    "treble": clef.TrebleClef(),
    "bass": clef.BassClef(),
    "alto": clef.AltoClef(),
    "tenor": clef.TenorClef()
}

scale_clefs = {
    "treble": clef.TrebleClef(),
    "bass": clef.BassClef()
}

notes_reading = ["A", "Ab", "A#", "Bb", "B", "B#", "Cb", "C", "C#", "Db", "D", "D#", "Eb", "E", "E#", "Fb","F", "F#", "Gb", "G", "G#",]
notes_chords = ["Ab", "A", "Bb", "B", "C",  "Db", "D", "Eb", "E", "F", "F#", "Gb", "G",]
notes_scales = ["Ab", "A", "Bb", "B", "C",  "Db", "D", "Eb", "E", "F", "F#", "Gb", "G",]

accidentals = {
    "Bb": "Bflat",
    "Db": "Dflat",
    "Eb": "Eflat",
    "F#": "Fsharp",
    "Gb": "Gflat",
    "Ab": "Aflat",
    "A#": "Asharp",
    "B#": "Bsharp",
    "Cb": "Cflat",
    "C#": "Csharp",
    "D#": "Dsharp",
    "E#": "Esharp",
    "Fb": "Fflat",
    "G#": "Gsharp",
}

chord_types = {
    "bronze": ["Major"],
    "silver": ["Minor"],
    "gold": ["Augmented", "Diminished"],
    "maestro": ["Dominant7", "Minor7", "Major7", "Dim7", "HalfDim7"]
}

scale_types = {
    "bronze": ["Major_scale"],
    "silver": ["Natural_minor"],
    "gold": ["Melodic_minor", "Harmonic_minor"],
    "maestro": ["Mixolydian", "Lydian", "Dorian", "Phrygian", "Locrian"]
}

# Functions to generate images
#---------------------------------

def generate_note():
    for clef_name, clef_obj in note_clefs.items():
        for n in notes_reading:
            s = stream.Stream()
            s.append(clef_obj) 
            s.append(note.Note(n))
            filename_note = accidentals.get(n, n).lower()
            filename = f"images/notes/{clef_name.lower()}note_{filename_note}"
            s.write('lily.png', fp=filename)
            print(f"Generated {filename}")

def generate_chord():
    for clef_name, clef_obj in note_clefs.items():
        for difficulty, types in chord_types.items():
            for n in notes_chords:
                for ctypes in types:
                    s = stream.Stream()
                    s.append(clef_obj) 
                    base_note = note.Note(n)

        
                    if ctypes == "Major":
                        intervals = ['M3', 'P5']
                    elif ctypes == "Minor":
                        intervals = ['m3', 'P5']
                    elif ctypes == "Augmented":
                        intervals = ['M3', 'A5']
                    elif ctypes == "Diminished":
                        intervals = ['m3', 'd5']
                    elif ctypes == "Dominant7":
                        intervals = ['M3', 'P5', 'm7']
                    elif ctypes == "Minor7":
                        intervals = ['m3', 'P5', 'm7']
                    elif ctypes == "Major7":
                        intervals = ['M3', 'P5', 'M7']
                    elif ctypes == "Dim7":
                        intervals = ['m3', 'd5', 'd7']
                    else:  # HalfDim7
                        intervals = ['m3', 'd5', 'm7']

                    # build the chord 
                    chord_notes = [base_note] + [interval.Interval(i).transposeNote(base_note) for i in intervals]
                    c = chord.Chord(chord_notes)
                    s.append(c)

                    filename_note = accidentals.get(n, n)
                    filename = f"images/chords/{clef_name}note_{filename_note}_{ctypes}"

                    try:
                        s.write("lily.png", fp=filename)
                        print(f"Generated {filename}")
                    except Exception as e:
                        print(f"Error generating {filename}: {e}")

def generate_scale():
    for clef_name, clef_obj in scale_clefs.items():
        for difficulty, types in scale_types.items():
            for n in notes_scales:
                for scale_type in types:
                    s = stream.Stream()
                    s.append(clef_obj) 

                    octave = 4 if clef_name == "treble" else 3
                    root = note.Note(f"{n}{octave}")

                    if scale_type == "Major_scale":
                        sc = scale.MajorScale(root.pitch)
                    elif scale_type == "Natural_minor":
                        sc = scale.MinorScale(root.pitch)
                    elif scale_type == "Melodic_minor":
                        sc = scale.MelodicMinorScale(root.pitch)
                    elif scale_type == "Harmonic_minor":
                        sc = scale.HarmonicMinorScale(root.pitch)
                    elif scale_type == "Mixolydian":
                        sc = scale.MixolydianScale(root.pitch)
                    elif scale_type == "Lydian":
                        sc = scale.LydianScale(root.pitch)
                    elif scale_type == "Dorian":
                        sc = scale.DorianScale(root.pitch)
                    elif scale_type == "Phrygian":
                        sc = scale.PhrygianScale(root.pitch)
                    else:  # Locrian
                        sc = scale.LocrianScale(root.pitch)

                    scale_pitches = sc.getPitches(root.pitch, root.pitch.transpose(12))
                    for p in scale_pitches:
                        s.append(note.Note(p))

                    filename_note = accidentals.get(n, n)
                    filename = f"images/scales/{clef_name}note_{filename_note}_{scale_type}"
                    s.write("lily.png", fp=filename)
                    print(f"Generated {filename}")



generate_scale()
generate_chord()
generate_note()
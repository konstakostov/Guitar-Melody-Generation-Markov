import numpy as np
import os.path
import re
from datasets import load_dataset
from pychord import Chord

from Utils.Chroma_Chords_Generation.chord_sort_key import chord_sort_key
from Utils.Chroma_Chords_Generation.manual_chord_to_chroma import manual_chord_to_chroma
from Utils.path_constants import CHROMA_CHORDS_PATH
from Utils.variable_constants import NOTE_TO_SEMITONE

def generate_chroma_chords_from_dataset():
    """
    Generates chroma vectors from Chordonomicon dataset using pychord library.
    """
    print("Loading Chordonomicon dataset...")
    dataset = load_dataset("ailsntua/Chordonomicon")
    chord_data = dataset['train'] if 'train' in dataset else dataset[list(dataset.keys())[0]]

    # Extract all chord symbols from progressions
    all_chord_symbols = set()

    print(f"Extracting chords from {len(chord_data)} songs...")

    for item in chord_data:
        chord_progression = item['chords']
        # Extract chord symbols (letters + optional sharps/flats + chord types)
        chord_symbols = re.findall(
            r"[A-G][#b]?(?:maj7?|min7?|m7?|7|dim|aug|sus[24]?|add\d+|\/[A-G][#b]?)?",
            chord_progression)

        all_chord_symbols.update(chord_symbols)

    print(f"Found {len(all_chord_symbols)} unique chord symbols")

    chord_to_chroma = {}

    for chord_symbol in all_chord_symbols:
        try:
            # Try pychord first
            chord = Chord(chord_symbol)
            chroma = np.zeros(12)
            for note in chord.components():
                chroma[NOTE_TO_SEMITONE[str(note)]] = 1
            chord_to_chroma[chord_symbol] = chroma
        except:
            # Try manual parsing for unsupported chords
            chroma = manual_chord_to_chroma(chord_symbol)
            if chroma is not None:
                chord_to_chroma[chord_symbol] = chroma
            else:
                print(f"Could not parse chord: {chord_symbol}")

    # Convert to arrays
    names = sorted(chord_to_chroma.keys(), key=chord_sort_key)
    chromas = np.array([chord_to_chroma[name] for name in names])

    # Normalize templates for consistent comparison
    chromas_normalized = np.array([
        chroma / np.linalg.norm(chroma) if np.linalg.norm(chroma) > 0 else chroma
        for chroma in chromas
    ])

    # Save both raw and normalized templates
    chords_file = os.path.join(CHROMA_CHORDS_PATH, "chordonomicon_templates.npz")
    np.savez_compressed(chords_file,
                        names=names,
                        chromas=chromas,
                        chromas_normalized=chromas_normalized)

    print(f"Saved {len(names)} chord templates")
    return names, chromas


if __name__ == "__main__":
    generate_chroma_chords_from_dataset()

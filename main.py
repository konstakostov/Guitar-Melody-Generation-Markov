import os
import json

from Utils.Midi_Utils.chords_sequence_to_midi import chord_sequence_to_midi
from Utils.Midi_Utils.play_midi import play_midi
from Utils.generate_music_sequence import generate_music_sequence
from Utils.path_constants import CHORD_SEQUENCES_PATH, MIDI_SEQUENCES_PATH

"""
This script demonstrates the workflow for generating a music sequence, converting it to MIDI, and playing the result.

Modules:
    - chords_sequence_to_midi: Converts a chord sequence to a MIDI file.
    - play_midi: Plays a MIDI file.
    - generate_music_sequence: Generates a chord sequence based on input parameters.
    - path_constants: Provides paths for chord and MIDI sequences.

Chordonomicon Genres:
    - "alternative", 
    - "country", 
    - "electronic", 
    - "jazz", 
    - "metal", 
    - "pop", 
    - "pop rock",
    - "punk", 
    - "rap", 
    - "reggae", 
    - "rock", 
    - "soul"

Midi_Utils Instruments:
    - Acoustic Grand Piano: 0
    - Bright Acoustic Piano: 1
    - Electric Grand Piano: 2
    - Honky-tonk Piano: 3
    - Electric Piano 1: 4
    - Electric Piano 2: 5
    - Acoustic Guitar (nylon): 24
    - Acoustic Guitar (steel): 25
    - Electric Guitar (jazz): 26
    - Electric Guitar (clean): 27
    - Electric Guitar (muted): 28
    - Overdriven Guitar: 29
    - Distortion Guitar: 30
    - Guitar harmonics: 31
"""

# Path to the chord sequence JSON file
file_path = os.path.join(CHORD_SEQUENCES_PATH, "sequence_20250827_134619_2237269e57f94d699c2790bd0e1b6e4d.json")

# Load chord sequence data from JSON file
with open(file_path, "r") as f:
    data = json.load(f)

# Extract input and generated chord sequences from the loaded data
input_sequence = data.get("input_sequence", [])
generated_sequence = data.get("generated_sequence", [])

if __name__ == "__main__":
    """
    Main execution block.

    Steps:
        1. Generate a music sequence using specified parameters.
        2. Convert the generated chord sequence to a MIDI file.
        3. Play the generated MIDI file.
    """

    # Generate a music sequence with specified parameters
    generate_music_sequence(
        in_seq=[],
        in_len=6,
        out_len=20,
        m_genre="jazz"
    )

    # Convert the generated chord sequence to MIDI
    # sequence_type can be "generated" or "input"
    chord_sequence_to_midi(
        json_path=file_path,
        sequence=generated_sequence,
        sequence_type="generated",
        duration=0.5,
        velocity=100,
        program=26
    )

    # Play the generated MIDI file
    play_midi(
        midi_file_path = os.path.join(MIDI_SEQUENCES_PATH, "sequence_20250827_134619_2237269e57f94d699c2790bd0e1b6e4d_generated.mid")
    )

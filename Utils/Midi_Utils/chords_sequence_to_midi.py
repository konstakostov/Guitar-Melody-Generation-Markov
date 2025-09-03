import os
import music21
import pretty_midi

from Utils.path_constants import MIDI_SEQUENCES_PATH


def chord_sequence_to_midi(json_path, sequence, sequence_type, duration=0.5, velocity=100, program=0):
    """
    Convert a sequence of chord symbols to a MIDI file.

    This function takes a sequence of chord symbol strings (e.g., 'C', 'Am', 'F7') and
    converts them into a MIDI file where each chord is played as simultaneous notes.
    The function uses music21 to interpret chord symbols and extract MIDI pitches,
    then uses pretty_midi to create the actual MIDI file with customizable parameters.

    Args:
        json_path (str): Path to the original JSON file containing the chord sequence.
            Used to derive the output MIDI filename. The base name (without extension)
            will be extracted and used as part of the MIDI filename.
        sequence (list): List of chord symbol strings to convert to MIDI.
            Examples: ['C', 'Am', 'F', 'G'], ['Cmaj7', 'Dm7', 'G7', 'Cmaj7']
            Chord symbols should follow standard notation supported by music21.
        sequence_type (str): Identifier for the type of sequence being converted.
            This is appended to the MIDI filename for identification purposes.
            Examples: 'original', 'generated', 'modified'
        duration (float, optional): Duration of each chord in seconds. All chords
            will have the same duration and play sequentially. Defaults to 0.5.
        velocity (int, optional): MIDI velocity (volume) for all notes, ranging
            from 0 (silent) to 127 (maximum volume). Defaults to 100.
        program (int, optional): MIDI program number (instrument) to use, ranging
            from 0-127. 0 is typically acoustic grand piano. Defaults to 0.

    Returns:
        None: The function writes the MIDI file to disk and does not return a value.
            The output file is saved to MIDI_SEQUENCES_PATH with filename format:
            "{base_name}_{sequence_type}.mid"

    Raises:
        music21.exceptions.ChordException: If a chord symbol cannot be interpreted.
        OSError: If the output directory doesn't exist or isn't writable.
        ValueError: If velocity or program values are outside valid MIDI ranges.
    """
    # Extract base filename from JSON path to create meaningful MIDI filename
    base_name = os.path.splitext(os.path.basename(json_path))[0]
    midi_file_name = f"{base_name}_{sequence_type}.mid"
    midi_file_path = os.path.join(MIDI_SEQUENCES_PATH, midi_file_name)

    # Convert chord symbols to MIDI pitch collections
    chord_notes_list = []
    for chord_name in sequence:
        # Use music21 to interpret chord symbol and extract constituent pitches
        chord = music21.harmony.ChordSymbol(chord_name)
        # Convert music21 pitch objects to MIDI note numbers (0-127)
        midi_pitches = [p.midi for p in chord.pitches]
        chord_notes_list.append(midi_pitches)

    # Initialize MIDI file structure with specified instrument
    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=program)
    start = 0.0  # Track current time position in the sequence

    # Add each chord to the MIDI file as a collection of simultaneous notes
    for notes in chord_notes_list:
        # Create a MIDI note for each pitch in the current chord
        for note in notes:
            # All notes in the chord start and end at the same time (polyphonic)
            midi_note = pretty_midi.Note(velocity=velocity, pitch=note, start=start, end=start+duration)
            instrument.notes.append(midi_note)
        # Move to the next chord's start time (sequential chord progression)
        start += duration

    # Add the instrument to the MIDI file and write to disk
    midi.instruments.append(instrument)
    midi.write(midi_file_path)

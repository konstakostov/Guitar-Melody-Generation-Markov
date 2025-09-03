import numpy as np
import re

from Utils.variable_constants import NOTE_TO_SEMITONE


def manual_chord_to_chroma(chord_symbol):
    # Parse root note
    match = re.match(r'([A-G][#b]?)(.*)', chord_symbol)
    if not match:
        return None

    root = match.group(1)
    chord_type = match.group(2)

    if root not in NOTE_TO_SEMITONE:
        return None

    root_pc = NOTE_TO_SEMITONE[root]
    chroma = np.zeros(12)

    # Define chord intervals
    if chord_type in ['min7', 'm7']:
        # Minor 7th: root, minor third, fifth, minor seventh
        intervals = [0, 3, 7, 10]
    elif chord_type.startswith('add13'):
        # Major triad + 13th (same as 6th)
        intervals = [0, 4, 7, 9]
    else:
        return None

    # Set chroma bits
    for interval in intervals:
        chroma[(root_pc + interval) % 12] = 1

    return chroma

import re

from Utils.variable_constants import NOTE_TO_SEMITONE


def chord_sort_key(chord_name):
    """
        Custom sort key for musical ordering.
    """

    # Extract root note for primary sorting
    match = re.match(r'([A-G][#b]?)', chord_name)

    if match:
        root = match.group(1)

        return NOTE_TO_SEMITONE.get(root, 12), chord_name

    return 12, chord_name

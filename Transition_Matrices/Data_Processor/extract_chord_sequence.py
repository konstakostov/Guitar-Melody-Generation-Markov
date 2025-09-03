def extract_chord_sequence(chord_string):
    """
    Extracts a sequence of chords from a given chord string.

    This function processes a string containing chord tokens, filters out
    any tokens that are enclosed in angle brackets (e.g., `<token>`), and
    returns a list of valid chord tokens.

    Args:
        chord_string (str): A string containing chord tokens separated by spaces.

    Returns:
        list: A list of chord tokens that are not enclosed in angle brackets.
    """
    chord_sequence = []

    # Split the input string into tokens and process each token
    for token in chord_string.split():
        # Include the token only if it is not enclosed in angle brackets
        if not (token.startswith('<') or token.endswith('>')):
            chord_sequence.append(token)

    return chord_sequence

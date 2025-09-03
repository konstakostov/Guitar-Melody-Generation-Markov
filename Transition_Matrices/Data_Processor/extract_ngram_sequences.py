def extract_ngram_sequences(chord_string, n=1):
    """
    Extracts n-gram sequences from a given chord string.

    This function processes a string containing chord tokens, filters out
    any tokens that are enclosed in angle brackets (e.g., `<token>`), and
    returns a list of n-gram sequences.

    Args:
        chord_string (str): A string containing chord tokens separated by spaces.
        n (int): The size of the n-gram (1 for unigrams, 2 for bigrams, etc.).

    Returns:
        list: A list of n-gram tuples. For n=1, returns individual chords.
              For n>1, returns tuples of consecutive chord sequences.
    """

    # First extract individual chords (reuse existing logic)
    chord_sequence = []

    for token in chord_string.split():
        if not (token.startswith('<') or token.endswith('>')):
            chord_sequence.append(token)

    # Return empty list if not enough chords for n-gram
    if len(chord_sequence) < n:
        return []

    # Generate n-grams
    ngrams = []

    for i in range(len(chord_sequence) - n + 1):
        if n == 1:
            # For unigrams, return individual chords (not tuples)
            ngrams.append(chord_sequence[i])
        else:
            # For n>1, return tuples
            ngrams.append(tuple(chord_sequence[i:i + n]))

    return ngrams

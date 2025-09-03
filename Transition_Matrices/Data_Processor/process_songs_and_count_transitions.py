from Transition_Matrices.Data_Processor.extract_chord_sequence import extract_chord_sequence
from Transition_Matrices.Data_Processor.initialize_genre_data_structures import initialize_genre_data_structures


def process_songs_and_count_transitions(dataset, main_genres):
    """
    Processes a dataset of songs and counts chord transitions for specified genres.

    This function iterates through a dataset of songs, extracts chord sequences for each song,
    and counts the transitions between consecutive chords for each genre. The results are stored
    in a nested dictionary structure.

    Args:
        dataset (dict): A dictionary containing song data. It must have a 'train' key with a list of song entries.
                        Each song entry should include:
                        - 'main_genre' (str): The genre of the song.
                        - 'chords' (str): A string of chords separated by spaces.
        main_genres (list or tuple): A list or tuple of genres to process. Only songs belonging to these genres
                                     will be included in the transition counting.

    Returns:
        dict: A nested dictionary where:
            - The first key is the genre.
            - The second key is the current chord.
            - The third key is the next chord.
            - The value is the count of transitions between the two chords.

    Raises:
        ValueError: If `main_genres` is not a non-empty list or tuple.
    """
    if not main_genres or not isinstance(main_genres, (list, tuple)):
        raise ValueError("main_genres must be a non-empty list or tuple")

    # Initialize data structures for storing chord transitions
    _, genre_transitions = initialize_genre_data_structures(main_genres)

    # Iterate through the training dataset
    for entry in dataset["train"]:
        try:
            # Extract the genre and chord string from the current entry
            genre = entry["main_genre"]
            chord_string = entry.get("chords", "")

            # Skip entries with invalid or missing data
            if not genre or genre not in main_genres or not chord_string:
                continue

            # Extract the sequence of chords from the chord string
            chord_sequence = extract_chord_sequence(chord_string)

            # Skip sequences with fewer than two chords
            if len(chord_sequence) < 2:
                continue

            # Count transitions between consecutive chords
            for i in range(len(chord_sequence) - 1):
                current_chord = chord_sequence[i]
                next_chord = chord_sequence[i + 1]
                genre_transitions[genre][current_chord][next_chord] += 1

        # Handle potential errors in the dataset entry
        except (KeyError, TypeError, AttributeError):
            continue

    return genre_transitions

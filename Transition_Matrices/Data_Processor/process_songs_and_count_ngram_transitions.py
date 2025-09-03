from Transition_Matrices.Data_Processor.extract_ngram_sequences import extract_ngram_sequences
from Transition_Matrices.Data_Processor.initialize_ngram_data_structures import initialize_ngram_data_structures


def process_songs_and_count_ngram_transitions(dataset, main_genres, n=1):
    """
    Processes a dataset of songs and counts n-gram transitions for specified genres.

    This function iterates through a dataset of songs, extracts n-gram sequences for each song,
    and counts the transitions between consecutive n-grams for each genre. The results are stored
    in a nested dictionary structure.

    Args:
        dataset (dict): A dictionary containing song data. It must have a 'train' key with a list of song entries.
                        Each song entry should include:
                        - 'main_genre' (str): The genre of the song.
                        - 'chords' (str): A string of chords separated by spaces.
        main_genres (list or tuple): A list or tuple of genres to process. Only songs belonging to these genres
                                    will be included in the transition counting.
        n (int): The size of the n-gram (1 for unigrams, 2 for bigrams, etc.). Defaults to 1.

    Returns:
        dict: A nested dictionary where:
            - The first key is the genre.
            - The second key is the current n-gram (chord for n=1, tuple for n>1).
            - The third key is the next n-gram.
            - The value is the count of transitions between the two n-grams.

    Raises:
        ValueError: If `main_genres` is not a non-empty list or tuple, or if n < 1.
    """
    if not main_genres or not isinstance(main_genres, (list, tuple)):
        raise ValueError("main_genres must be a non-empty list or tuple")

    if n < 1:
        raise ValueError("n must be at least 1")

    # Initialize data structures for storing n-gram transitions
    _, genre_ngram_transitions = initialize_ngram_data_structures(main_genres, n)

    # Iterate through the training dataset
    for entry in dataset["train"]:
        try:
            # Extract the genre and chord string from the current entry
            genre = entry["main_genre"]
            chord_string = entry.get("chords", "")

            # Skip entries with invalid or missing data
            if not genre or genre not in main_genres or not chord_string:
                continue

            # Extract the sequence of n-grams from the chord string
            ngram_sequence = extract_ngram_sequences(chord_string, n)

            # Skip sequences with fewer than two n-grams (need at least 2 for transitions)
            if len(ngram_sequence) < 2:
                continue

            # Count transitions between consecutive n-grams
            for i in range(len(ngram_sequence) - 1):
                current_ngram = ngram_sequence[i]
                next_ngram = ngram_sequence[i + 1]
                genre_ngram_transitions[genre][current_ngram][next_ngram] += 1

        # Handle potential errors in the dataset entry
        except (KeyError, TypeError, AttributeError):
            continue

    return genre_ngram_transitions

from collections import defaultdict

def initialize_ngram_data_structures(main_genres, n=1):
    """
    Initializes data structures for storing genre-specific n-gram indices and transitions.

    This function creates two data structures optimized for n-gram processing:
    1. `genre_ngram_indices`: Maps n-gram sequences to their indices for each genre.
    2. `genre_ngram_transitions`: Maps n-gram sequences to their following sequences with counts.

    Args:
        main_genres (list): A list of genre names (strings) for which the data structures will be initialized.
        n (int): The size of the n-gram. For n=1 (unigrams), handles individual chords.
                 For n>1, handles tuples of chord sequences.

    Returns:
        tuple: A tuple containing:
            - genre_ngram_indices (dict): Dictionary for storing n-gram-to-index mappings for each genre.
            - genre_ngram_transitions (dict): Dictionary for storing n-gram transition counts for each genre.
    """
    # Initialize a dictionary for n-gram-to-index mappings for each genre
    genre_ngram_indices = {genre: {} for genre in main_genres}

    # Initialize a dictionary for n-gram transition counts for each genre
    # The structure depends on n-gram size:
    # - For n=1: chord -> chord -> count
    # - For n>1: (chord_tuple) -> (chord_tuple) -> count
    genre_ngram_transitions = {genre: defaultdict(lambda: defaultdict(int)) for genre in main_genres}

    return genre_ngram_indices, genre_ngram_transitions

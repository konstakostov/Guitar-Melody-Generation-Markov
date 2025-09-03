from collections import defaultdict

def initialize_genre_data_structures(main_genres):
    """
    Initializes data structures for storing genre-specific chord indices and transitions.

    This function creates two data structures:
    1. `genre_chord_indices`: A dictionary where each key is a genre, and the value is an empty dictionary.
       This is used to store mappings of chords to their indices for each genre.
    2. `genre_transitions`: A dictionary where each key is a genre, and the value is a nested defaultdict.
       The nested defaultdict maps a chord to another chord with an integer count, representing the number
       of transitions between the two chords for that genre.

    Args:
        main_genres (list): A list of genre names (strings) for which the data structures will be initialized.

    Returns:
        tuple: A tuple containing:
            - genre_chord_indices (dict): A dictionary for storing chord-to-index mappings for each genre.
            - genre_transitions (dict): A dictionary for storing chord transition counts for each genre.
    """
    # Initialize a dictionary for chord-to-index mappings for each genre
    genre_chord_indices = {genre: {} for genre in main_genres}

    # Initialize a dictionary for chord transition counts for each genre
    # The nested defaultdict structure allows automatic initialization of integer counts
    genre_transitions = {genre: defaultdict(lambda: defaultdict(int)) for genre in main_genres}

    return genre_chord_indices, genre_transitions

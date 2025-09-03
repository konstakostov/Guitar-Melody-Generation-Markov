from Transition_Matrices.Data_Processor.process_songs_and_count_ngram_transitions import process_songs_and_count_ngram_transitions
from Transition_Matrices.Matrix_Builder.create_transition_matrix import create_transition_matrix


def build_genre_ngram_transition_matrices(dataset, main_genres, n=1, min_count=1):
    """
    Build n-gram transition matrices for multiple musical genres from a dataset.

    This function processes a dataset of songs to extract n-gram transition patterns
    for each specified genre, then creates normalized probabilistic transition matrices
    suitable for Markov chain music generation. It handles multiple genres simultaneously
    and provides robust error handling for genres with insufficient data.

    Args:
        dataset: Dataset containing musical data with genre labels. Expected to be
            compatible with the data processor that extracts chord sequences and
            genre information from songs.
        main_genres (list or tuple): Collection of genre names to process. Each genre
            must be present in the dataset. Examples: ['blues', 'jazz', 'rock'].
        n (int, optional): The n-gram size for transition analysis. Must be >= 1.
            - n=1: Chord-level transitions (C -> Am)
            - n=2: Bigram transitions ((C,Am) -> (Am,F))
            - n=3+: Higher-order n-gram patterns
            Defaults to 1.
        min_count (int, optional): Minimum transition count threshold for inclusion
            in the matrix. Transitions occurring fewer than this many times are
            filtered out to reduce noise. Defaults to 1.

    Returns:
        dict: Dictionary mapping genre names to their transition matrix data structures.
            Structure: {
                'genre_name': {
                    'matrix': numpy.ndarray or scipy.sparse matrix - normalized transition matrix,
                    'ngram_to_idx': dict - mapping from n-gram strings to matrix indices,
                    'idx_to_ngram': dict - mapping from matrix indices to n-gram strings
                },
                ...
            }
            Genres that fail matrix creation are excluded from the returned dictionary.

    Raises:
        ValueError: If main_genres is empty, not a list/tuple, or if n < 1.
    """
    # Validate input parameters to ensure they meet requirements
    if not main_genres or not isinstance(main_genres, (list, tuple)):
        raise ValueError("main_genres must be a non-empty list or tuple")

    if n < 1:
        raise ValueError("n must be at least 1")

    # Extract n-gram transition counts for all specified genres from the dataset
    # This processes the entire dataset and groups transitions by genre
    genre_ngram_transitions = process_songs_and_count_ngram_transitions(dataset, main_genres, n)

    # Dictionary to store successfully created transition matrices for each genre
    transition_matrices = {}

    # Process each genre's transition data to create normalized probability matrices
    for genre, transitions in genre_ngram_transitions.items():
        try:
            # Create transition matrix with sparse format for memory efficiency
            # min_count filtering removes rare transitions to reduce noise
            matrix, ngram_to_idx, idx_to_ngram = create_transition_matrix(
                transitions,
                use_sparse=True,
                min_count=min_count
            )

            # Store complete matrix data structure for this genre
            # Includes matrix and both direction mappings for easy access
            transition_matrices[genre] = {
                "matrix": matrix,
                "ngram_to_idx": ngram_to_idx,
                "idx_to_ngram": idx_to_ngram
            }

        except ValueError as e:
            # Handle genres with insufficient data gracefully
            # Print warning but continue processing other genres
            print(f"Warning: Could not create matrix for genre '{genre}': {e}")
            continue

    return transition_matrices

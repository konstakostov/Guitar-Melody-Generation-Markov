from Transition_Matrices.Data_Processor.process_songs_and_count_transitions import process_songs_and_count_transitions
from Transition_Matrices.Matrix_Builder.create_transition_matrix import create_transition_matrix


def build_genre_transition_matrices(dataset, main_genres):
    """
    Builds transition matrices for each genre based on a dataset of songs.

    This function processes a dataset to count chord transitions for specified genres
    and then creates transition matrices for each genre. The matrices include mappings
    between chords and their indices.

    Args:
        dataset (dict): A dictionary containing song data. It must have a 'train' key with a list of song entries.
                        Each song entry should include:
                        - 'main_genre' (str): The genre of the song.
                        - 'chords' (str): A string of chords separated by spaces.
        main_genres (list or tuple): A list or tuple of genres to process. Only songs belonging to these genres
                                     will be included in the transition counting.

    Returns:
        dict: A dictionary where each key is a genre, and the value is another dictionary containing:
              - 'matrix' (numpy.ndarray): The transition matrix for the genre.
              - 'chord_to_idx' (dict): A mapping from chords to their indices in the matrix.
              - 'idx_to_chord' (dict): A mapping from indices to their corresponding chords.
    """
    # Count chord transitions for each genre
    genre_transitions = process_songs_and_count_transitions(dataset, main_genres)

    # Initialize a dictionary to store transition matrices
    transition_matrices = {}

    # Create a transition matrix for each genre
    for genre, transitions in genre_transitions.items():
        # Generate the transition matrix and chord mappings
        matrix, chord_to_idx, idx_to_chord = create_transition_matrix(transitions)

        # Store the results in the dictionary
        transition_matrices[genre] = {
            "matrix": matrix,
            "chord_to_idx": chord_to_idx,
            "idx_to_chord": idx_to_chord
        }

    return transition_matrices
